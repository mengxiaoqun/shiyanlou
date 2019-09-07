# -*- coding:utf-8 -*-

import pandas as pd

def co2():

#1读取data表。筛选数据并设置index索引。删除多余行。替换无效数据为缺失值
#自动填充缺失值并删除整行都为空的数据。

    df_data = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    df_data = df_data[df_data['Series code'] == 'EN.ATM.CO2E.KT'].set_index('Country code')
    df_data.drop(df_data.columns[[0,1,2,3,4]],axis=1,inplace=True)
    df_data.replace({'..':pd.np.NaN},inplace=True)
    df_data = df_data.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df_data.dropna(how='all',inplace=True)
    df_data['Sum emissions'] = df_data.sum(axis=1)
    df_data = df_data['Sum emissions']
   
    
    df_country = pd.read_excel('ClimateChange.xlsx',sheetname='Country').set_index('Country code')
    df_country.drop(df_country.columns[[1,2,4]],axis=1,inplace=True)
    

    df_climate = pd.concat([df_data,df_country],axis=1,join='inner')
   
    sum_climate = df_climate[['Sum emissions','Income group']].groupby('Income group').sum()
    highest_climate = df_climate.sort_values('Sum emissions',ascending=False).groupby('Income group',as_index=False).first().set_index('Income group')
    highest_climate.columns = ['Highest emissions','Highest emission country']
    lowest_climate = df_climate.sort_values('Sum emissions',ascending=True).groupby('Income group',as_index=False).first().set_index('Income group')
    lowest_climate.columns = ['Lowest emissions','Lowest emission country']
    results = pd.concat([sum_climate,highest_climate,lowest_climate],axis=1)
    print(results)
    return results



if __name__ == '__main__':
    co2()
