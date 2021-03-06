# -*- coding: utf-8 -*-
#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType
from gen_py import Common
import gen_py.WarehouseWorker.ttypes as WarehouseWorker
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import gen_py.WareSearchConditions.ttypes as WareSearchConditions

try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class WaresOrderDto:
  """
  Attributes:
   - criteria
   - direction
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'criteria', None, None, ), # 1
    (2, TType.I32, 'direction', None, None, ), # 2
  )

  def __init__(self, criteria=None, direction=None,):
    self.criteria = criteria
    self.direction = direction

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
        if ftype == TType.I32:
          self.criteria = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.direction = iprot.readI32();
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
    oprot.writeStructBegin('WaresOrderDto')
    if self.criteria is not None:
      oprot.writeFieldBegin('criteria', TType.I32, 1)
      oprot.writeI32(self.criteria)
      oprot.writeFieldEnd()
    if self.direction is not None:
      oprot.writeFieldBegin('direction', TType.I32, 2)
      oprot.writeI32(self.direction)
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

class SearchRequestDto:
  """
  Attributes:
   - pagination
   - ordering
   - multiOrdering
   - searchCategory
   - allowedManagementCategories
   - allowedShopIds
   - searchConditions
   - allowedModerationStates
   - allowedStockStates
   - textStringSearch
   - minimalDealTimestamp
   - minimalCreationTimestamp
   - minimalStartedDeals
   - minimalSuccessfulDeals
   - useShowcaseFilter
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'pagination', (Common.ttypes.PaginationDto, Common.ttypes.PaginationDto.thrift_spec), None, ), # 1
    (2, TType.I32, 'ordering', None, None, ), # 2
    (3, TType.I32, 'searchCategory', None, None, ), # 3
    (4, TType.SET, 'allowedManagementCategories', (TType.I32,None), None, ), # 4
    (5, TType.SET, 'allowedShopIds', (TType.I32,None), None, ), # 5
    (6, TType.LIST, 'searchConditions', (TType.STRUCT,(WareSearchConditions.WareSearchConditionsDto, WareSearchConditions.WareSearchConditionsDto.thrift_spec)), None, ), # 6
    (7, TType.SET, 'allowedModerationStates', (TType.I32,None), None, ), # 7
    (8, TType.SET, 'allowedStockStates', (TType.I32,None), None, ), # 8
    (9, TType.STRING, 'textStringSearch', None, None, ), # 9
    (10, TType.I64, 'minimalDealTimestamp', None, None, ), # 10
    (11, TType.I64, 'minimalCreationTimestamp', None, None, ), # 11
    (12, TType.I32, 'minimalStartedDeals', None, None, ), # 12
    (13, TType.I32, 'minimalSuccessfulDeals', None, None, ), # 13
    (14, TType.LIST, 'multiOrdering', (TType.STRUCT,(WaresOrderDto, WaresOrderDto.thrift_spec)), None, ), # 14
    (15, TType.BOOL, 'useShowcaseFilter', None, None, ), # 15
  )

  def __init__(self, pagination=None, ordering=None, multiOrdering=None, searchCategory=None, allowedManagementCategories=None, allowedShopIds=None, searchConditions=None, allowedModerationStates=None, allowedStockStates=None, textStringSearch=None, minimalDealTimestamp=None, minimalCreationTimestamp=None, minimalStartedDeals=None, minimalSuccessfulDeals=None, useShowcaseFilter=None,):
    self.pagination = pagination
    self.ordering = ordering
    self.multiOrdering = multiOrdering
    self.searchCategory = searchCategory
    self.allowedManagementCategories = allowedManagementCategories
    self.allowedShopIds = allowedShopIds
    self.searchConditions = searchConditions
    self.allowedModerationStates = allowedModerationStates
    self.allowedStockStates = allowedStockStates
    self.textStringSearch = textStringSearch
    self.minimalDealTimestamp = minimalDealTimestamp
    self.minimalCreationTimestamp = minimalCreationTimestamp
    self.minimalStartedDeals = minimalStartedDeals
    self.minimalSuccessfulDeals = minimalSuccessfulDeals
    self.useShowcaseFilter = useShowcaseFilter

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
        if ftype == TType.STRUCT:
          self.pagination = Common.ttypes.PaginationDto()
          self.pagination.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.ordering = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 14:
        if ftype == TType.LIST:
          self.multiOrdering = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = WaresOrderDto()
            _elem5.read(iprot)
            self.multiOrdering.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.searchCategory = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.SET:
          self.allowedManagementCategories = set()
          (_etype9, _size6) = iprot.readSetBegin()
          for _i10 in xrange(_size6):
            _elem11 = iprot.readI32();
            self.allowedManagementCategories.add(_elem11)
          iprot.readSetEnd()
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.SET:
          self.allowedShopIds = set()
          (_etype15, _size12) = iprot.readSetBegin()
          for _i16 in xrange(_size12):
            _elem17 = iprot.readI32();
            self.allowedShopIds.add(_elem17)
          iprot.readSetEnd()
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.LIST:
          self.searchConditions = []
          (_etype21, _size18) = iprot.readListBegin()
          for _i22 in xrange(_size18):
            _elem23 = WareSearchConditions.WareSearchConditionsDto()
            _elem23.read(iprot)
            self.searchConditions.append(_elem23)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.SET:
          self.allowedModerationStates = set()
          (_etype27, _size24) = iprot.readSetBegin()
          for _i28 in xrange(_size24):
            _elem29 = iprot.readI32();
            self.allowedModerationStates.add(_elem29)
          iprot.readSetEnd()
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.SET:
          self.allowedStockStates = set()
          (_etype33, _size30) = iprot.readSetBegin()
          for _i34 in xrange(_size30):
            _elem35 = iprot.readI32();
            self.allowedStockStates.add(_elem35)
          iprot.readSetEnd()
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.STRING:
          self.textStringSearch = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 10:
        if ftype == TType.I64:
          self.minimalDealTimestamp = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 11:
        if ftype == TType.I64:
          self.minimalCreationTimestamp = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 12:
        if ftype == TType.I32:
          self.minimalStartedDeals = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 13:
        if ftype == TType.I32:
          self.minimalSuccessfulDeals = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 15:
        if ftype == TType.BOOL:
          self.useShowcaseFilter = iprot.readBool();
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
    oprot.writeStructBegin('SearchRequestDto')
    if self.pagination is not None:
      oprot.writeFieldBegin('pagination', TType.STRUCT, 1)
      self.pagination.write(oprot)
      oprot.writeFieldEnd()
    if self.ordering is not None:
      oprot.writeFieldBegin('ordering', TType.I32, 2)
      oprot.writeI32(self.ordering)
      oprot.writeFieldEnd()
    if self.searchCategory is not None:
      oprot.writeFieldBegin('searchCategory', TType.I32, 3)
      oprot.writeI32(self.searchCategory)
      oprot.writeFieldEnd()
    if self.allowedManagementCategories is not None:
      oprot.writeFieldBegin('allowedManagementCategories', TType.SET, 4)
      oprot.writeSetBegin(TType.I32, len(self.allowedManagementCategories))
      for iter36 in self.allowedManagementCategories:
        oprot.writeI32(iter36)
      oprot.writeSetEnd()
      oprot.writeFieldEnd()
    if self.allowedShopIds is not None:
      oprot.writeFieldBegin('allowedShopIds', TType.SET, 5)
      oprot.writeSetBegin(TType.I32, len(self.allowedShopIds))
      for iter37 in self.allowedShopIds:
        oprot.writeI32(iter37)
      oprot.writeSetEnd()
      oprot.writeFieldEnd()
    if self.searchConditions is not None:
      oprot.writeFieldBegin('searchConditions', TType.LIST, 6)
      oprot.writeListBegin(TType.STRUCT, len(self.searchConditions))
      for iter38 in self.searchConditions:
        iter38.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.allowedModerationStates is not None:
      oprot.writeFieldBegin('allowedModerationStates', TType.SET, 7)
      oprot.writeSetBegin(TType.I32, len(self.allowedModerationStates))
      for iter39 in self.allowedModerationStates:
        oprot.writeI32(iter39)
      oprot.writeSetEnd()
      oprot.writeFieldEnd()
    if self.allowedStockStates is not None:
      oprot.writeFieldBegin('allowedStockStates', TType.SET, 8)
      oprot.writeSetBegin(TType.I32, len(self.allowedStockStates))
      for iter40 in self.allowedStockStates:
        oprot.writeI32(iter40)
      oprot.writeSetEnd()
      oprot.writeFieldEnd()
    if self.textStringSearch is not None:
      oprot.writeFieldBegin('textStringSearch', TType.STRING, 9)
      oprot.writeString(self.textStringSearch)
      oprot.writeFieldEnd()
    if self.minimalDealTimestamp is not None:
      oprot.writeFieldBegin('minimalDealTimestamp', TType.I64, 10)
      oprot.writeI64(self.minimalDealTimestamp)
      oprot.writeFieldEnd()
    if self.minimalCreationTimestamp is not None:
      oprot.writeFieldBegin('minimalCreationTimestamp', TType.I64, 11)
      oprot.writeI64(self.minimalCreationTimestamp)
      oprot.writeFieldEnd()
    if self.minimalStartedDeals is not None:
      oprot.writeFieldBegin('minimalStartedDeals', TType.I32, 12)
      oprot.writeI32(self.minimalStartedDeals)
      oprot.writeFieldEnd()
    if self.minimalSuccessfulDeals is not None:
      oprot.writeFieldBegin('minimalSuccessfulDeals', TType.I32, 13)
      oprot.writeI32(self.minimalSuccessfulDeals)
      oprot.writeFieldEnd()
    if self.multiOrdering is not None:
      oprot.writeFieldBegin('multiOrdering', TType.LIST, 14)
      oprot.writeListBegin(TType.STRUCT, len(self.multiOrdering))
      for iter41 in self.multiOrdering:
        iter41.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.useShowcaseFilter is not None:
      oprot.writeFieldBegin('useShowcaseFilter', TType.BOOL, 15)
      oprot.writeBool(self.useShowcaseFilter)
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

class WaresSearchResponseDto:
  """
  Attributes:
   - wares
   - totalCount
  """

  thrift_spec = (
    None, # 0
    (1, TType.LIST, 'wares', (TType.STRUCT,(WarehouseWorker.WareDto, WarehouseWorker.WareDto.thrift_spec)), None, ), # 1
    (2, TType.I32, 'totalCount', None, None, ), # 2
  )

  def __init__(self, wares=None, totalCount=None,):
    self.wares = wares
    self.totalCount = totalCount

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
        if ftype == TType.LIST:
          self.wares = []
          (_etype45, _size42) = iprot.readListBegin()
          for _i46 in xrange(_size42):
            _elem47 = WarehouseWorker.WareDto()
            _elem47.read(iprot)
            self.wares.append(_elem47)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.totalCount = iprot.readI32();
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
    oprot.writeStructBegin('WaresSearchResponseDto')
    if self.wares is not None:
      oprot.writeFieldBegin('wares', TType.LIST, 1)
      oprot.writeListBegin(TType.STRUCT, len(self.wares))
      for iter48 in self.wares:
        iter48.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.totalCount is not None:
      oprot.writeFieldBegin('totalCount', TType.I32, 2)
      oprot.writeI32(self.totalCount)
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

class ShowcaseRequestDto:
  """
  Attributes:
   - categoryId
   - showcaseSize
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'categoryId', None, None, ), # 1
    (2, TType.I32, 'showcaseSize', None, None, ), # 2
  )

  def __init__(self, categoryId=None, showcaseSize=None,):
    self.categoryId = categoryId
    self.showcaseSize = showcaseSize

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
        if ftype == TType.I32:
          self.categoryId = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.showcaseSize = iprot.readI32();
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
    oprot.writeStructBegin('ShowcaseRequestDto')
    if self.categoryId is not None:
      oprot.writeFieldBegin('categoryId', TType.I32, 1)
      oprot.writeI32(self.categoryId)
      oprot.writeFieldEnd()
    if self.showcaseSize is not None:
      oprot.writeFieldBegin('showcaseSize', TType.I32, 2)
      oprot.writeI32(self.showcaseSize)
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

class ShowcaseResponseDto:
  """
  Attributes:
   - categoryId
   - wares
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'categoryId', None, None, ), # 1
    (2, TType.LIST, 'wares', (TType.STRUCT,(WarehouseWorker.WareDto, WarehouseWorker.WareDto.thrift_spec)), None, ), # 2
  )

  def __init__(self, categoryId=None, wares=None,):
    self.categoryId = categoryId
    self.wares = wares

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
        if ftype == TType.I32:
          self.categoryId = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.LIST:
          self.wares = []
          (_etype52, _size49) = iprot.readListBegin()
          for _i53 in xrange(_size49):
            _elem54 = WarehouseWorker.WareDto()
            _elem54.read(iprot)
            self.wares.append(_elem54)
          iprot.readListEnd()
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
    oprot.writeStructBegin('ShowcaseResponseDto')
    if self.categoryId is not None:
      oprot.writeFieldBegin('categoryId', TType.I32, 1)
      oprot.writeI32(self.categoryId)
      oprot.writeFieldEnd()
    if self.wares is not None:
      oprot.writeFieldBegin('wares', TType.LIST, 2)
      oprot.writeListBegin(TType.STRUCT, len(self.wares))
      for iter55 in self.wares:
        iter55.write(oprot)
      oprot.writeListEnd()
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
