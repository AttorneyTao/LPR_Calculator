# SPDX-FileCopyrightText: 2023 Tao Ye <taoye1992@163e.com>
#
# SPDX-License-Identifier: MIT

#encoding:utf-8
from src.file_reader import init
from src.calculator import entry,wrapper
import copy
from pandas import ExcelWriter


if __name__ == "__main__":
    config,lpr,data = init()
    entries=[]
    for i in range(0,len(data)):
        calc_entry = entry(data.iloc[i]['款项名称'],
                           data.iloc[i]['金额'],
                           data.iloc[i]['起息日'],
                           data.iloc[i]['截止日'])
        calc_entry.calculate(config = config,lpr = lpr)
        entries.append(copy.copy(calc_entry))
        #print(f"{entries[i].name=} {entries[i].amount=} {entries[i].process.iloc[0]['金额']=}")
    wpr = wrapper(entries)
    with ExcelWriter('res.xlsx') as writer:
        wpr.aggr_df.to_excel(writer,sheet_name='汇总表')
        for et in entries:
            #print(f"{et.name=} {et.amount=} {et.process.iloc[0]['金额']=}")
            et.process.to_excel(writer,sheet_name=f"{et.name}利息计算明细")