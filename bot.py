#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import nio
import configparser
import logging
from logging import handlers
import sys
import json
import os
import traceback
import datetime
import psycopg2
import psycopg2.extras
import time
import sql
import commands
import matrix_api

config = None
client = None
log = None
session = {}

async def send_emotion(room_id,event_id,emotion_text):
  global config
  global client
  global log
  content = {
        "m.relates_to": {
          "event_id": event_id,
          "key": emotion_text,
          "rel_type": "m.annotation"
        }
    }
  try:
      await client.room_send(room_id, message_type="m.reaction", content=content)
      log.debug("st reaction successfully")
  except Exception:
      log.error(f"set reaction failed.")

async def unknown_cb(room, event):
  global config
  global client
  global log
  #if room.display_name == "Сергей2":
  log.debug(room.room_id)
  log.debug(event)

async def message_cb(room, event):
  global config
  global client
  global log

  log.debug("start function")
  #log.debug(room.room_id)
  #log.debug(event)

  # проверяем, что обращаются к нам:
  nick_name = room.user_name(session["user_id"])
  if re.search(' *%s *'%nick_name,event.body)) is not None:
    command = re.sub(' *%s *'%nick_name, '', event.body)
    if async commands.process_command(room, event, command) == False:
      log.error("commands.process_command()")
      return False
  if async set_read_marker(room,event) == False:
    log.error("matrix_api.set_read_marker()")
    return False
  return True


def write_details_to_disk(session) -> None:
  global config
  # open the config file in write-mode
  with open(config["matrix"]["session_store_path"], "w") as f:
    # write the login details to disk
    json.dump(session,f)


async def main():
  global config
  global client
  global session

  session = {}

  # If there are no previously-saved credentials, we'll use the password
  if not os.path.exists(config["matrix"]["session_store_path"]):
    client = nio.AsyncClient(config["matrix"]["matrix_server"], config["matrix"]["matrix_login"])

    resp = await client.login(config["matrix"]["matrix_passwd"])
    # check that we logged in succesfully
    if isinstance(resp, nio.LoginResponse):
      session["homeserver"] = config["matrix"]["matrix_server"]  # e.g. "https://matrix.example.org"
      session["user_id"] = resp.user_id  # e.g. "@user:example.org"
      session["device_id"] = resp.device_id  # device ID, 10 uppercase letters
      session["access_token"] = resp.access_token  # cryptogr. access token
      log.info("login by password")
  else:
    # open the file in read-only mode
    with open(config["matrix"]["session_store_path"], "r") as f:
      session = json.load(f)
      client = nio.AsyncClient(session["homeserver"])
      client.access_token = session["access_token"]
      client.user_id = session["user_id"]
      client.device_id = session["device_id"]

      resp = client.restore_login(
        user_id=session["user_id"],
        device_id=session["device_id"],
        access_token=session["access_token"],
      )  # returns always None, on success or failure
    log.info("login by session")

  client.add_event_callback(message_cb, nio.RoomMessageText)
  client.add_event_callback(unknown_cb, nio.RoomMessage)

  # инициализация модулей:
  if sql.init(log,config) == False:
    log.error("sql.init()")
    return False
  log.info("sql.init()")
  if commands.init(log,config) == False:
    log.error("commands.init()")
    return False
  log.info("commands.init()")
  if matrix_api.init(log,config,client) == False:
    log.error("matrix_api.init()")
    return False
  log.info("matrix_api.init()")
  
  while True:
    if "token" in session:
      token = session["token"]
      resp = await client.sync(full_state=True, since=session['token'])
    else:
      resp = await client.sync(timeout=1000,full_state=True)
    session["token"] = resp.next_batch
    # save token
    write_details_to_disk(session)
    log.info("iteration")
    time.sleep(3)
  #f=open("out.json","w+")
  #f.write(json.dumps(resp, indent=4, sort_keys=True,ensure_ascii=True))
  #f.close()
  #sys.exit(0)
  #await client.sync_forever(timeout=30000,full_state=True)#,since="token123")



def loadConfig(file_name):
  config = configparser.ConfigParser()
  config.read(file_name)
  return config

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("need 1 param - config file")
    sys.exit(1)
  else:
    config=loadConfig(sys.argv[1])
  log=logging.getLogger("matrix-reaction-signature-bot")

  if config["logging"]["debug"].lower()=="yes":
    log.setLevel(logging.DEBUG)
  else:
    log.setLevel(logging.INFO)

  # create the logging file handler
  #fh = logging.FileHandler(config.log_path)
  fh = logging.handlers.TimedRotatingFileHandler(config["logging"]["log_path"], when=config["logging"]["log_backup_when"], backupCount=int(config["logging"]["log_backup_count"]), encoding='utf-8')
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s() %(levelname)s - %(message)s')
  fh.setFormatter(formatter)

#  if config["logging"]["debug"].lower()=="yes":
  # логирование в консоль:
  stdout = logging.StreamHandler(sys.stdout)
  stdout.setFormatter(formatter)
  log.addHandler(stdout)

  # add handler to logger object
  log.addHandler(fh)

  log.info("Program started")
  log.info("python version=%s"%sys.version)

  asyncio.get_event_loop().run_until_complete(main())
  #if main()==False:
  #  log.error("error main()")
  #  sys.exit(1)
  log.info("program exit success")

