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
import re
import matrix_api
import sql

config = None
client = None
log = None


def get_exception_traceback_descr(e):
  if hasattr(e, '__traceback__'):
    tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
    result=""
    for msg in tb_str:
      result+=msg
    return result
  else:
    return e

def init(log_param,config_param):
  global log
  global config
  log = log_param
  config = config_param
  log.info("success init commands module")
  return True

def parse_command_line(commandline):
  try:
    params = re.split('"|\'| ',commandline)
    log.debug(params)

    # собираем папраметры:
    result_params = []
    many_words = False
    current_many_words_param = ""
    for param in params:
      if many_words == False:
        if param != '':
          result_params.append(param)
        else:
          many_words = True
      else:
        if param != '':
          current_many_words_param+=param
          current_many_words_param+=" "
        else:
          many_words = False
          result_params.append(current_many_words_param.strip())
          current_many_words_param=""
    log.debug(result_params)
    return result_params
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None

async def process_command(room,event,commandline):
  global config
  global client
  global log
  log.debug("start function")

  log.debug("command in room %s (id: %s): %s"%(room.display_name, room.room_id, commandline))

  param_list = parse_command_line(commandline)

  if len(param_list) == 0:
    log.warning("empty command - skip")
    command = "help"
    parameters = []
  else:
    command = param_list[0]
    parameters = param_list[1:]
  #=========== help command =========
  if command == "help":
    help_text="""I am admin reaction bot.
1. help - this help
2. add_signature - add signature to user
    """
    if await matrix_api.send_text(room,help_text) == False:
      log.error("matrix_api.send_text()")
      return False
    return True

  elif command == "add_signature":
    if len(parameters) < 3:
      help_text="""command `add_signature` need 3 params.
syntax:

  my_botname_in_this_room: add_signature user_name_for_signature signature_text "description - Why signature added to user"

example:
  rsbot: add_signature Baduser "spammer" "This user spam in this room!"

      """
      if await matrix_api.send_text(room,help_text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True
    else:
      # параметров достаточно:
      signature_user = parameters[0]
      signature = parameters[1]
      signature_descr = parameters[2]

      if signature_user in room.users:
        # пользователь указан по MXID:
        signature_user_mxid = signature_user
      elif signature_user in room.names:
        # пользователь указан по имени
        if len(room.names[signature_user])>1:
          # несколько пользователей с одинаковыми именами:
          text="""nickname %s not uniqum in this room. Please, select user by mxid (as @user:server.com)"""%signature_user
          log.warning(text)
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return True
        else:
          # пользователь указан по MXID:
          signature_user_mxid = room.names[signature_user][0]
      else:
        # неизвестный пользователь:
        text="""nickname %s not known. Please, correct, or select user by mxid (as @user:server.com)"""%signature_user
        log.warning(text)
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True
      log.debug("signature_user_mxid = %s"%signature_user_mxid)
      if sql.add_signature(room.room_id, signature_user_mxid, signature, event.sender, signature_descr ) == False:
        log.error("sql.add_signature()")
        text="""internal error sql.add_signature()"""
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return False
      # уведомляем пользователя, что всё получилось:
      text="""success add signature to user %s"""%signature_user_mxid
      if await matrix_api.send_text(room,text) == False:
        log.error("matrix_api.send_text()")
        return False

      return True


  else:
    # unknown command:
    help_text="""unknown command!
Please, use 'help' or empty command (only my room nick name) for help.
    """
    if await matrix_api.send_text(room,help_text) == False:
      log.error("matrix_api.send_text()")
      return False
    return True
