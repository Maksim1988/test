# -*- coding: utf-8 -*-
#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from gen_py import Common
import gen_py.Exceptions.ttypes
import gen_py.Common.ttypes
import gen_py.DealsWorkerConstants.ttypes


from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class DealItemDto:
  """
  Attributes:
   - wareId
   - amount
   - price
   - addedWhen
   - excluded
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'wareId', None, None, ), # 1
    (2, TType.I32, 'amount', None, None, ), # 2
    (3, TType.STRUCT, 'price', (Common.ttypes.CurrencyAmount, Common.ttypes.CurrencyAmount.thrift_spec), None, ), # 3
    (4, TType.I64, 'addedWhen', None, None, ), # 4
    (5, TType.BOOL, 'excluded', None, None, ), # 5
  )

  def __init__(self, wareId=None, amount=None, price=None, addedWhen=None, excluded=None,):
    self.wareId = wareId
    self.amount = amount
    self.price = price
    self.addedWhen = addedWhen
    self.excluded = excluded

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.wareId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.amount = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.price = Common.ttypes.CurrencyAmount()
          self.price.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I64:
          self.addedWhen = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.BOOL:
          self.excluded = iprot.readBool();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DealItemDto')
    if self.wareId is not None:
      oprot.writeFieldBegin('wareId', TType.STRING, 1)
      oprot.writeString(self.wareId)
      oprot.writeFieldEnd()
    if self.amount is not None:
      oprot.writeFieldBegin('amount', TType.I32, 2)
      oprot.writeI32(self.amount)
      oprot.writeFieldEnd()
    if self.price is not None:
      oprot.writeFieldBegin('price', TType.STRUCT, 3)
      self.price.write(oprot)
      oprot.writeFieldEnd()
    if self.addedWhen is not None:
      oprot.writeFieldBegin('addedWhen', TType.I64, 4)
      oprot.writeI64(self.addedWhen)
      oprot.writeFieldEnd()
    if self.excluded is not None:
      oprot.writeFieldBegin('excluded', TType.BOOL, 5)
      oprot.writeBool(self.excluded)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class OfferDto:
  """
  Attributes:
   - dealId
   - offerNumber
   - owner
   - changes
   - state
   - createdWhen
   - totalPrice
   - readWhen
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'dealId', None, None, ), # 1
    (2, TType.I64, 'offerNumber', None, None, ), # 2
    (3, TType.I32, 'owner', None, None, ), # 3
    (4, TType.LIST, 'changes', (TType.STRUCT,(DealItemDto, DealItemDto.thrift_spec)), None, ), # 4
    (5, TType.I32, 'state', None, None, ), # 5
    (6, TType.I64, 'createdWhen', None, None, ), # 6
    (7, TType.STRUCT, 'totalPrice', (Common.ttypes.CurrencyAmount, Common.ttypes.CurrencyAmount.thrift_spec), None, ), # 7
    (8, TType.I64, 'readWhen', None, None, ), # 8
  )

  def __init__(self, dealId=None, offerNumber=None, owner=None, changes=None, state=None, createdWhen=None, totalPrice=None, readWhen=None,):
    self.dealId = dealId
    self.offerNumber = offerNumber
    self.owner = owner
    self.changes = changes
    self.state = state
    self.createdWhen = createdWhen
    self.totalPrice = totalPrice
    self.readWhen = readWhen

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.dealId = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I64:
          self.offerNumber = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.owner = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.LIST:
          self.changes = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = DealItemDto()
            _elem5.read(iprot)
            self.changes.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.I32:
          self.state = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.I64:
          self.createdWhen = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.STRUCT:
          self.totalPrice = Common.ttypes.CurrencyAmount()
          self.totalPrice.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.I64:
          self.readWhen = iprot.readI64();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('OfferDto')
    if self.dealId is not None:
      oprot.writeFieldBegin('dealId', TType.I64, 1)
      oprot.writeI64(self.dealId)
      oprot.writeFieldEnd()
    if self.offerNumber is not None:
      oprot.writeFieldBegin('offerNumber', TType.I64, 2)
      oprot.writeI64(self.offerNumber)
      oprot.writeFieldEnd()
    if self.owner is not None:
      oprot.writeFieldBegin('owner', TType.I32, 3)
      oprot.writeI32(self.owner)
      oprot.writeFieldEnd()
    if self.changes is not None:
      oprot.writeFieldBegin('changes', TType.LIST, 4)
      oprot.writeListBegin(TType.STRUCT, len(self.changes))
      for iter6 in self.changes:
        iter6.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.state is not None:
      oprot.writeFieldBegin('state', TType.I32, 5)
      oprot.writeI32(self.state)
      oprot.writeFieldEnd()
    if self.createdWhen is not None:
      oprot.writeFieldBegin('createdWhen', TType.I64, 6)
      oprot.writeI64(self.createdWhen)
      oprot.writeFieldEnd()
    if self.totalPrice is not None:
      oprot.writeFieldBegin('totalPrice', TType.STRUCT, 7)
      self.totalPrice.write(oprot)
      oprot.writeFieldEnd()
    if self.readWhen is not None:
      oprot.writeFieldBegin('readWhen', TType.I64, 8)
      oprot.writeI64(self.readWhen)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class DealDto:
  """
  Attributes:
   - id
   - sellerId
   - buyerId
   - number
   - items
   - totalPrice
   - state
   - lastOffer
   - createdWhen
   - updatedWhen
   - archivedWhen
   - readDeal
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'id', None, None, ), # 1
    (2, TType.I32, 'sellerId', None, None, ), # 2
    (3, TType.I32, 'buyerId', None, None, ), # 3
    (4, TType.I64, 'number', None, None, ), # 4
    (5, TType.LIST, 'items', (TType.STRUCT,(DealItemDto, DealItemDto.thrift_spec)), None, ), # 5
    None, # 6
    None, # 7
    (8, TType.STRUCT, 'totalPrice', (Common.ttypes.CurrencyAmount, Common.ttypes.CurrencyAmount.thrift_spec), None, ), # 8
    (9, TType.I32, 'state', None, None, ), # 9
    None, # 10
    (11, TType.STRUCT, 'lastOffer', (OfferDto, OfferDto.thrift_spec), None, ), # 11
    (12, TType.I64, 'createdWhen', None, None, ), # 12
    (13, TType.I64, 'updatedWhen', None, None, ), # 13
    (14, TType.I64, 'archivedWhen', None, None, ), # 14
    (15, TType.BOOL, 'readDeal', None, None, ), # 15
  )

  def __init__(self, id=None, sellerId=None, buyerId=None, number=None, items=None, totalPrice=None, state=None, lastOffer=None, createdWhen=None, updatedWhen=None, archivedWhen=None, readDeal=None,):
    self.id = id
    self.sellerId = sellerId
    self.buyerId = buyerId
    self.number = number
    self.items = items
    self.totalPrice = totalPrice
    self.state = state
    self.lastOffer = lastOffer
    self.createdWhen = createdWhen
    self.updatedWhen = updatedWhen
    self.archivedWhen = archivedWhen
    self.readDeal = readDeal

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.id = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.sellerId = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.buyerId = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I64:
          self.number = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.LIST:
          self.items = []
          (_etype10, _size7) = iprot.readListBegin()
          for _i11 in xrange(_size7):
            _elem12 = DealItemDto()
            _elem12.read(iprot)
            self.items.append(_elem12)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.STRUCT:
          self.totalPrice = Common.ttypes.CurrencyAmount()
          self.totalPrice.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.I32:
          self.state = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 11:
        if ftype == TType.STRUCT:
          self.lastOffer = OfferDto()
          self.lastOffer.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 12:
        if ftype == TType.I64:
          self.createdWhen = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 13:
        if ftype == TType.I64:
          self.updatedWhen = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 14:
        if ftype == TType.I64:
          self.archivedWhen = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 15:
        if ftype == TType.BOOL:
          self.readDeal = iprot.readBool();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DealDto')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.I64, 1)
      oprot.writeI64(self.id)
      oprot.writeFieldEnd()
    if self.sellerId is not None:
      oprot.writeFieldBegin('sellerId', TType.I32, 2)
      oprot.writeI32(self.sellerId)
      oprot.writeFieldEnd()
    if self.buyerId is not None:
      oprot.writeFieldBegin('buyerId', TType.I32, 3)
      oprot.writeI32(self.buyerId)
      oprot.writeFieldEnd()
    if self.number is not None:
      oprot.writeFieldBegin('number', TType.I64, 4)
      oprot.writeI64(self.number)
      oprot.writeFieldEnd()
    if self.items is not None:
      oprot.writeFieldBegin('items', TType.LIST, 5)
      oprot.writeListBegin(TType.STRUCT, len(self.items))
      for iter13 in self.items:
        iter13.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.totalPrice is not None:
      oprot.writeFieldBegin('totalPrice', TType.STRUCT, 8)
      self.totalPrice.write(oprot)
      oprot.writeFieldEnd()
    if self.state is not None:
      oprot.writeFieldBegin('state', TType.I32, 9)
      oprot.writeI32(self.state)
      oprot.writeFieldEnd()
    if self.lastOffer is not None:
      oprot.writeFieldBegin('lastOffer', TType.STRUCT, 11)
      self.lastOffer.write(oprot)
      oprot.writeFieldEnd()
    if self.createdWhen is not None:
      oprot.writeFieldBegin('createdWhen', TType.I64, 12)
      oprot.writeI64(self.createdWhen)
      oprot.writeFieldEnd()
    if self.updatedWhen is not None:
      oprot.writeFieldBegin('updatedWhen', TType.I64, 13)
      oprot.writeI64(self.updatedWhen)
      oprot.writeFieldEnd()
    if self.archivedWhen is not None:
      oprot.writeFieldBegin('archivedWhen', TType.I64, 14)
      oprot.writeI64(self.archivedWhen)
      oprot.writeFieldEnd()
    if self.readDeal is not None:
      oprot.writeFieldBegin('readDeal', TType.BOOL, 15)
      oprot.writeBool(self.readDeal)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class DealTotalsReport:
  """
  Attributes:
   - total
   - active
   - successful
   - cancelled
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'total', None, None, ), # 1
    (2, TType.I64, 'active', None, None, ), # 2
    (3, TType.I64, 'successful', None, None, ), # 3
    (4, TType.I64, 'cancelled', None, None, ), # 4
  )

  def __init__(self, total=None, active=None, successful=None, cancelled=None,):
    self.total = total
    self.active = active
    self.successful = successful
    self.cancelled = cancelled

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.total = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I64:
          self.active = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I64:
          self.successful = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I64:
          self.cancelled = iprot.readI64();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DealTotalsReport')
    if self.total is not None:
      oprot.writeFieldBegin('total', TType.I64, 1)
      oprot.writeI64(self.total)
      oprot.writeFieldEnd()
    if self.active is not None:
      oprot.writeFieldBegin('active', TType.I64, 2)
      oprot.writeI64(self.active)
      oprot.writeFieldEnd()
    if self.successful is not None:
      oprot.writeFieldBegin('successful', TType.I64, 3)
      oprot.writeI64(self.successful)
      oprot.writeFieldEnd()
    if self.cancelled is not None:
      oprot.writeFieldBegin('cancelled', TType.I64, 4)
      oprot.writeI64(self.cancelled)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class DealReportResponse:
  """
  Attributes:
   - sig
   - report
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'report', (DealTotalsReport, DealTotalsReport.thrift_spec), None, ), # 1
    None, # 2
    None, # 3
    None, # 4
    None, # 5
    None, # 6
    None, # 7
    None, # 8
    None, # 9
    None, # 10
    None, # 11
    None, # 12
    None, # 13
    None, # 14
    None, # 15
    None, # 16
    None, # 17
    None, # 18
    None, # 19
    None, # 20
    None, # 21
    None, # 22
    None, # 23
    None, # 24
    None, # 25
    None, # 26
    None, # 27
    None, # 28
    None, # 29
    None, # 30
    None, # 31
    None, # 32
    None, # 33
    None, # 34
    None, # 35
    None, # 36
    None, # 37
    None, # 38
    None, # 39
    None, # 40
    None, # 41
    None, # 42
    None, # 43
    None, # 44
    None, # 45
    None, # 46
    None, # 47
    None, # 48
    None, # 49
    None, # 50
    None, # 51
    None, # 52
    None, # 53
    None, # 54
    None, # 55
    None, # 56
    None, # 57
    None, # 58
    None, # 59
    None, # 60
    None, # 61
    None, # 62
    None, # 63
    None, # 64
    None, # 65
    None, # 66
    None, # 67
    None, # 68
    None, # 69
    None, # 70
    None, # 71
    None, # 72
    None, # 73
    None, # 74
    None, # 75
    None, # 76
    None, # 77
    None, # 78
    None, # 79
    None, # 80
    None, # 81
    None, # 82
    None, # 83
    None, # 84
    None, # 85
    None, # 86
    None, # 87
    None, # 88
    None, # 89
    None, # 90
    None, # 91
    None, # 92
    None, # 93
    None, # 94
    None, # 95
    None, # 96
    None, # 97
    None, # 98
    None, # 99
    None, # 100
    None, # 101
    None, # 102
    None, # 103
    None, # 104
    None, # 105
    None, # 106
    None, # 107
    None, # 108
    None, # 109
    None, # 110
    None, # 111
    None, # 112
    None, # 113
    None, # 114
    None, # 115
    None, # 116
    None, # 117
    None, # 118
    None, # 119
    None, # 120
    None, # 121
    None, # 122
    None, # 123
    None, # 124
    None, # 125
    None, # 126
    (127, TType.STRUCT, 'sig', (Common.ttypes.Signature, Common.ttypes.Signature.thrift_spec), None, ), # 127
  )

  def __init__(self, sig=None, report=None,):
    self.sig = sig
    self.report = report

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 127:
        if ftype == TType.STRUCT:
          self.sig = Common.ttypes.Signature()
          self.sig.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 1:
        if ftype == TType.STRUCT:
          self.report = DealTotalsReport()
          self.report.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DealReportResponse')
    if self.report is not None:
      oprot.writeFieldBegin('report', TType.STRUCT, 1)
      self.report.write(oprot)
      oprot.writeFieldEnd()
    if self.sig is not None:
      oprot.writeFieldBegin('sig', TType.STRUCT, 127)
      self.sig.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class DealsReportRequest:
  """
  Attributes:
   - sig
   - userId
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'userId', None, None, ), # 1
    None, # 2
    None, # 3
    None, # 4
    None, # 5
    None, # 6
    None, # 7
    None, # 8
    None, # 9
    None, # 10
    None, # 11
    None, # 12
    None, # 13
    None, # 14
    None, # 15
    None, # 16
    None, # 17
    None, # 18
    None, # 19
    None, # 20
    None, # 21
    None, # 22
    None, # 23
    None, # 24
    None, # 25
    None, # 26
    None, # 27
    None, # 28
    None, # 29
    None, # 30
    None, # 31
    None, # 32
    None, # 33
    None, # 34
    None, # 35
    None, # 36
    None, # 37
    None, # 38
    None, # 39
    None, # 40
    None, # 41
    None, # 42
    None, # 43
    None, # 44
    None, # 45
    None, # 46
    None, # 47
    None, # 48
    None, # 49
    None, # 50
    None, # 51
    None, # 52
    None, # 53
    None, # 54
    None, # 55
    None, # 56
    None, # 57
    None, # 58
    None, # 59
    None, # 60
    None, # 61
    None, # 62
    None, # 63
    None, # 64
    None, # 65
    None, # 66
    None, # 67
    None, # 68
    None, # 69
    None, # 70
    None, # 71
    None, # 72
    None, # 73
    None, # 74
    None, # 75
    None, # 76
    None, # 77
    None, # 78
    None, # 79
    None, # 80
    None, # 81
    None, # 82
    None, # 83
    None, # 84
    None, # 85
    None, # 86
    None, # 87
    None, # 88
    None, # 89
    None, # 90
    None, # 91
    None, # 92
    None, # 93
    None, # 94
    None, # 95
    None, # 96
    None, # 97
    None, # 98
    None, # 99
    None, # 100
    None, # 101
    None, # 102
    None, # 103
    None, # 104
    None, # 105
    None, # 106
    None, # 107
    None, # 108
    None, # 109
    None, # 110
    None, # 111
    None, # 112
    None, # 113
    None, # 114
    None, # 115
    None, # 116
    None, # 117
    None, # 118
    None, # 119
    None, # 120
    None, # 121
    None, # 122
    None, # 123
    None, # 124
    None, # 125
    None, # 126
    (127, TType.STRUCT, 'sig', (Common.ttypes.Signature, Common.ttypes.Signature.thrift_spec), None, ), # 127
  )

  def __init__(self, sig=None, userId=None,):
    self.sig = sig
    self.userId = userId

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 127:
        if ftype == TType.STRUCT:
          self.sig = Common.ttypes.Signature()
          self.sig.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 1:
        if ftype == TType.I32:
          self.userId = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DealsReportRequest')
    if self.userId is not None:
      oprot.writeFieldBegin('userId', TType.I32, 1)
      oprot.writeI32(self.userId)
      oprot.writeFieldEnd()
    if self.sig is not None:
      oprot.writeFieldBegin('sig', TType.STRUCT, 127)
      self.sig.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class DealIdRequest:
  """
  Attributes:
   - sig
   - dealId
   - userId
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'dealId', None, None, ), # 1
    (2, TType.I32, 'userId', None, None, ), # 2
    None, # 3
    None, # 4
    None, # 5
    None, # 6
    None, # 7
    None, # 8
    None, # 9
    None, # 10
    None, # 11
    None, # 12
    None, # 13
    None, # 14
    None, # 15
    None, # 16
    None, # 17
    None, # 18
    None, # 19
    None, # 20
    None, # 21
    None, # 22
    None, # 23
    None, # 24
    None, # 25
    None, # 26
    None, # 27
    None, # 28
    None, # 29
    None, # 30
    None, # 31
    None, # 32
    None, # 33
    None, # 34
    None, # 35
    None, # 36
    None, # 37
    None, # 38
    None, # 39
    None, # 40
    None, # 41
    None, # 42
    None, # 43
    None, # 44
    None, # 45
    None, # 46
    None, # 47
    None, # 48
    None, # 49
    None, # 50
    None, # 51
    None, # 52
    None, # 53
    None, # 54
    None, # 55
    None, # 56
    None, # 57
    None, # 58
    None, # 59
    None, # 60
    None, # 61
    None, # 62
    None, # 63
    None, # 64
    None, # 65
    None, # 66
    None, # 67
    None, # 68
    None, # 69
    None, # 70
    None, # 71
    None, # 72
    None, # 73
    None, # 74
    None, # 75
    None, # 76
    None, # 77
    None, # 78
    None, # 79
    None, # 80
    None, # 81
    None, # 82
    None, # 83
    None, # 84
    None, # 85
    None, # 86
    None, # 87
    None, # 88
    None, # 89
    None, # 90
    None, # 91
    None, # 92
    None, # 93
    None, # 94
    None, # 95
    None, # 96
    None, # 97
    None, # 98
    None, # 99
    None, # 100
    None, # 101
    None, # 102
    None, # 103
    None, # 104
    None, # 105
    None, # 106
    None, # 107
    None, # 108
    None, # 109
    None, # 110
    None, # 111
    None, # 112
    None, # 113
    None, # 114
    None, # 115
    None, # 116
    None, # 117
    None, # 118
    None, # 119
    None, # 120
    None, # 121
    None, # 122
    None, # 123
    None, # 124
    None, # 125
    None, # 126
    (127, TType.STRUCT, 'sig', (Common.ttypes.Signature, Common.ttypes.Signature.thrift_spec), None, ), # 127
  )

  def __init__(self, sig=None, dealId=None, userId=None,):
    self.sig = sig
    self.dealId = dealId
    self.userId = userId

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 127:
        if ftype == TType.STRUCT:
          self.sig = Common.ttypes.Signature()
          self.sig.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 1:
        if ftype == TType.I64:
          self.dealId = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.userId = iprot.readI32();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('DealIdRequest')
    if self.dealId is not None:
      oprot.writeFieldBegin('dealId', TType.I64, 1)
      oprot.writeI64(self.dealId)
      oprot.writeFieldEnd()
    if self.userId is not None:
      oprot.writeFieldBegin('userId', TType.I32, 2)
      oprot.writeI32(self.userId)
      oprot.writeFieldEnd()
    if self.sig is not None:
      oprot.writeFieldBegin('sig', TType.STRUCT, 127)
      self.sig.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
