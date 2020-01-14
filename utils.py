import json
import pandas as pd
import numpy as np
from collections import defaultdict


# takes dataframe and returns sum of `col` column over `window` hour intervals
# (assumes `timestamp` col exists in df)
def hour_summed(df, col, window=2):
    summary = []
    final_ts = df['timestamp'].iloc[-1]
    ts_stops = list(np.arange(0, int(np.floor(final_ts))+window, window))
    # iterate over pairs in the list
    for min_ts, max_ts in zip(ts_stops, ts_stops[1:]):
        # sum col entries for timestamps in the range
        rowbits = (df['timestamp'] >= min_ts) & (df['timestamp'] <= max_ts)
        if np.sum(rowbits) == 0:
            q = 0
        else:
            # how many clicks/impressions/etc. were served in the interval
            q = max(0, df[rowbits][col].iloc[-1] - df[rowbits][col].iloc[0])
        summary.append(q)

    return np.array(summary), np.array(ts_stops[1:])




def get_err(p, N, Zval=2.576):
    ul = (p + Zval**2/(2*N)+Zval*np.sqrt((p*(1-p)/N + Zval**2/(4*N**2))))/(1+Zval**2/N)
    ll = (p + Zval**2/(2*N)-Zval*np.sqrt((p*(1-p)/N + Zval**2/(4*N**2))))/(1+Zval**2/N)
    return [[-ll+p], [ul-p]]


# def load_file(fname):
#     data = []
#     for line in open(fname, 'r'):
#         temp = defaultdict(int)
#         t = json.loads(line.strip())
#         temp.update(t)
#         data.append([temp['query_time'], temp['reach'], temp['impressions'],\
#         temp['clicks'], temp['unique_clicks'], temp['ctr'], temp['spend']])

#     data = pd.DataFrame(data, columns=['timestamp', 'reach', 'impressions',
#         'clicks', 'unique_clicks', 'ctr', 'spend'])
#     data['timestamp'] = pd.to_datetime(data['timestamp'])
#     data['timestamp'] = ((data['timestamp']-data['timestamp'][0])).astype('int64')
#     data['timestamp'] = data['timestamp']/3600000000000
#     data['reach'] = data['reach'].astype('int64')
#     data['impressions'] = data['impressions'].astype('int64')
#     data['clicks'] = data['clicks'].astype('int64')
#     data['unique_clicks'] = data['unique_clicks'].astype('int64')
#     data['ctr'] = data['ctr'].astype('float64')
#     data['spend'] = data['spend'].astype('float64')

#     return data

# pulls out attribute every `mins` minutes; can also specify a cutoff maximum timestamp (max_ts)
def interval_vals(df, col, mins, max_ts=None):
    interval = mins/60
    vals = []
    ts_stops = []
    if not max_ts:
        max_ts = float(df['timestamp'].iloc[-1])
    ts = 0
    while True:
        if ts >= max_ts:
            break
        ind = np.where(df['timestamp'] >= ts)[0][0]
        vals.append(df[col].iloc[ind])
        ts_stops.append(df['timestamp'].iloc[ind])
        ts += interval

    return np.array(vals), np.array(ts_stops)

# returns the timestamp where campaign reached 50 clicks
def clicks_50(df_men, df_women):
    tc = df_men['clicks'] + df_women['clicks']
    ind_50 = np.where(tc >= 50)
    if len(ind_50) > 0:
        ind_50 = ind_50[0][0]

    # return the timestamp, not the index
    return df_men['timestamp'].iloc[ind_50]

# smoothing function Piotr made, putting here for reference
def momentary(series, timestamps, period=1):
    res = []
    for idx in range(0, timestamps.shape[0]):
        ii = np.argmin(np.abs(timestamps - (timestamps.iloc[idx]-period)))
        res.append(max(series.iloc[idx] - series.iloc[ii], 0))
    return np.array(res)
