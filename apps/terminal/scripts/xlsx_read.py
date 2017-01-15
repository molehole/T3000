# -*- coding: utf-8 -*-

import xlrd
import datetime
import unicodecsv
import shutil
import os
from apps.terminal.models import Kolejnosc

working_dir = os.path.join('/', 'share', 'kolejnosc')
file_name = 'export.XLSX'
tury_path = os.path.join(working_dir, 'tury.csv')

def csv_from_excel(arkusz):
    wb = xlrd.open_workbook(arkusz)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(tury_path, 'wb')
    wr = unicodecsv.writer(your_csv_file, quoting=unicodecsv.QUOTE_ALL)
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()

def zapiszKolejnoscDoBazy(import_file=tury_path):
    with open(import_file, 'rb') as f:
        csvdata = unicodecsv.reader(f, delimiter=',')
        header = next(csvdata)
        for row in csvdata:
            if row:
                if not row == header:
                    if not row[11] == '0.0':
                        try:
                            seconds = (float(row[2]) - 25569) * 86400.0
                            date = datetime.datetime.utcfromtimestamp(seconds)
                            if len(row[1]) > 3:                                
                                Kolejnosc.objects.get_or_create(tura=row[1], data=date)
                        except ValueError as e:
                            break

def DodajKolejnosc():
    try:
        csv_from_excel(os.path.join(working_dir, file_name))
        zapiszKolejnoscDoBazy()
    except Exception as e:
        raise e

    archive_file = Kolejnosc.objects.last().data.isoformat() + '.XLSX'
    shutil.move(os.path.join(working_dir, file_name), os.path.join(working_dir, 'archive', archive_file))
