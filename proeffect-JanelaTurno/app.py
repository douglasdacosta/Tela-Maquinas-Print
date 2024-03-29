from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from main import *
import time

App1 = App()

while True:
    time.sleep(5) #1min
    # time.sleep(600) # 10min
    # time.sleep(3600) #1h
    App.reload(App1)
