# ***************
# Como parte del proceso de limpieza, se creean las gráficas dinámicas y se guardan
# ***************

import pdb
import plotly as py
import plotly.graph_objs as go
import pandas as pd
import os

    
def graficas_dinamicas(cliente,mes,findero,df):
    carpeta_out = f'D:/01 Findero/{mes}/{cliente}/Graficas'   
    frecuencia_graficacion = 5
    if not os.path.exists(carpeta_out):
        os.mkdir(carpeta_out)
        
    carpeta_out_findero = f'{carpeta_out}/{findero[8:-4]}'
    
    if not os.path.exists(carpeta_out_findero):
        os.mkdir(carpeta_out_findero)
    
    df['Datetime'] = pd.to_datetime(df['Date']+' '+df['Time'], format='%d-%m-%Y  %H:%M:%S')
        
    for columna in df.columns:
        
        if 'Date' in columna or 'Time' in columna or 'Datetime' in columna or 'Milis' in columna :
            continue
            
        puerto = f'Puerto {columna[1:]}'
        y_data = df[columna].values
        
        x_data = df['Datetime']-pd.Timedelta('0 days 0:00:00')
        
        layout = go.Layout(
                title = puerto +'  '+ findero[8:-4],
                yaxis = dict(
                        title = 'Potencia'
                        ),
                xaxis = dict(
                        title = 'Fecha y hora'
                        )
                )
                
        trace1 = go.Scattergl(
                        x = x_data[::frecuencia_graficacion],
                        y = y_data[::frecuencia_graficacion],
                        mode = 'lines',
                        line = dict(
                                color  = 'rgb(0,0,0)',
                                shape = 'linear',
                                width = 2,   
                                )
                        )
        fig = go.Figure(data = [trace1] ,layout=layout)
        py.offline.plot(fig, filename = f'{carpeta_out_findero}/{puerto}.html', auto_open=False)