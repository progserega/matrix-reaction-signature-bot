#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import configparser
import logging
from logging import handlers
import traceback
import sys
import json
import os
import traceback
import datetime
import psycopg2
import psycopg2.extras
import time

config = None
log = None
global_error_descr=""
conn=None
cur=None

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
  if connect_to_db() == False:
    log.error("connect_to_db()")
    return False
  log.info("success init sql module")
  return True

def connect_to_db():
  global conn
  global cur
  try:
    log.debug("connect to: dbname='" + config["database"]["db_name"] + "' user='" +config["database"]["db_user"] + "' host='" + config["database"]["db_host"] + "' password='" + config["database"]["db_passwd"] + "'")
    conn = psycopg2.connect("dbname='" + config["database"]["db_name"] + "' user='" +config["database"]["db_user"] + "' host='" + config["database"]["db_host"] + "' password='" + config["database"]["db_passwd"] + "'")
    cur = conn.cursor()
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    log.error("I am unable to connect to the database")
    return False
  return True

def update_signature(room_id,mxid,signature,signature_author,signature_descr):
  global config
  global client
  global log

  try:
    # формируем sql-запрос:
    columns = "signature, signature_author, signature_time_create, description_signature"
    values = "'%(signature)s', '%(signature_author)s', %(signature_time_create)s, '%(description_signature)s'"%\
      {\
        "signature":signature,\
        "signature_author":signature_author,\
        "signature_time_create":psycopg2.TimestampFromTicks(time.time()),\
        "description_signature":signature_descr\
      }
    sql="update tbl_users_info SET (%s) = (%s) where mxid='%s' and room_id='%s' RETURNING user_id"%(columns,values,mxid,room_id)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
      cur.execute('SELECT LASTVAL()')
      id_of_new_row = cur.fetchone()[0]
    except psycopg2.Error as e:
      global_error_descr="I am unable update data to tbl_users_info: %s" % e.pgerror
      log.error(global_error_descr)
      log.info("try rollback insertion for this connection")
      try:
        conn.rollback()
      except psycopg2.Error as e:
        log.error("sql error: %s" % e.pgerror)
        return False
      return False

  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    global_error_descr="internal script error - see logs"
    log.error(global_error_descr)
    return False
  return True


def insert_signature(room_id,mxid,signature,signature_author,signature_descr):
  global config
  global client
  global log

  try:
    # формируем sql-запрос:
    columns = "mxid, room_id, signature, signature_author, signature_time_create, description_signature"
    values = "'%(mxid)s','%(room_id)s', '%(signature)s', '%(signature_author)s', %(signature_time_create)s, '%(description_signature)s'"%\
      {\
        "mxid":mxid,\
        "room_id":room_id,\
        "signature":signature,\
        "signature_author":signature_author,\
        "signature_time_create":psycopg2.TimestampFromTicks(time.time()),\
        "description_signature":signature_descr\
      }
    sql="insert INTO tbl_users_info (%s) VALUES (%s) RETURNING user_id"%(columns,values)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
      cur.execute('SELECT LASTVAL()')
      id_of_new_row = cur.fetchone()[0]
    except psycopg2.Error as e:
      global_error_descr="I am unable insert data to tbl_sending_queue: %s" % e.pgerror
      log.error(global_error_descr)
      log.info("try rollback insertion for this connection")
      try:
        conn.rollback()
      except psycopg2.Error as e:
        log.error("sql error: %s" % e.pgerror)
        return False
      return False

  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    global_error_descr="internal script error - see logs"
    log.error(global_error_descr)
    return False
  return True

def add_signature(room_id,mxid,signature,signature_author,signature_descr):
  global config
  global log
  if get_signature(room_id,mxid) is None:
    return insert_signature(room_id,mxid,signature,signature_author,signature_descr)
  else:
    return update_signature(room_id,mxid,signature,signature_author,signature_descr)

def get_signature(room_id,mxid):
  global config
  global log
  item = None
  try:
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select signature from tbl_users_info where room_id='%s' and mxid='%s'"%(room_id,mxid)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchone()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item==None:
      log.debug("no signature records for room_id=%s and mxid=%s"%(room_id,mxid))
      return None
    log.debug("execute function time=%f"%(time.time()-time_execute))
    return item[0]
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None
