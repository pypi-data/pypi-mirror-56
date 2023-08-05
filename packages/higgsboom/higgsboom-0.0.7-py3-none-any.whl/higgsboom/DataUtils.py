# -*- coding: utf-8 -*-
import sqlalchemy
import numpy as np
import pandas as pd
from .DataBaseUtils import *

#将列表拆分成长度尽可能平均的子列表
def Chunks(arr, m):
	n = int(np.ceil(len(arr) / float(m)))
	return [arr[i:i + n] for i in range(0, len(arr), n)]

def TimeOfDayToSecondsCount(todStr):
	todParts = todStr.split(":")
	return 3600*int(todParts[0]) + 60*int(todParts[1]) + int(todParts[2])

def TickOfSecond(millisec):
	if millisec < 500:
		return 0
	else:
		return 1

def T2TimeStampToTickLabel(todStr, millisec):
	return 2*TimeOfDayToSecondsCount(todStr) + TickOfSecond(millisec)

def VolumeWeighedPrice(bidPrice1, bidVolume1, askPrice1, askVolume1):
	return (bidPrice1*askVolume1 + askPrice1*bidVolume1)/(bidVolume1 + askVolume1)

class FuturesDataUtils(object):
	def __init__(self, dataEngine):
		self.dataEngine = dataEngine
		self.dbUtils = DataBaseUtils()
		print('HiggsBoom: initializing data engine for %s' % self.dataEngine)
		self.dbUtils.InitDataEngine(dataEngine)
		self.isLevel2 = True if ('-l2-' in self.dataEngine) else False
		self.dataTables = list()
		inspector = sqlalchemy.inspect(self.dbUtils.conns[dataEngine])
		for tableName in inspector.get_table_names():
			if len(tableName) > 9 and len(tableName) < 12 and IsValidDate(tableName[-8:]):
				self.dataTables.append(tableName)
		self.dataColumns = list()
		for col in inspector.get_columns(self.dataTables[0]):
			self.dataColumns.append(col['name'])
		self.idField = None
		self.volumeField = None
		print('Data Table Structure for %s:' % self.dataEngine, self.dataColumns)
		for col in self.dataColumns:
			if col.replace('_', '').lower() in ['instrumentid', 'contractid', 'instrument', 'contract']:
				self.idField = col
			if col.replace('_', '').lower() in ['volume', 'matchtotqty']:
				self.volumeField = col

	def GetFuturesTickData(self, instrument, tradingDate):
		try:
			instrumentId = ""
			productId = ""
			tableName = ""
			selectSql = ""
			if '_V' in instrument:
				parts = instrument.split('_V')
				productId = parts[0]
				priority = int(parts[1])
				instrumentId = self.ProductInstrumentListWithVolumePriority(productId, tradingDate)[priority]
			else:
				instrumentId = instrument
				productId = ProductIdFromInstrumentId(instrument)
			if not '-l2-' in self.dataEngine:
				tableName = "%s_%s" % (productId, tradingDate)
				selectSql = "SELECT * FROM %s WHERE %s='%s' AND settle_date=local_date" % (tableName, self.idField, instrumentId)
			else:
				tableName = "md%s" % tradingDate
				selectSql = "SELECT * FROM %s WHERE %s='%s'" % (tableName, self.idField, instrumentId)
			return pd.DataFrame(self.dbUtils.GetSqlResultForDataEngine(self.dataEngine, selectSql), columns=self.dataColumns)
		except:
			print("error, failed to get tick data for %s on %s" % (instrument, tradingDate))

	def TradingDateList(self, productId):
		tdList = list()
		if not self.isLevel2:
			for table in self.dataTables:
				if table.startswith(productId) and IsValidDate(table[-8:]):
					tdList.append(table[-8:])
		else:
			for table in self.dataTables:
				tdList.append(table[-8:])
		tdList.sort()
		return tdList

	def ProductInstrumentListWithVolumePriority(self, productId, tradingDate):
		tdList = self.TradingDateList(productId)
		#tradingDateListCheck, currently not available
		try:
			tdIdx = tdList.index(tradingDate)
			if tdIdx == 0:
				print('error, %s is the first available trading date for %s, cannot automatically determine instrument priority' % (tradingDate, product))
				return
			ydList = self.VolumeSortedInstruments(productId, tradingDate)
			instList = self.ProductInstrumentList(productId, tradingDate)
			diff = list(set(instList).difference(set(ydList)))
			if len(diff) == 0:
				return ydList
			return list(set(ydList).intersection(set(instList))) + diff
		except:
			print('error, %s not in current trading date list!' % tradingDate)
			return

	def ProductInstrumentList(self, productId, tradingDate):
		if not '-l2-' in self.dataEngine:
			sql = "SELECT %s AS Instrument FROM %s_%s GROUP BY Instrument" % (self.idField, productId, tradingDate)
		else:
			sql = "SELECT %s AS Instrument FROM md%s WHERE %s LIKE '%s" % (self.idField, tradingDate, self.idField, productId) + "%' GROUP BY Instrument"
		instrumentList = [item[0] for item in self.dbUtils.GetSqlResultForDataEngine(self.dataEngine, sql)]
		instrumentList.sort()
		return instrumentList

	def VolumeSortedInstruments(self, productId, tradingDate):
		if not '-l2-' in self.dataEngine:
			sql = "SELECT %s AS Instrument, MAX(%s) AS TotalVolume FROM %s_%s WHERE settle_date=local_date GROUP BY Instrument ORDER BY TotalVolume DESC" % (self.idField, self.volumeField, productId, tradingDate)
		else:
			sql = "SELECT %s AS Instrument, MAX(%s) AS TotalVolume FROM md%s WHERE %s LIKE '%s" % (self.idField, self.volumeField, tradingDate, self.idField, productId) + "%' GROUP BY Instrument ORDER BY TotalVolume DESC"
		return [item[0] for item in self.dbUtils.GetSqlResultForDataEngine(self.dataEngine, sql)]


def StockIDToTableName(stockId):
	parts = stockId.split(".")
	return parts[1] +  parts[0]

class StockDataUtils(object):
	def __init__(self):
		self.dbUtils = DataBaseUtils()
		print('HiggsBoom: initializing stock data engine')
		self.dbUtils.InitDataEngine('astock-daily')
		self.stockDailyColumns = [col['name'] for col in sqlalchemy.inspect(self.dbUtils.conns['astock-daily']).get_columns('sz000001')]
		self.dailyDataColumns = [col['name'] for col in sqlalchemy.inspect(self.dbUtils.conns['astock-daily']).get_columns('daily20081006')]
		self.dbUtils.InitDataEngine('astock-minute')
		self.stockMinuteColumns = [col['name'] for col in sqlalchemy.inspect(self.dbUtils.conns['astock-minute']).get_columns('sz000001')]

	def StockList(self, tradingDate=''):
		stockList = list()
		if tradingDate == '':
			allTables = sqlalchemy.inspect(self.dbUtils.conns['astock-daily']).get_table_names()
			for table in allTables:
				if len(table) == 8 and (table.startswith('sh') or table.startswith('sz')):
					stockList.append('%s.%s' % (table[2:], table[0:2].upper()))
		else:
			stockList = list(self.TradingDateDailyFrame(tradingDate)['STOCK_ID'])
		stockList.sort()
		return stockList

	def StockDailyDataFrame(self, stockId, startDate='', endDate=''):
		df = pd.DataFrame(self.dbUtils.GetSqlResultForDataEngine('astock-daily', "SELECT * FROM %s" % StockIDToTableName(stockId).lower()), columns=self.stockDailyColumns)
		if startDate:
			df = df[df['TRADING_DATE'] >= datetime.datetime.strptime(startDate.replace('-',''), '%Y%m%d').date()]
		if endDate:
			df = df[df['TRADING_DATE'] <= datetime.datetime.strptime(endDate.replace('-',''), '%Y%m%d').date()]
		df = df.reset_index(drop=True)
		return df

	def StockMinuteDataFrame(self, stockId, startDate='', endDate=''):
		df = pd.DataFrame(self.dbUtils.GetSqlResultForDataEngine('astock-minute', "SELECT * FROM %s" % StockIDToTableName(stockId).lower()), columns=self.stockMinuteColumns)
		if startDate:
			df = df[df['DATE_TIME'] >= datetime.datetime.strptime(startDate.replace('-',''), '%Y%m%d')]
		if endDate:
			df = df[df['DATE_TIME'] <= datetime.datetime.strptime(endDate.replace('-',''), '%Y%m%d') + datetime.timedelta(days=1)]
		df = df.reset_index(drop=True)
		return df

	def TradingDateDailyFrame(self, tradingDate):
		return pd.DataFrame(self.dbUtils.GetSqlResultForDataEngine('astock-daily', "SELECT * FROM daily%s" % tradingDate.replace('-', '')), columns=self.dailyDataColumns)

	def TradingDateList(self, dataSet='daily', stockId='000001.SZ'):
		tdList = list()
		if dataSet.startswith('min'):
			tdList = list(set(list(self.StockMinuteDataFrame(stockId)['DATE_TIME'].apply(lambda x:x.strftime('%Y-%m-%d')))))
		else:
			tdList = list(self.StockDailyDataFrame(stockId)['TRADING_DATE'].apply(lambda x:x.strftime('%Y-%m-%d')))
		tdList.sort()
		return tdList


			
