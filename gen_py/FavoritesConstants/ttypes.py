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


class FavoriteType:
  USER = 1
  WARE = 2

  _VALUES_TO_NAMES = {
    1: "USER",
    2: "WARE",
  }

  _NAMES_TO_VALUES = {
    "USER": 1,
    "WARE": 2,
  }

