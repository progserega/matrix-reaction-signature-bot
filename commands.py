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

async def proccess_commands(room,event,command):
  global config
  global client
  global log
  log.debug("start function")

  log.debug("command in room %s: %s"%(room.room_id, command))

