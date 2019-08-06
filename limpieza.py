# *****************************
# Aqui se preparan los archivos csv. eliminando fechas u horas incorrectas
# Tambien se pueden elegir filas especificas para eliminar
#*******************************

import pandas as pd
import os
import pdb


def quitar_anteriores(df,inicio,formato_fecha):
    df = df.loc[pd.to_datetime(df['Date'], format=formato_fecha) >= pd.to_datetime(inicio, format=formato_fecha)]
    return df

def limpieza_lineas(df):
   
    for col in range(12):
        df.reset_index(inplace=True,drop=True)
        for index, item in enumerate(df[f'L{col+1}']):
            try:
                float(item)
            except:
                df.drop(index,inplace=True)
        df[f'L{col+1}'] = df[f'L{col+1}'].astype('float')
        print(f'L{col+1} listo')
    
    return df
        

def leer_y_preparar(filename,saltos,inicio,restar,formato_fecha):
    eliminar = 900
    fecha_mal = 0
    dia_mal = 0
    hora_mal = 0

    df = pd.read_csv(filename, skiprows=saltos, error_bad_lines=False, warn_bad_lines=True, encoding='latin1', engine='python')
    
    if 'COM' in filename:
        for i in range (1,4):
            a_drop = 'I'+str(i)
            try:
                df.drop([a_drop], axis=1, inplace=True)
            except:
                pass
        
        if df.shape[1] == 5:        
            for i in range (4,13):
                a_input = 'L'+str(i)
                df[a_input] = 0
        else:
            for i in range (5,13):
                a_input = 'L'+str(i)
                df[a_input] = 0
    
    df.dropna(inplace=True)
#    df = limpieza_lineas(df)
    e1 = df.shape[0]
    df = df[~df['Date'].str.contains("2165")] # Por un error, el findero coloca fechas en el año 2165 y 2158
    df = df[~df['Date'].str.contains("2158")]
    fecha_mal = e1-df.shape[0]
    df = df[~df['Date'].str.contains("00")] # Por un error, algunas fechas tienen día 00
    df = df[~df['Date'].str.contains("45")] # Por un error, algunas fechas tienen día 45
    dia_mal = e1-df.shape[0] + fecha_mal
    df = df[~df['Time'].str.contains("62")] # Por un error, algunas fechas tienen hora 62
    hora_mal = e1-df.shape[0] + dia_mal + fecha_mal
    
    
#    df.reset_index(inplace=True,drop=True)
#    for index, date in enumerate(df['Date']):
#        try:
#            pd.to_datetime(date, format=formato_fecha)
#        except:
#            df.drop(index,inplace=True)
#            print(index)
            
            
    if pd.to_datetime(df['Date'], format=formato_fecha, errors='coerce').notnull().all() == False:
        if pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce').notnull().all() == True:
            df['Date'] = df['Date'].str.replace('/','-')
        elif pd.to_datetime(df['Date'], format='%d/%m/%y', errors='coerce').notnull().all() == True:
            df['Date'] = df['Date'].str.replace('/','-')
            for i in range(1,13):
                df['Date'] = df['Date'].str.replace(str(i),'0'+str(i))
            df['Date'] = df['Date'].str.replace('0109','2019')
        else:
            print('El formato de fecha original es incorrecto')
            
            
    if inicio != None:
        df = quitar_anteriores(df,inicio,formato_fecha)
    
    df.fillna(0,inplace = True)
    df.reset_index(drop=True, inplace = True)
    e2 = df.shape[0]
    eliminados = e1 - e2
    
    df.drop(df.head(eliminar).index,inplace=True)
    df.drop(df.tail(eliminar).index,inplace=True)
    df.reset_index(drop=True, inplace = True)
#    pdb.set_trace()
    for puerto in range(1,13):
        df[f'L{puerto}'] = df[f'L{puerto}'] - restar
        df[f'L{puerto}'].clip(lower=0, inplace=True)
#    pdb.set_trace()
    if df.shape[1]>15:
        for i in range(15,df.shape[1]):
            df.drop(df.columns[15], axis=1, inplace = True)
    return df, eliminados, fecha_mal, dia_mal, hora_mal

def limpiar(cliente,mes,inicio):
    restar = 10
    formato_fecha = '%d-%m-%Y'
    carpeta_in = f'D:/01 Findero/{mes}/{cliente}/Datos/Original'
    carpeta_out = f'D:/01 Findero/{mes}/{cliente}/Datos'
    
    finderos = os.listdir(carpeta_in)
    finderos = [item for item in finderos if '.CSV' in item[-4:] or '.csv' in item[-4:]]
    saltar = [list(range(1,200)) for i in range(len(finderos))]
    
    for i in range(0,len(finderos)):
#        pdb.set_trace()
        archivo  = finderos[i]
        filename = f'{carpeta_in}/{archivo}'
        filename_out = f'{carpeta_out}/{archivo}'
        saltos = saltar[i]
        try:
            df, eliminados, fecha_mal, dia_mal, hora_mal = leer_y_preparar(filename,saltos,inicio,restar,formato_fecha)
            df.to_csv(filename_out,index=False)
            print()
            print(f'Se limpió el archivo {archivo}, se eliminaron {eliminados} filas.')
            print()
            if fecha_mal != 0:
                print(f'{fecha_mal} filas con fecha incorrecta.')
            if dia_mal != 0:
                print(f'{dia_mal} filas con día incorrecto.')
            if hora_mal != 0:
                print(f'{hora_mal} filas con hora incorrecta.')
            print('-----------------------------------------------')
        except Exception as e:
            print(f'Error al limpiar el archivo {archivo}')
            print(str(e))
    
    



if __name__=="__main__":
    cliente = '22 Veronica Avalos'
    mes='07 Julio'
    inicio = None
    limpiar(cliente,mes,inicio)