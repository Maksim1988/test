# -*- coding: utf-8 -*-
#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class ContentType:
  """
   * Тип содержимого сообщения
  *
  """
  TEXT = 1
  PICTURE = 2
  DEAL = 3
  USER = 4
  WARE = 5

  _VALUES_TO_NAMES = {
    1: "TEXT",
    2: "PICTURE",
    3: "DEAL",
    4: "USER",
    5: "WARE",
  }

  _NAMES_TO_VALUES = {
    "TEXT": 1,
    "PICTURE": 2,
    "DEAL": 3,
    "USER": 4,
    "WARE": 5,
  }

class DealContentType:
  """
   * Тип сделки
  *
  """
  DEAL_OFFER = 1
  DEAL_ACCEPTION = 2
  DEAL_REJECTION = 4
  PRICE_REQUEST = 5

  _VALUES_TO_NAMES = {
    1: "DEAL_OFFER",
    2: "DEAL_ACCEPTION",
    4: "DEAL_REJECTION",
    5: "PRICE_REQUEST",
  }

  _NAMES_TO_VALUES = {
    "DEAL_OFFER": 1,
    "DEAL_ACCEPTION": 2,
    "DEAL_REJECTION": 4,
    "PRICE_REQUEST": 5,
  }

