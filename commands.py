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
import gettext

config = None
client = None
log = None
db_bot_settings = {}


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

  # локализация. Стандартный вариант, без переключения локали на-лету. Опция языка берётся из переменных 
  # окружения LC_*:
  # переводимые строки заключать в символы _("english text id")
  # https://habr.com/ru/post/73554/
  # https://docs.python.org/3/library/gettext.html
  #
  #gettext.install('commands', './locale')

  log.info("success init commands module")
  return True

def update_db_bot_settings_cache(room_id=None):
  global log
  global db_bot_settings
  try:
    global_settings = sql.get_global_settings()
    db_bot_settings["global_settings"]={}
    if global_settings is None:
      log.warning("sql.get_global_settings() return None")
    else:
      for line in global_settings:
        db_bot_settings["global_settings"][line[0]]=line[1]
        
    if "room_settings" not in db_bot_settings:
      db_bot_settings["room_settings"]={}
    if room_id is not None:
      room_settings=sql.get_room_settings(room_id)
      db_bot_settings["room_settings"][room_id]={}
      if room_settings is None:
        log.warning("sql.get_room_settings() return None")
      else:
        for line in room_settings:
          db_bot_settings["room_settings"][room_id][line[0]]=line[1]
      # устанавливаем значение локали по умолчанию в английскую:
      if "locale" not in db_bot_settings["room_settings"][room_id]:
        db_bot_settings["room_settings"][room_id]["locale"]="en"
    log.debug(db_bot_settings)
    return True
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return False

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
  global global_settings
  global room_settings

  try:
    log.debug("start function")
    log.debug("command in room %s (id: %s): %s"%(room.display_name, room.room_id, commandline))

    # update options:
    if "room_settings" in db_bot_settings and room.room_id in db_bot_settings["room_settings"]:
      # опции уже загружены:
      pass
    else:
      # нужно обновить кэш опций:
      if update_db_bot_settings_cache(room.room_id) == False:
        log.error("update_db_bot_settings_cache()")
        return False
      # включаем локаль:
      lang_setting = db_bot_settings["room_settings"][room.room_id]["locale"]
      lang = gettext.translation('commands', localedir='./locale', languages=[lang_setting])
      lang.install()

    param_list = parse_command_line(commandline)

    if len(param_list) == 0:
      log.warning("empty command - skip")
      command = "help"
      parameters = []
    else:
      command = param_list[0]
      parameters = param_list[1:]
    #=========== help command =========
    if command == "help" or command == _("help"):
      help_text=_("""I am admin reaction bot.
  1. help - this help
  2. add_signature - add signature to user
  3. enable_signature - enable/disable showing signature for user
  4. show_signature - show signature for user
  5. add_rule_interruption - increment rule interruption
  6. show_rule_interruption_stat - show active/all rule interruption count for user
  6. show_active_rule_interruption - show active rule interruption description (for all interruption) - be cafule with many active interruption for user - bot will spam messages
  7. clear_active_rule_interruption - clear active rule interruption count (when unban user)
  8. set_locale - change language of bot for this room
      """)
      if await matrix_api.send_text(room,help_text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True

    elif command == "set_locale" or command == _("set_locale"):
      # проверяем права доступа:
      if is_power_level_for_signature(room,event.sender) == False:
        log.warning("no power level for this")
        text="""you need more power level for this command"""
        log.warning(text)
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True

      if len(parameters) < 1:
        help_text="""This command allow switch language for this room.

  command `set_locale` need 1 param: locale. Locale can be 'ru', 'us', etc.
  syntax:

    my_botname_in_this_room: set_locale locale

  example:
    rsbot: set_locale ru
        """
        if await matrix_api.send_text(room,help_text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True
      else:
        # параметров достаточно:
        locale_name = parameters[0]
        try:
          # включаем локаль:
          lang = gettext.translation('commands', localedir='./locale', languages=[locale_name])
          lang.install()
        except:
          # ошибка включения локали:
          text="""unsupported locale name '%s'. Try 'en' or 'ru' for example."""%locale_name
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False

        if sql.set_room_setting(room.room_id, 'locale', locale_name) == False:
          log.error("sql.set_room_setting()")
          text="""internal error sql.set_room_setting()"""
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False

        # нужно обновить кэш опций:
        if update_db_bot_settings_cache(room.room_id) == False:
          log.error("update_db_bot_settings_cache()")
          return False
        return True

    elif command == "enable_signature" or command == _("enable_signature"):
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

    elif command == "add_rule_interruption" or command == _("add_rule_interruption"):
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
        help_text="""command `add_rule_interruption` need 2 params.
  syntax:

    my_botname_in_this_room: add_rule_interruption user_name_for_inc_rule_interruption "description - Why rule is interrupt"

  example:
    rsbot: add_signature Baduser "rule paragraph 3 at message url: https://matrix.to/#/!tBHU3434554VVVfuMP:matrix.org/$UV232444VR8-F9ch3eAZxlG2nUdakJXDMfYETdZVYCQ?via=matrix.org"

        """
        if await matrix_api.send_text(room,help_text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True
      else:
        # параметров достаточно:
        user_mxid = parameters[0]
        rule_interruption_descr = parameters[1]

        if user_mxid in room.users:
          # пользователь указан по MXID:
          user_mxid_mxid = user_mxid
        elif user_mxid in room.names:
          # пользователь указан по имени
          if len(room.names[user_mxid])>1:
            # несколько пользователей с одинаковыми именами:
            text="""nickname %s not uniqum in this room. Please, select user by mxid (as @user:server.com)"""%user_mxid
            log.warning(text)
            if await matrix_api.send_text(room,text) == False:
              log.error("matrix_api.send_text()")
              return False
            return True
          else:
            # пользователь указан по MXID:
            user_mxid_mxid = room.names[user_mxid][0]
        else:
          # неизвестный пользователь:
          text="""nickname %s not known. Please, correct, or select user by mxid (as @user:server.com)"""%user_mxid
          log.warning(text)
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return True
        log.debug("user_mxid_mxid = %s"%user_mxid_mxid)
        if sql.add_rule_interruption(room.room_id, user_mxid_mxid, rule_interruption_descr, event.sender) == False:
          log.error("sql.add_rule_interruption()")
          text="""internal error sql.add_rule_interruption()"""
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
        # уведомляем пользователя, что всё получилось:
        text="""success add rule_interruption to user %s"""%user_mxid_mxid
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True

    elif command == "add_signature" or command == _("add_signature"):
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

    elif command == "show_signature" or command == _("show_signature"):

      if len(parameters) < 1:
        help_text=_("""This command show signature record for user.

  command `show_signature` need 1 params.
  syntax:

    my_botname_in_this_room: show_signature user_name

  example:
    rsbot: show_signature Baduser

        """)
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
          text=_("""internal error sql.check_user_exist()""")
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
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
          text=_("""internal error sql.get_signature_descr()""")
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
        # формируем отчёт:
        text = _("""User %(signature_user_mxid)s:
  1. signature: %(signature)s
  2. Author of signature: %(signature_author)s
  3. Time create/update of signature: %(signature_time_create)s
  4. Show signature: %(signature_show)s
  5. Description signature: %(signature_descr)s
  """)%{\
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

    elif command == "show_rule_interruption_stat" or command == _("show_rule_interruption_stat"):

      if len(parameters) < 1:
        help_text=_("""This command show rule interruption stat for user.

  command `show_rule_interruption_stat` need 1 params.
  syntax:

    my_botname_in_this_room: show_rule_interruption_stat user_name

  example:
    rsbot: show_rule_interruption_stat Baduser

        """)
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
          text=_("""internal error sql.check_user_exist()""")
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
        if ret == 0:
          text = _("no such user in db: %s")%signature_user_mxid
          log.debug(text)
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False

        # получаем данные о записи:
        # активные:
        active_rule_interruption = sql.get_rule_interruption_count(room.room_id, signature_user_mxid,active=True)
        # неактивные:
        all_rule_interruption = sql.get_rule_interruption_count(room.room_id, signature_user_mxid,active=False)
        if active_rule_interruption is None or all_rule_interruption is None:
          log.error("sql.get_rule_interruption_count()")
          text=_("internal error in function: ") + "sql.get_rule_interruption_count()"
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
        # все:
        all_rule_interruption += active_rule_interruption
        # формируем отчёт:
        text = _("""User %(signature_user_mxid)s have:
  1. active rule interruption: %(active_rule_interruption)d
  2. all rule interruption: %(all_rule_interruption)d
  """)%{\
        "signature_user_mxid":signature_user_mxid,\
        "active_rule_interruption":active_rule_interruption,\
        "all_rule_interruption":all_rule_interruption\
        }
        # показываем отчёт:
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True

    elif command == "show_active_rule_interruption" or command == _("show_active_rule_interruption"):

      if len(parameters) < 1:
        help_text=_("""This command show description for active rule interruption for user.

  command `show_active_rule_interruption` need 1 params.
  syntax:

    my_botname_in_this_room: show_active_rule_interruption user_name

  example:
    rsbot: show_active_rule_interruption Baduser

        """)
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
            text=_("""nickname %s not uniqum in this room. Please, select user by mxid (as @user:server.com)""")%signature_user
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
          text=_("nickname %s not known. Please, correct, or select user by mxid (as @user:server.com)")%signature_user
          log.warning(text)
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return True
        log.debug("signature_user_mxid = %s"%signature_user_mxid)

        ret = sql.check_user_exist(room.room_id, signature_user_mxid)
        if ret is None:
          log.error("sql.check_user_exist()")
          text=_("internal error in function: ") + "sql.check_user_exist()"
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
        if ret == 0:
          text = _("no such user in db: %s")%signature_user_mxid
          log.debug(text)
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False

        # получаем данные о записи:
        # активные:
        rule_interruption_descr_list = sql.get_rule_interruption_descr(room.room_id, signature_user_mxid,active=True)
        if rule_interruption_descr_list is None:
          log.error("sql.get_rule_interruption_descr()")
          text=_("internal error in function: ") + "sql.get_rule_interruption_descr()"
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
        # формируем отчёт:
        if len(rule_interruption_descr_list)==0:
          log.info("no active rule interruptions for user %s"%signature_user_mxid)
          text=_("no active rule interruptions for user %s")%signature_user_mxid
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
        else:
          for item in rule_interruption_descr_list:
            text = _("""Admin %(admin)s at %(date)s add rule interruption by user %(signature_user_mxid)s with descr: %(descr)s""")%{\
              "admin":item[0],\
              "date":item[1],\
              "signature_user_mxid":signature_user_mxid,\
              "descr":item[2]\
              }
            # показываем отчёт:
            if await matrix_api.send_text(room,text) == False:
              log.error("matrix_api.send_text()")
              return False
        return True

    elif command == "clear_active_rule_interruption" or command == _("clear_active_rule_interruption"):
      # проверяем права доступа:
      if is_power_level_for_signature(room,event.sender) == False:
        log.warning("no power level for this")
        text="""you need more power level for this command"""
        log.warning(text)
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True

      if len(parameters) < 1:
        help_text="""This command clear active rule interruptions for user.
  They will become as not active.

  command `clear_active_rule_interruption` need 1 param.
  syntax:

    my_botname_in_this_room: clear_active_rule_interruption user_name

  example:
    rsbot: clear_active_rule_interruption Baduser

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
            text=_("nickname %s not uniqum in this room. Please, select user by mxid (as @user:server.com)")%signature_user
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
          text=_("nickname %s not known. Please, correct, or select user by mxid (as @user:server.com)")%signature_user
          log.warning(text)
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return True
        log.debug("signature_user_mxid = %s"%signature_user_mxid)

        if sql.clear_active_rule_interruption(room.room_id, signature_user_mxid) == False:
          log.error("sql.clear_active_rule_interruption()")
          text=_("internal error in function: ") + "sql.clear_active_rule_interruption()"
          if await matrix_api.send_text(room,text) == False:
            log.error("matrix_api.send_text()")
            return False
          return False
        # уведомляем пользователя, что всё получилось:
        text=_("success clear active rule interruptions for user %s")%signature_user_mxid
        if await matrix_api.send_text(room,text) == False:
          log.error("matrix_api.send_text()")
          return False
        return True

    else:
      # unknown command:
      help_text=_("""unknown command!
  Please, use 'help' or empty command (only my room nick name) for help.
      """)
      if await matrix_api.send_text(room,help_text) == False:
        log.error("matrix_api.send_text()")
        return False
      return True
  except Exception as e:
    log.error(get_exception_traceback_descr(e))
    return False
