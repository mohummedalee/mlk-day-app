import math
import json
import pandas as pd

import numpy as np
from collections import defaultdict

def pval_format(x):
    if x >= 0.05:
        return '> 0.05'
    elif 0.01 <= x < 0.05:
        return '< 0.05'
    elif 0.001 <= x < 0.01:
        return ' < 0.01'
    else:
        digits = math.floor(math.log10(1/x))
        return '10^{-%d}'%digits

def pval_format_stars(x):
    if x >= 0.05:
        return ''
    elif 0.01 <= x < 0.05:
        return '*'
    elif 0.001 <= x < 0.01:
        return '**'
    else:
        return '***'

def load_file(fname, start_timestamp=None):
    data = []
    fields = ['query_time','reach','impressions','clicks','unique_clicks','ctr','spend']
    for line in open(fname, 'r'):
        line = json.loads(line.strip())

        if type(line) == dict:
            line = [line]
        temp = defaultdict(float)
        #pdb.set_trace()
        if len(line) == 0: continue
        for elt in line:
            for f in ['reach','impressions','clicks','unique_clicks', 'spend']:
                try:
                    temp[f] += float(elt[f])
                except KeyError:
                    temp[f] = 0
        temp['query_time'] = elt['query_time']
        if temp['impressions'] == 0:
            temp['ctr'] = 0
        else:
            temp['ctr'] = temp['clicks']/temp['impressions']
        data.append([temp['query_time'], temp['reach'], temp['impressions'],\
        temp['clicks'], temp['unique_clicks'], temp['ctr'], temp['spend']])

    if len(data) == 0:
        data = np.zeros((1, len(fields)))

    data = pd.DataFrame(data, columns=['timestamp', 'reach', 'impressions',
        'clicks', 'unique_clicks', 'ctr', 'spend'])
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    if start_timestamp == None:
        start_timestamp = data['timestamp'][0]
    else:
        start_timestamp = pd.to_datetime(start_timestamp)
    data['timestamp'] = ((data['timestamp']-start_timestamp)).astype('int64')
    data['timestamp'] = data['timestamp']/3600000000000
    data['reach'] = data['reach'].astype('int64')
    data['impressions'] = data['impressions'].astype('int64')
    data['clicks'] = data['clicks'].astype('int64')
    data['unique_clicks'] = data['unique_clicks'].astype('int64')
    data['ctr'] = data['ctr'].astype('float64')
    data['spend'] = data['spend'].astype('float64')

    return data
