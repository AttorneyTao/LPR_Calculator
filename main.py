# SPDX-FileCopyrightText: 2023 Tao Ye <taoye1992@163e.com>
#
# SPDX-License-Identifier: MIT

#encoding:utf-8
from src.file_reader import init
from src.calculator import entry,wrapper
import copy
from pandas import ExcelWriter
#以下为配合pyinstaller导入
import openpyxl.cell._writer

# main__ is the main function to be called from the main module.
if __name__ == "__main__":
    print('reading data')
    config,lpr,data = init()
    entries=[]
    # calculates the total interest of each entry in data.
    for i in range(0,len(data)):
        calc_entry = entry(data.iloc[i]['款项名称'],
                           data.iloc[i]['金额'],
                           data.iloc[i]['起息日'],
                           data.iloc[i]['截止日'])
        calc_entry.calculate(config = config,lpr = lpr)
        entries.append(copy.copy(calc_entry))
        print(f'calculating {calc_entry.name},the total interest is {calc_entry.interest.round(2)}')
        #print(f"{entries[i].name=} {entries[i].amount=} {entries[i].process.iloc[0]['金额']=}")
    wpr = wrapper(entries)
    with ExcelWriter('res.xlsx') as writer:
        wpr.aggr_df.to_excel(writer,sheet_name='汇总表')
        # This function is used to write the entries to the excel file.
        for et in entries:
            #print(f"{et.name=} {et.amount=} {et.process.iloc[0]['金额']=}")
            et.process.to_excel(writer,sheet_name=f"{et.name}利息计算明细")