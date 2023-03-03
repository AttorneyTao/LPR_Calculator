# SPDX-FileCopyrightText: 2023 Tao Ye <taoye1992@163e.com>
#
# SPDX-License-Identifier: MIT

import pandas as pd

def parse_config(config_dict:dict):
    """
     Replace 360 and 365 with 360 and 365. This is to make it easier to read the config file
     
     @param config_dict - dictionary of config values to replace
     
     @return new dictionary with replacements for 360 and 365 in order to work with json. loads ( config_dict
    """
    REPLACE_DICT={
        "360天":360,
        "365天":365
    }
    # Replaces all values in REPLACE_DICT with the given key in REPLACE_DICT.
    for key,value in REPLACE_DICT.items():
        # Set the value of the key in the config_dict
        for key2,value2 in config_dict.items():
            # Set the value of config_dict key2 to value2 if value2 is key
            if value2 == key:
                config_dict[key2]=value
    return config_dict

def read_config(src: str = r'config\config.xlsx'):
    """
     Read configuration from excel file. This function is used to read 
     
     the configuration from a excel file. If you want to read the configuration from a file that is not in the excel format use : func : ` read_config_from_excel `
     
     @param src - path to the excel file
     
     @return a dictionary with the configuration as keys and the values as values. Example :. >>> import paddle. v1beta1 as v >>> config = paddle. read_config ('config. xlsx '
    """
    config = pd.read_excel(src)
    config_dict = {}
    # Set the config dictionary to the config dictionary
    for paras in config['paras_list']:
        config_dict[paras] = config[paras][0]
    config_dict = parse_config(config_dict)
    return config_dict



def read_lpr(src: str = r'data\lpr_data.xlsx'):
    """
     Read LPR data from an Excel file. This is a wrapper around pandas. 
     
     read_excel that does not support reading a column of data.
     
     @param src - path to the excel file to read. Default is r'data \ lpr_data. xlsx '
     
     @return a dataframe with the data from the file. Each row corresponds to a line in the file. Example :
    """
    lpr_df = pd.read_excel(src)
    return lpr_df

def read_data(src: str =r'data\data.xlsx'):
    """
     Read data from an Excel file. This is a wrapper around pandas.
      
     read_excel that does not support reading multiple rows at once
     
     @param src - path to the excel file
     
     @return a dataframe with the data from the excel file as the first column and the data as the second column
    """
    data_df = pd.read_excel(src)
    return data_df

def init():
    """
     Initialize the LPR and data. This is called by the program's 
     
     main loop to get the configuration and lpr from the command line
          
     @return A tuple containing the configuration the list of log levels and the
    """
    """return config,lpr,data"""
    data=read_data()
    lpr=read_lpr()
    config=read_config()
    return config,lpr,data