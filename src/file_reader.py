# SPDX-FileCopyrightText: 2023 Tao Ye <taoye1992@163e.com>
#
# SPDX-License-Identifier: MIT

import pandas as pd

def parse_config(config_dict:dict):
    REPLACE_DICT={
        "360天":360,
        "365天":365
    }
    for key,value in REPLACE_DICT.items():
        for key2,value2 in config_dict.items():
            if value2 == key:
                config_dict[key2]=value
    return config_dict

def read_config(src: str = r'config\config.xlsx'):
    config = pd.read_excel(src)
    config_dict = {}
    for paras in config['paras_list']:
        config_dict[paras] = config[paras][0]
    config_dict = parse_config(config_dict)
    return config_dict



def read_lpr(src: str = r'data\lpr_data.xlsx'):
    lpr_df = pd.read_excel(src)
    return lpr_df

def read_data(src: str =r'data\data.xlsx'):
    data_df = pd.read_excel(src)
    return data_df

def init():
    """return config,lpr,data"""
    data=read_data()
    lpr=read_lpr()
    config=read_config()
    return config,lpr,data