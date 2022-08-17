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

def is_power_level_for_signature(room,mxid):
  global config
  global client
  global log
  try:
    log.debug("start function")
    need_power_level_config = config["powers"]["power_level_for_signature"]
    try:
      need_power_level_integer = int(need_power_level_config)
    except:
      log.debug("power_level_for_signature is not int")
      # пробуем через имя:
      if hasattr(room.power_levels.defaults, need_power_level_config):
        need_power_level_integer = getattr(room.power_levels.defaults, need_power_level_config)
      else:
        log.warning("unknown power_level alias in config - set default as 'ban'")
        # значение по-умолчанию - 'ban':
        need_power_level_integer = room.power_levels.defaults.ban
    # прповеряем - есть ли нужные права у пользователя:
    if room.power_levels.users[mxid] >= need_power_level_integer:
      return True
    else:
      return False
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return False

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
3. enable_signature - enable/disable showing signature for user
4. show_signature - show signature for user
    """
    if await matrix_api.send_text(room,help_text) == False:
      log.error("matrix_api.send_text()")
      return False
    return True

  elif command == "enable_signature":
    # проверяем права доступа:
    if is_power_level_for_signature(room,event.sender) == False:
      log.warning("no power level for this")
      text="""you need more power level for this command"""
      log.warning(text)
      if await matrix_api.send_text(room,text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True

    if len(parameters) < 2:
      help_text="""This command disable or enable showing signature for user.
Disabling - is not delete signature in db, but it will not be show.

command `enable_signature` need 2 params.
syntax:

  my_botname_in_this_room: enable_signature user_name_for_signature yes/no

example:
  rsbot: enable_signature Baduser yes

      """
      if await matrix_api.send_text(room,help_text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True
    else:
      # параметров достаточно:
      signature_user = parameters[0]
      enable_flag_str = parameters[1]

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
      enable_flag = False
      if enable_flag_str.lower() == "yes":
        enable_flag = True

      if sql.enable_signature(room.room_id, signature_user_mxid, enable_flag) == False:
        log.error("sql.enable_signature()")
        text="""internal error sql.enable_signature()"""
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return False
      # уведомляем пользователя, что всё получилось:
      if enable_flag == True:
        text="""success enable signature to user %s"""%signature_user_mxid
      else:
        text="""success disable signature to user %s"""%signature_user_mxid
      if await matrix_api.send_text(room,text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True

  elif command == "add_signature":
    # проверяем права доступа:
    if is_power_level_for_signature(room,event.sender) == False:
      log.warning("no power level for this")
      text="""you need more power level for this command"""
      log.warning(text)
      if await matrix_api.send_text(room,text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True

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

  elif command == "show_signature":

    if len(parameters) < 1:
      help_text="""This command show signature record for user.

command `show_signature` need 1 params.
syntax:

  my_botname_in_this_room: show_signature user_name

example:
  rsbot: show_signature Baduser

      """
      if await matrix_api.send_text(room,help_text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True
    else:
      # параметров достаточно:
      signature_user = parameters[0]

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

      ret = sql.check_user_exist(room.room_id, signature_user_mxid)
      if ret is None:
        log.error("sql.check_user_exist()")
        text="""internal error sql.check_user_exist()"""
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return False
      log.debug(ret)
      if ret == 0:
        text = "no such user in db: %s"%signature_user_mxid
        log.debug(text)
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return False

      # получаем данные о записи:
      ret = sql.get_signature_descr(room.room_id, signature_user_mxid)
      if ret is None:
        log.error("sql.get_signature_descr()")
        text="""internal error sql.get_signature_descr()"""
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return False
      # формируем отчёт:
      text = """User %(signature_user_mxid)s:
1. signature: %(signature)s
2. Author of signature: %(signature_author)s
3. Time create/update of signature: %(signature_time_create)s
4. Show signature: %(signature_show)s
5. Description signature: %(signature_descr)s
"""%{\
      "signature_user_mxid":signature_user_mxid,\
      "signature":ret[0],\
      "signature_author":ret[1],\
      "signature_time_create":ret[2],\
      "signature_show":ret[3],\
      "signature_descr":ret[4]\
      }
      # показываем отчёт:
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
