# SPDX-FileCopyrightText: 2023 Tao Ye <taoye1992@163e.com>
#
# SPDX-License-Identifier: MIT
import pandas as pd
import numpy as np
from typing import Iterable

class entry:
    def __init__(self,name,amount,start_date,end_date,interest = 0,process = None) -> None:
        """
         Initialize the data object. This is the method that will be called by the constructor
         
         @param name - The name of the transaction
         @param amount - The amount of the transaction in cents.
         @param start_date - The start date of the transaction.
         @param end_date - The end date of the transaction.
         @param interest - The interest of the transaction. Default is 0.
         @param process - The process that is associated with the transaction.
         
         @return The instance of the class with the data populated. If you don't want to create a transaction you can pass None
        """
        self.name = name
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
        self.interest = interest
        self.process = pd.DataFrame({'金额':[],
                                         '起始日':[],
                                         '截止日':[],
                                         '计息天数':[],
                                         '利率':[],
                                         '利息金额':[]})
    


    def calc_elapse(self,lpr_df: pd.DataFrame):
        """
         Calculate lapse between episodes in the past. This is based on the number of episodes in the past and the difference between the episodes in the past.
         
         @param lpr_df - dataframe of LPR data.
         
         @return a dataframe with elapse in days. It's a pandas
        """
        temp_df = lpr_df.drop(index = 0,inplace = False)
        temp_df = temp_df.reset_index()
        temp_df.loc[len(temp_df)] = temp_df.loc[len(temp_df)-1]
        lpr_df['elapse'] = 0
        lpr_df['elapse'] = temp_df['日期']-lpr_df['日期']
        lpr_df.drop(lpr_df.tail(1).index,inplace=True)
        #因最后一天要包含在计算中，所以最后一行的日期间隔需要加1
        lpr_df.loc[len(lpr_df)-1,'elapse'] += np.timedelta64(1,'D')
        lpr_df['elapse_int'] = lpr_df['elapse'].astype('str').apply(lambda x:x[:-5]).astype('int32')
        return lpr_df
    
    def decorate(self,calc_df,config):
        """
         Decorate dataframes to be used in calculation. This is a method to be called by : meth : ` ~calc_generator `.
         
         @param calc_df - pandas DataFrame with data to be decorated
         @param config - dict with LPR configuration. See
         
         @return a pandas DataFrame with decorated data for calculation. It is assumed that the columns are in the same order as
        """
        self.process['起始日'] = calc_df['日期'].astype('datetime64[D]')
        self.process['计息天数'] = calc_df['elapse']
        self.process['截止日'] = (self.process['起始日']+self.process['计息天数']-np.timedelta64(1,'D')).astype('datetime64[D]')
        self.process['利率'] = calc_df[config['LPR类型']]
        self.process['利息金额'] = calc_df['interest']
        self.process['金额'] = self.amount
        self.process.loc[len(self.process)] = ['合计',0,0,0,0,self.interest]
        return self.process


    def calculate(self,config,lpr: pd.DataFrame):
        """
         Calculate LPR and store in database. @param config Configuration of the calculation.
         
         @param config
         @param lpr - Data frame of LPR.
         
         @return result of calculation and store in database. @return result
        """
        calc_df = lpr[(lpr['日期']>self.start_date)&(lpr['日期']<self.end_date)]
        start_rate_1y = lpr.loc[max(calc_df.index[0]-1,0)]['1年期']
        start_rate_5y = lpr.loc[max(calc_df.index[0]-1,0)]['5年期']
        temp_row = pd.DataFrame({'日期':[self.start_date],
                                 '1年期':[start_rate_1y],
                                 '5年期':[start_rate_5y]})
        calc_df = pd.concat([temp_row,calc_df])
        calc_df = calc_df.reset_index().drop(columns = 'index')
        calc_df.loc[len(calc_df)] = {'日期':self.end_date,
                                    '1年期':calc_df.iloc[len(calc_df)-1]['1年期'],
                                    '5年期':calc_df.iloc[len(calc_df)-1]['5年期']}
        calc_df = self.calc_elapse(calc_df)
        calc_df['interest'] = self.amount*calc_df[config['LPR类型']]/100/config['一年为']*calc_df['elapse_int']
        calc_df['interest'] = calc_df['interest'].round(2)
        self.interest = calc_df['interest'].sum()
        self.decorate(calc_df,config)
        return self.process

        
class wrapper:
    def __init__(self,entries : Iterable) -> None:
        """
         Initialize the class with data. This is the method that will be called by __init
         
         @param entries - An iterable of : class : ` pylearn2. data. Process `
         
         @return None if success otherwise
        """
        self.dic={'款项名称':[],
                  '金额':[],
                  '起息日':[],
                  '截止日':[],
                  '利息合计':[]}
        self.processes=[]
        # This method is used to generate the dic
        for i in range(0, len(entries)):
            self.dic['款项名称'].append(entries[i].name)
            self.dic['金额'].append(entries[i].amount)
            self.dic['起息日'].append(entries[i].start_date)
            self.dic['截止日'].append(entries[i].end_date)
            self.dic['利息合计'].append(entries[i].interest)
            self.processes.append(entries[i].process)
        self.aggr_df=pd.DataFrame(self.dic)
        return 
            