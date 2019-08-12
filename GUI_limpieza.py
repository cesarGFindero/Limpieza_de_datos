#*********************
# Interfaz para hacer la limpieza de datos
# usando el acomodo de clases y objetos
#*********************

import tkinter as tk

import os
from datetime import datetime
import limpieza as li
from functools import partial
import graficas as gr

class Ventana(tk.Tk):
    
    def __init__(self, master):
        tk.Tk.__init__(self, master)
        self.master = master
        self.title("Limpieza de Datos")
        self.iconbitmap('favicon.ico')
        self.geometry('500x400+600+200')
        self.resizable(0,0)
        menu = tk.Menu(self)
        self.config(menu=menu)
        
        subMenu = tk.Menu(menu,tearoff=False)
        menu.add_cascade(label = 'Archivo', menu = subMenu)
        subMenu.add_command(label = 'Cerrar', command=self.cerrar)
        
        self.mainWidgets()
        
       
    def mainWidgets(self):
        self.cuerpo = Cuerpo(self)
        self.cuerpo.grid(row=0, column=0)

        
#        self.mensajes = Mensajes(self)
#        self.mensajes.grid(row=3, column=0,columnspan = 3, sticky=tk.W)
        
    
    def cerrar(self):
        self.destroy()


class Cuerpo(tk.Frame):
    
    carpeta_in = 'D:/01 Findero'
    meses_lista = {1:'01 Enero',2:'02 Febrero',3:'03 Marzo',
                   4:'04 Abril',5:'05 Mayo',6:'06 Junio',
                   7:'07 Julio',8:'08 Agosto',9:'09 Septiembre',
                   10:'10 Octubre',11:'11 Noviembre',12:'12 Diciembre', 13:'Otros proyectos'}
    
    def __init__(self, master):
        tk.Frame.__init__(self,master)
        self.master = master
        self.widgets()        

    def widgets(self):
        
        self.tk_mes = tk.StringVar()
        self.tk_mes.set(self.meses_lista[datetime.now().month])
        self.tk_cliente = tk.StringVar()
        
        self.label_encabezado = tk.Label(self,  text = '         Limpieza de datos',
                                         font='Helvetica 18 bold' )
        self.label_encabezado.grid(row=1, column=1, columnspan = 2)
        
        self.label_mes = tk.Label(self, text ='Mes:')
        self.label_mes.grid(row=3, column=1, padx=20, pady=20, sticky=tk.E)
        
        self.label_cliente = tk.Label(self, text = 'Cliente:')
        self.label_cliente.grid(row=4, column=1, padx=20, pady=20, sticky=tk.E)
        
        self.meses = {m for m in os.listdir(self.carpeta_in) if m in self.meses_lista.values()}
        
        self.mes_desplegable = tk.OptionMenu(self, self.tk_mes, *self.meses)
        self.mes_desplegable.config(width=20)
        self.mes_desplegable.grid(row=3,column=2)
        
        self.clientes = os.listdir(self.carpeta_in+'/'+ self.tk_mes.get())
        self.tk_cliente.set(self.clientes[-1])
        self.tk_mes.trace('w',self.update)
        
        self.cliente_desplegable = tk.OptionMenu(self, self.tk_cliente, *self.clientes)
        self.cliente_desplegable.config(width=20)
        self.cliente_desplegable.grid(row=4,column=2)
        
        self.label_fecha = tk.Label(self, text='Instalación:')
        self.label_fecha.grid(row=5, column=1, padx=20, pady=20, sticky=tk.E)
        
        self.entrada_fecha = None
        self.entrada_fecha = tk.Entry(self)
        self.entrada_fecha.grid(row=5,column=2)
        
       
        self.boton_enviar = tk.Button(self, text = 'Limpiar Datos', command=self.enviar)
        self.boton_enviar.grid(row=7, column=1, columnspan = 2, ipadx=15)
        
        self.grid_rowconfigure(0, minsize=20)
        self.grid_rowconfigure(2, minsize=20)
        self.grid_rowconfigure(6, minsize=20)
        
        self.grid_columnconfigure(0, minsize=55)
        
    def enviar(self):
        
        if self.entrada_fecha.get():
            fecha=self.entrada_fecha.get()
        else:
            fecha=None
            
        li.limpiar(self.tk_cliente.get(),self.tk_mes.get(),fecha)
        
#        gr.graficas(self.tk_cliente.get(),self.tk_mes.get())
        
        print(f'Se terminaron de limpiar los datos de {self.tk_cliente.get()[3:]}')

        
    def update(self, *args):
        client = os.listdir(self.carpeta_in+'/'+ self.tk_mes.get())
        try:
            self.tk_cliente.set(client[-1])
        except:
            self.tk_cliente.set('')
        
        menu = self.cliente_desplegable['menu']
        menu.delete(0,'end')

        for name in client:
            menu.add_command(label=name, command=lambda nuevo=name: self.tk_cliente.set(nuevo))
                 
        
                
    

        

limpieza = Ventana(None)

limpieza.mainloop()