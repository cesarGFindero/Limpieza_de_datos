# *****************************
# Aqui se preparan los archivos csv. eliminando fechas u horas incorrectas
# Tambien se pueden elegir filas especificas para eliminar
#*******************************

import pandas as pd
import os
import pdb
import graficas as gd

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
        

def leer_y_preparar(filename,saltos,inicio,formato_fecha):
    restar = 10
    eliminar = 500
    fecha_mal = 0
    dia_mal = 0
    hora_mal = 0

    df = pd.read_csv(filename, skiprows=saltos, error_bad_lines=False, warn_bad_lines=True, encoding='latin1', engine='python')
    
    if 'COM' in filename:
        for column in df.columns:
            if 'I' in column:
               df.drop(column, axis=1, inplace=True)
                    
        i = 1
        while df.shape[1] <= 14:
            if f'L{i}' not in df.columns:
                df[f'L{i}'] = 0
            i += 1
        del i
    
    
    df.dropna(inplace=True)
    filas_inicial = df.shape[0]
    df = df[~df['Date'].str.contains("2165")] # Por un error, el findero coloca fechas en el año 2165 y 2158
    df = df[~df['Date'].str.contains("2158")]
    fecha_mal = filas_inicial-df.shape[0]
    df = df[~df['Date'].str.contains("00")] # Por un error, algunas fechas tienen día 00
    df = df[~df['Date'].str.contains("45")] # Por un error, algunas fechas tienen día 45
    dia_mal = filas_inicial-df.shape[0] + fecha_mal
    df = df[~df['Time'].str.contains("62")] # Por un error, algunas fechas tienen hora 62
    hora_mal = filas_inicial-df.shape[0] + dia_mal + fecha_mal
    
           
            
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
    
    
    eliminados = filas_inicial - df.shape[0]
    
    df.drop(df.tail(eliminar).index,inplace=True)
    df.reset_index(drop=True, inplace = True)

    
    for puerto in range(1,13):
        df[f'L{puerto}'] = df[f'L{puerto}'] - restar
        df[f'L{puerto}'].clip(lower=0, inplace=True)

    if df.shape[1]>15:
        for i in range(15,df.shape[1]):
            df.drop(df.columns[15], axis=1, inplace = True)
    return df, eliminados, fecha_mal, dia_mal, hora_mal


def limpiar(cliente,mes,inicio):
    formato_fecha = '%d-%m-%Y'
    carpeta_in = f'D:/01 Findero/{mes}/{cliente}/Datos/Original'
    carpeta_out = f'D:/01 Findero/{mes}/{cliente}/Datos'
    
    finderos = os.listdir(carpeta_in)
    finderos = [item for item in finderos if '.CSV' in item[-4:] or '.csv' in item[-4:]]
    saltos = list(range(1,500))
    
    for i, archivo in enumerate(finderos):
        filename = f'{carpeta_in}/{archivo}'
        filename_out = f'{carpeta_out}/{archivo}'
        print()
        print(f'{archivo}')
        print()
        try:
            df, eliminados, fecha_mal, dia_mal, hora_mal = leer_y_preparar(filename,saltos,inicio,formato_fecha)
            df.to_csv(filename_out,index=False)
            print()
            print(f'Se limpió el archivo, se eliminaron {eliminados} filas.')
            print()
            if fecha_mal != 0:
                print(f'{fecha_mal} filas con fecha incorrecta.')
            if dia_mal != 0:
                print(f'{dia_mal} filas con día incorrecto.')
            if hora_mal != 0:
                print(f'{hora_mal} filas con hora incorrecta.')
            
        except Exception as error:
            print(f'Error al limpiar el archivo {archivo}')
            print(str(error))
            
        try:
            gd.graficas_dinamicas(cliente,mes,archivo,df) 
            print()
            print(f'Se produjeron las gráficas dinámicas.')
            print()
            print('-----------------------------------------------')
        except Exception as error:
            print()
            print(f'Error al producir las gráficas del archivo {archivo}')
            print(str(error))
            
    
    

if __name__=="__main__":
    cliente = '99 Martin Urrutia'
    mes='08 Agosto'
    inicio = None
    limpiar(cliente,mes,inicio)