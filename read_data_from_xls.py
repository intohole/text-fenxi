#coding=utf-8




from b2 import system2
import xlrd


system2.reload_utf8()

xls = xlrd.open_workbook("texts/成都女司机data_3.xlsx")
for booksheet in xls.sheets():
    for row in xrange(booksheet.nrows):
        print booksheet.cell(row, booksheet.ncols - 1).value
