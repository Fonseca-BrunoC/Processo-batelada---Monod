from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.button import MDRectangleFlatButton
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
#import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution
from scipy.integrate import odeint
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import os
import openpyxl
import pandas as pd
import shutil
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ResultDialog(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p = Main().model()
        mimax = str(round(self.p[0], 5))
        ks = str(round(self.p[1], 5))
        yxs = str(round(self.p[2], 5))
        kd = str(round(self.p[3], 5))
        alfa = str(round(self.p[4], 5))
        beta = str(round(self.p[5], 5))
        Table = MDDataTable(size_hint= (1, 0.3),
                            pos_hint= {'center_x':0.8, 'center_y':0.8},
                            column_data= [("Mimax", dp(20)), ("Ks", dp(20)), ("Yxs", dp(20)),
                                          ("Kd", dp(20)), ("Alfa", dp(20)), ("Beta", dp(20)),],
                            row_data= [(f"{mimax}", f"{ks}", f"{yxs}", f"{kd}", f"{alfa}", f"{beta}"),
                                       ("", "", "", "", "", "")])
        tabela = self.ids.tabela
        tabela.add_widget(Table)


    cancel2 = ObjectProperty(None)

class Main(FloatLayout):
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        path_splited = path.split()
        filename2 =''
        for i in path_splited:
            filename2 = filename[0].replace(i, '')

        caminho = rf'{os.path.join(path, filename[0])}'
        destino = r'C:\Users\user\Documents\Bruno\Kivy_Estudos\Kivy_Modelagem'

        shutil.copy2(caminho,destino)
        filename2 = destino + filename2
        file_oldname = os.path.join(destino, filename2)
        file_newname_newfile = os.path.join(destino, 'Dados.xlsx')
        shutil.move(file_oldname, file_newname_newfile)

    def show_result(self):
        content2 = ResultDialog(cancel2=self.dismiss_popup)
        self._popup = Popup(title="Resultados", content=content2,
                           size_hint=(0.9, 0.9), background='lightgray', title_color=(0, 0, 0, 1))
        self._popup.open()


    def model(self):
        import modelagem
        return modelagem.result()


class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        Builder.load_file('main.kv')
        return Main()

    def on_stop(self):
        return os.remove(r'C:\Users\user\Documents\Bruno\Kivy_Estudos\Kivy_Modelagem\Dados.xlsx')

if __name__ == '__main__':
    MyApp().run()