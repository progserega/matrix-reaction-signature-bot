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
  log.debug("start function")
  config = config_param
  if connect_to_db() == False:
    log.error("connect_to_db()")
    return False
  log.info("success init sql module")
  return True

def connect_to_db():
  global conn
  global cur
  db_params = {}
  if "db_name" in config["database"]:
    db_params['dbname'] = config["database"]["db_name"]
  if "db_user" in config["database"]:
    db_params['user'] = config["database"]["db_user"]
  if "db_host" in config["database"]:
    db_params['host'] = config["database"]["db_host"]
  if "db_passwd" in config["database"]:
    db_params['password'] = config["database"]["db_passwd"]
  try:
    log.debug("start function")
    log.debug("connect to: dbname='" + db_params.get('dbname','') + "' user='" + db_params.get('user','') + "' host='" + db_params.get('host','') + "' password='" + db_params.get('password','') + "'")
    conn = psycopg2.connect(**db_params)
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
  global conn
  global cur

  try:
    log.debug("start function")
    # формируем sql-запрос:
    columns = "signature, signature_author, signature_time_create, signature_description"
    values = "'%(signature)s', '%(signature_author)s', %(signature_time_create)s, '%(signature_description)s'"%\
      {\
        "signature":signature,\
        "signature_author":signature_author,\
        "signature_time_create":psycopg2.TimestampFromTicks(time.time()),\
        "signature_description":signature_descr\
      }
    sql="update tbl_users_info SET (%s) = (%s) where mxid='%s' and room_id='%s'"%(columns,values,mxid,room_id)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
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
  global log
  global conn
  global cur

  try:
    log.debug("start function")
    # формируем sql-запрос:
    columns = "mxid, room_id, signature, signature_author, signature_time_create, signature_description"
    values = "'%(mxid)s','%(room_id)s', '%(signature)s', '%(signature_author)s', %(signature_time_create)s, '%(signature_description)s'"%\
      {\
        "mxid":mxid,\
        "room_id":room_id,\
        "signature":signature,\
        "signature_author":signature_author,\
        "signature_time_create":psycopg2.TimestampFromTicks(time.time()),\
        "signature_description":signature_descr\
      }
    sql="insert INTO tbl_users_info (%s) VALUES (%s) RETURNING user_id"%(columns,values)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
      cur.execute('SELECT LASTVAL()')
      id_of_new_row = cur.fetchone()[0]
    except psycopg2.Error as e:
      global_error_descr="I am unable insert data to tbl_users_info: %s" % e.pgerror
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

def enable_signature(room_id,mxid,enable_flag):
  global config
  global log
  log.debug("start function")

  try:
    # формируем sql-запрос:
    sql="update tbl_users_info SET signature_show=%s where mxid='%s' and room_id='%s'"%(enable_flag,mxid,room_id)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
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

def add_signature(room_id,mxid,signature,signature_author,signature_descr):
  global config
  global log
  global conn
  global cur
  log.debug("start function")
  ret=check_user_exist(room_id,mxid) 
  if ret is None:
    log.error("sql.check_user_exist()")
    return False
  if ret == 0:
    return insert_signature(room_id,mxid,signature,signature_author,signature_descr)
  else:
    return update_signature(room_id,mxid,signature,signature_author,signature_descr)

def get_signature(room_id,mxid):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select signature from tbl_users_info where room_id='%s' and mxid='%s' and signature_show=True"%(room_id,mxid)
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

def get_room_settings(room_id):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select name,value from tbl_room_settings where room_id='%s'"%room_id
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchall()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item==None:
      log.debug("no settings for room %s"%room_id)
      return None
    log.debug("execute function time=%f"%(time.time()-time_execute))
    return item
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None

def set_global_setting(name,value):
  global config
  global log
  global conn
  global cur
  try:
    log.debug("start function")
    # формируем sql-запрос:
    sql="""
INSERT INTO tbl_global_settings (name,value) VALUES ('%(name)s','%(value)s')
ON CONFLICT (name) DO UPDATE SET value = '%(value)s';
    """%{\
      "name":name,\
      "value":value\
    }
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
    except psycopg2.Error as e:
      global_error_descr="I am unable insert/update data: %s" % e.pgerror
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
    return False
  return True

def set_room_setting(room_id,name,value):
  global config
  global log
  global conn
  global cur
  try:
    log.debug("start function")
    # формируем sql-запрос:
    sql="""
INSERT INTO tbl_room_settings (room_id,name,value) VALUES ('%(room_id)s','%(name)s','%(value)s')
ON CONFLICT (room_id,name) DO UPDATE SET value = '%(value)s';
    """%{\
      "room_id":room_id,\
      "name":name,\
      "value":value\
    }
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
    except psycopg2.Error as e:
      global_error_descr="I am unable insert/update data: %s" % e.pgerror
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
    return False
  return True

def get_global_settings():
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select name,value from tbl_global_settings"
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchall()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item==None:
      log.debug("no global settings")
      return None
    log.debug("execute function time=%f"%(time.time()-time_execute))
    return item
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None

def get_signature_descr(room_id,mxid):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select signature,signature_author,signature_time_create,signature_show,signature_description from tbl_users_info where room_id='%s' and mxid='%s'"%(room_id,mxid)
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
    return item
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None

def check_user_exist(room_id,mxid):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select count(user_id) from tbl_users_info where room_id='%s' and mxid='%s'"%(room_id,mxid)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchone()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item[0]==0:
      log.debug("no user records for room_id=%s and mxid=%s"%(room_id,mxid))
    log.debug("execute function time=%f"%(time.time()-time_execute))
    return item[0]
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None


def add_rule_interruption(room_id,mxid,rule_interruption_descr,mxid_author):
  global config
  global log
  global conn
  global cur
  try:
    log.debug("start function")
    # формируем sql-запрос:
    ret = check_user_exist(room_id,mxid)
    if ret is None:
      log.error("sql.check_user_exist()")
      return False
    if ret == 0:
      # нет такого пользователя - нужно завести (через функцию добавления пустой подписи):
      if insert_signature(room_id,mxid,signature="",signature_author="",signature_descr="") == False:
        log.error("sql.insert_signature()")
        return False
    # добавляем запись о нарушении правил:
    sql="""START TRANSACTION;
      insert into tbl_rule_interruptions
        (user_id, rule_interruption_author, description)
        VALUES
        ((select user_id from tbl_users_info where mxid='%(mxid)s' and room_id='%(room_id)s'), '%(mxid_author)s', '%(rule_interruption_descr)s');

        update tbl_users_info set
          rule_interruption_active_count = rule_interruption_active_count + 1,
          rule_interruption_count_all = rule_interruption_count_all + 1
          where mxid='%(mxid)s' and room_id='%(room_id)s';
    COMMIT;
    """%{\
      "room_id":room_id,\
      "mxid":mxid,\
      "rule_interruption_descr":rule_interruption_descr,\
      "mxid_author":mxid_author\
    }
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
    except psycopg2.Error as e:
      global_error_descr="I am unable insert/update data: %s" % e.pgerror
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
    return False
  return True

# только активные нарушения - из одной таблицы:
def get_active_rule_interruption_count(room_id,mxid):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select rule_interruption_active_count from tbl_users_info where room_id='%s' and mxid='%s'"%(room_id,mxid)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchone()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item==None:
      log.debug("no interruption records for room_id=%s and mxid=%s"%(room_id,mxid))
      return None
    log.debug("execute function time=%f"%(time.time()-time_execute))
    return item[0]
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None

# функция даёт возможность получить активные или неактивные типы нарушений:
def get_rule_interruption_count(room_id,mxid,active=True):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select count(*) from tbl_rule_interruptions where active_rule_interruption=%s and user_id=(select user_id from tbl_users_info where room_id='%s' and mxid='%s');"%(active,room_id,mxid)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchone()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item==None:
      log.debug("no interruption records for room_id=%s and mxid=%s"%(room_id,mxid))
      return None
    log.debug("execute function time=%f"%(time.time()-time_execute))
    return item[0]
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None

# функция даёт возможность получить активные или неактивные описания нарушений:
def get_rule_interruption_descr(room_id,mxid,active=True):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select rule_interruption_author,time_create,description from tbl_rule_interruptions where active_rule_interruption=%s and user_id=(select user_id from tbl_users_info where room_id='%s' and mxid='%s');"%(active,room_id,mxid)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchall()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item==None:
      log.debug("no interruption records for room_id=%s and mxid=%s"%(room_id,mxid))
      return None
    log.debug("execute function time=%f"%(time.time()-time_execute))
    return item
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None

# очищаем список активных замечаний:
def clear_active_rule_interruption(room_id,mxid):
  global config
  global log
  global conn
  global cur
  try:
    log.debug("start function")
    # формируем sql-запрос:
    ret = check_user_exist(room_id,mxid)
    if ret is None:
      log.error("sql.check_user_exist()")
      return False
    # добавляем запись о нарушении правил:
    sql="""START TRANSACTION;
      update tbl_rule_interruptions
        set active_rule_interruption=False
        where
        user_id=(select user_id from tbl_users_info where mxid='%(mxid)s' and room_id='%(room_id)s');

        update tbl_users_info set
          rule_interruption_active_count = 0
          where mxid='%(mxid)s' and room_id='%(room_id)s';
    COMMIT;
    """%{\
      "room_id":room_id,\
      "mxid":mxid\
    }
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
    except psycopg2.Error as e:
      log.error("I am unable update data: %s" % e.pgerror)
      log.info("try rollback insertion for this connection")
      try:
        conn.rollback()
      except psycopg2.Error as e:
        log.error("sql error: %s" % e.pgerror)
        return False
      return False
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return False
  return True


def add_user_descr(room_id,mxid,user_descr):
  global config
  global log
  global conn
  global cur
  log.debug("start function")
  ret=check_user_exist(room_id,mxid) 
  if ret is None:
    log.error("sql.check_user_exist()")
    return False
  if ret == 0:
    return insert_user_descr(room_id,mxid,user_descr)
  else:
    return update_user_descr(room_id,mxid,user_descr)

def update_user_descr(room_id,mxid,user_descr):
  global config
  global log
  global conn
  global cur

  try:
    log.debug("start function")
    # формируем sql-запрос:
    sql="update tbl_users_info SET user_description='%s' where mxid='%s' and room_id='%s'"%(user_descr,mxid,room_id)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
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

def insert_user_descr(room_id,mxid,user_descr):
  global config
  global log
  global conn
  global cur

  try:
    log.debug("start function")
    # формируем sql-запрос:
    columns = "mxid, room_id, user_description"
    values = "'%(mxid)s','%(room_id)s', '%(user_descr)s'"%\
      {\
        "mxid":mxid,\
        "room_id":room_id,\
        "user_descr":user_descr\
      }
    sql="insert INTO tbl_users_info (%s) VALUES (%s) RETURNING user_id"%(columns,values)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      conn.commit()
      cur.execute('SELECT LASTVAL()')
      id_of_new_row = cur.fetchone()[0]
    except psycopg2.Error as e:
      global_error_descr="I am unable insert data to tbl_users_info: %s" % e.pgerror
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

def get_user_descr(room_id,mxid):
  global config
  global log
  global conn
  global cur
  item = None
  try:
    log.debug("start function")
    time_execute=time.time()
    # формируем sql-запрос:
    sql="select user_description from tbl_users_info where room_id='%s' and mxid='%s'"%(room_id,mxid)
    log.debug("sql='%s'"%sql)
    try:
      cur.execute(sql)
      item = cur.fetchone()
    except psycopg2.Error as e:
      log.error("sql error: %s" % e.pgerror)
      return None
    if item==None:
      log.debug("no user records for room_id=%s and mxid=%s"%(room_id,mxid))
      return None
    log.debug("execute function time=%f"%(time.time()-time_execute))
    if item[0] is None:
      return ""
    return item[0]
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return None
