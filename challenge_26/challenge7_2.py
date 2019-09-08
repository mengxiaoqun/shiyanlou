# -*- coding:utf-8 -*-
import pandas as pd

def co2_gdp_plot():
    df_climate = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    data = df_climate[df_climate['Series code'] == 'EN.ATM.CO2E.KT'].set_index('Country code')
    data.drop(data.columns[[0,1,2,3,4]],axis=1,inplace=True)
    data.replace({'..':pd.np.NaN},inplace=True)
    data = data.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    data.fillna(0,inplace=True)
    data['Sum co2'] = data.sum(axis=1)
    data_co2 = data['Sum co2']

    data = df_climate[df_climate['Series code'] == 'NY.GDP.MKTP.CD'].set_index('Country code')
    data.drop(data.columns[[0,1,2,3,4]],axis=1,inplace=True)
    data.replace({'..':pd.np.NaN},inplace=True)
    data = data.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    data.fillna(0,inplace=True)
    data['Sum gdp'] = data.sum(axis=1)
    data_gdp = data['Sum gdp']

    df_climate = pd.concat([data_co2,data_gdp],axis=1)



    fig = plt.subplot()
    china = []
    return fig,china



