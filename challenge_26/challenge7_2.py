# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt


def co2_gdp_plot():
    df_climate = pd.read_excel('ClimateChange.xlsx',sheet_name=0)
    data = df_climate[df_climate['Series code'] == 'EN.ATM.CO2E.KT'].set_index('Country code')
    data.drop(data.columns[[0,1,2,3,4]],axis=1,inplace=True)
    data.replace({'..':pd.np.NaN},inplace=True)
    data = data.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    data.fillna(0,inplace=True)
    data['co2'] = data.sum(axis=1)
    data_co2 = data['co2']

    data = df_climate[df_climate['Series code'] == 'NY.GDP.MKTP.CD'].set_index('Country code')
    data.drop(data.columns[[0,1,2,3,4]],axis=1,inplace=True)
    data.replace({'..':pd.np.NaN},inplace=True)
    data = data.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    data.fillna(0,inplace=True)
    data['gdp'] = data.sum(axis=1)
    data_gdp = data['gdp']

    df_climate = pd.concat([data_co2,data_gdp],axis=1)    
    df_norm = (df_climate - df_climate.min()) / (df_climate.max() - df_climate.min())

    china = ["{:.3f}".format(df_norm.loc['CHN'].co2),"{:.3f}".format(df_norm.loc['CHN'].gdp)]
    print(china)


    country_names = ['CHN','USA','GBR','FRA','RUS']
    positions = []
    countrys = []

    for i,val in enumerate(list(df_norm.index)):
        for country in country_names:
            if val == country:
                countrys.append(country)
                positions.append(i)

    
    fig,ax = plt.subplots()
    x = df_norm.index
    y1 = df_norm.co2
    y2 = df_norm.gdp
    ax.plot(x,y1,label='CO2-SUM')
    ax.plot(x,y2,label='GDP-SUM')
    ax.set_title('GDP-CO2')
    ax.set_xlabel('Countries')
    ax.set_ylabel('Values')
    plt.xticks(positions,countrys)
    plt.legend()
    plt.show()
    
    

    return fig,china

if __name__ == '__main__':
    co2_gdp_plot()



