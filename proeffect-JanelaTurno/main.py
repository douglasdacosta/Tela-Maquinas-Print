import datetime
import configparser
import requests
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from main import *
import json
import threading
import pyautogui
import os

class App(threading.Thread):    
    def __init__(self):
        threading.Thread.__init__(self)
        self.horasTrabalhadas = {}
        self.horasUsinadas = {}
        self.pbHorasUsinadas ={}
        self.pbHorasTrabalhadas = {}
        self.percentualHorasTrabalhadas = {}
        self.percentualHorasUsinadas = {}
        self.texto_turno = {}
        self.start()

    def callback(self):

        self.root.quit()

    def run(self):

        config = self.read_config('config.conf')
        
        TOKEN = config['API']['TOKEN']
        LOGIN = config['API']['LOGIN']
        SENHA = config['API']['SENHA']
        url = config['API']['endpointGetHoras']
        NUMERO_CNC = config['CONFIG']['NUMERO_CNC']


        resposta = self.consultar_horas_turno(TOKEN, LOGIN, SENHA, NUMERO_CNC, url)
        print(resposta)
        if resposta == 'erro':
            self.log_error('Erro na consulta')
            return None
        
        objeto_json = json.loads(resposta)
        texto_turno = objeto_json['turno']
        textoHorasTrabalhadas = objeto_json['textoHorasTrabalhadas']
        textoHorasUsinadas = objeto_json['textoHorasUsinadas']
        valorhorasTrabalhadasq = objeto_json['horasTrabalhadasq']
        valorHorasUsinadas = objeto_json['horasUsinadas']
        # Janela window
        Janela = tk.Tk()
        Janela.geometry('420x350')
        Janela.title('Turno')

        self.texto_turno = tk.Label(Janela, text=texto_turno, font=("Helvetica", 16))
        self.texto_turno.grid(column=0, row=0, padx=80, pady=40)
        
        self.horasTrabalhadas = tk.Label(Janela, text=textoHorasTrabalhadas)
        self.horasTrabalhadas.grid(column=0, row=1, padx=80, pady=1)

        # progressbar
        self.pbHorasTrabalhadas = ttk.Progressbar(
            Janela,
            orient='horizontal',
            mode='determinate',
            length=280
        )

        self.pbHorasTrabalhadas.grid(column=0, row=2, columnspan=1, padx=10, pady=1)
        self.pbHorasTrabalhadas['value'] = valorhorasTrabalhadasq

        valorhorasTrabalhadasq = str(valorhorasTrabalhadasq) + '%'
        self.percentualHorasTrabalhadas = tk.Label(Janela, text=valorhorasTrabalhadasq)
        self.percentualHorasTrabalhadas.grid(column=1   , row=2, columnspan=1, padx=0, pady=1)

        #Seta o percentual da progressbar

        texto = tk.Label(Janela, text='')
        texto.grid(column=0, row=3, padx=10,  pady=10, ipadx=0, ipady=0)
        self.horasUsinadas = tk.Label(Janela, text=textoHorasUsinadas)
        self.horasUsinadas.grid(column=0, row=4, padx=10,  pady=1)

        # progressbar
        self.pbHorasUsinadas = ttk.Progressbar(
            Janela,
            orient='horizontal',
            mode='determinate',
            length=280
        )

        # Orientação do  progressbar
         
        self.pbHorasUsinadas.grid(column=0, row=5, columnspan=1, padx=10, pady=1)
        self.pbHorasUsinadas['value'] = valorHorasUsinadas
         
        valorHorasUsinadas = str(valorHorasUsinadas) + '%'
        self.percentualHorasUsinadas = tk.Label(Janela, text=valorHorasUsinadas)
        self.percentualHorasUsinadas.grid(column=1, row=5, columnspan=1, padx=0, pady=1)
       
        Janela.mainloop()

    def reload(self):
        config = self.read_config('config.conf')
        TOKEN = config['API']['TOKEN']
        LOGIN = config['API']['LOGIN']
        SENHA = config['API']['SENHA']
        url = config['API']['endpointGetHoras']
        NUMERO_CNC = config['CONFIG']['NUMERO_CNC']
        
        resposta = self.consultar_horas_turno(TOKEN, LOGIN, SENHA, NUMERO_CNC, url)        
        print(resposta)
        if resposta == 'erro':
            self.log_error('Erro na consulta')
            return None
        
        objeto_json = json.loads(resposta)
        self.horasTrabalhadas['text'] = objeto_json['textoHorasTrabalhadas']
        self.horasUsinadas['text'] = objeto_json['textoHorasUsinadas']
        self.texto_turno['text'] =  objeto_json['turno']
        valorhorasTrabalhadasq = objeto_json['horasTrabalhadasq']
        valorHorasUsinadas = objeto_json['horasUsinadas']
        
        self.percentualHorasTrabalhadas['text']=valorhorasTrabalhadasq +'%'
        self.percentualHorasUsinadas['text']=valorHorasUsinadas + '%'

        self.pbHorasTrabalhadas['value'] = valorhorasTrabalhadasq
        self.pbHorasUsinadas['value'] = valorHorasUsinadas

        print(objeto_json)
        return None

    def is_before_14(self):
        hora_atual = datetime.datetime.now().time()
        meio_dia = datetime.time(14, 0)
        return hora_atual < meio_dia

    def consultar_horas_turno(self,TOKEN, LOGIN, SENHA, NUMERO_CNC, url):
        parametros = {
            'TOKEN': TOKEN,
            'LOGIN': LOGIN,
            'SENHA': SENHA,
            'NUMERO_CNC': NUMERO_CNC
        }

        try:
            resposta = requests.get(url, params=parametros)
            if resposta.status_code == 200:        
                return resposta.text
            else:            
                resposta.raise_for_status()
        except requests.exceptions.RequestException as e:        
            print("Erro durante a solicitação:", e)

    def read_config(self,config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def log_error(self,message):
        with open('error.log', 'a') as file:
            file.write(message + '\n')
