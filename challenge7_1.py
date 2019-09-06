# -*- coding:utf-8 -*-

import pandas as pd

def co2():
    c1 = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    c2 = c1[c1['Series code'] == 'EN.ATM.CO2E.KT'].set_index('Country code')
    c2.drop(c2.columns[[0,1,2,3,4]],axis=1,inplace=True)
    c2.replace({'..':pd.np.NaN},inplace=True)
    c3 = c2.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1).dropna()
    c3['Sum emissions'] = c3.sum(axis=1)
    c3.drop(c3.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]],axis=1,inplace=True)
    
    c4 = pd.read_excel('ClimateChange.xlsx',sheetname='Country').set_index('Country code')
    c4.drop(c4.columns[[1,2,4]],axis=1,inplace=True)
    c5 = pd.concat([c3,c4],axis=1).dropna()
    
    r1 = c5[['Sum emissions','Income group']].groupby('Income group').sum()
    r2 = c5.sort_values('Sum emissions',ascending=False).groupby('Income group',as_index=False).first().set_index('Income group')
    r2.columns = ['Highest emissions','Highest emission country']
    r3 = c5.sort_values('Sum emissions',ascending=True).groupby('Income group',as_index=False).first().set_index('Income group')
    r3.columns = ['Lowest emission','Lowest emission country']
    results = pd.concat([r1,r2,r3],axis=1)
    print(results)
    return results



if __name__ == '__main__':
    co2()
