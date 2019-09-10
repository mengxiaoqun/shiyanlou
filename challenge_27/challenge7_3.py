import pandas as pd
import matplotlib.pyplot as plt

def get_data():

    excel_data  = pd.read_excel('ClimateChange.xlsx')
    data = excel_data[excel_data['Series code'].isin(['EN.ATM.CO2E.KT','EN.ATM.METH.KT.CE','EN.ATM.NOXE.KT.CE','EN.ATM.GHGO.KT.CE','EN.CLC.GHGR.MT.CE'])]
    data = data.drop(['Country code','Country name','Series code','Series name','SCALE','Decimals',2011],axis=1)
    data.replace({'..':pd.np.NaN},inplace=True)
    data = data.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    data.dropna(how='all',inplace=True)
    data_climate = data.apply(lambda x: x.sum())
    data_climate.index = pd.to_datetime(data_climate.index,format='%Y')

    excel_data = pd.read_excel('GlobalTemperature.xlsx')
    data = excel_data.set_index(pd.to_datetime(excel_data['Date']))
    data = data.drop(['Date','Land Max Temperature','Land Min Temperature'],axis=1)
    data_a = data.resample('A').mean()
    data_q = data.resample('Q').mean()
    data_temperature = data_a['1990-12':'2010-12']

    data_merge = pd.concat([data_temperature.reset_index(),data_climate.reset_index()],axis=1)
    data_merge.index = data_merge['index']
    data_merge.drop(['Date','index'],axis=1,inplace=True)
    data_merge.columns = ['Total GHG','Land Max Temperature','Land And Ocean Average Temperature']
    df_norm = (data_merge - data_merge.min()) / (data_merge.max() - data_merge.min())

    return [df_norm,data_q]


def climate_plot():

    df_norm = get_data()[0]
    data_q = get_data()[1]

    fig,ax = plt.subplots(2,2)
    ax1 = df_norm.plot(kind='line',ax=ax[0,0])
    ax2 = df_norm.plot(kind='bar',ax=ax[0,1])
    ax3 = data_q.plot(kind='area',ax=ax[1,0])
    ax4 = data_q.plot(kind='kde',ax=ax[1,1])
    ax1.set_xlabel('Years') 
    ax1.set_ylabel('Values')
    ax2.set_xlabel('Years') 
    ax2.set_ylabel('Values')
    ax3.set_xlabel('Quarters') 
    ax3.set_ylabel('Temperature')
    ax4.set_xlabel('Quarters')
    ax4.set_ylabel('Temperature')
    plt.show()

    return fig
    
    
if __name__ == '__main__':
    climate_plot()

