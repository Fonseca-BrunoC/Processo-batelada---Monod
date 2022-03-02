import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from scipy.integrate import odeint
import pandas as pd

#Importando os dados
df = pd.read_excel('Dados.xlsx')
data = df.to_numpy() #Covertendo os dados em np
t = data[:,0] #tempo
Cexp = data[:,1:4] #Concentrações experimentais
Ci = (Cexp[0,0], Cexp[0,1], Cexp[0,2]) #condições iniciais

#Definindo as EDO's
#Essa função será utilizada tanto para estimar os parâmetros quanto para testa-los
def edo(C, t, *args):
  mimax = args[0] #unidade 1/hora - taxa específica de crescimento
  Ks = args[1] #constante de semi-saturação
  Yxs = args[2] #coeficiente estequiométrico
  kd = args[3] #constante de morte celular
  alfa = args[4] #constante do produto associado ao crescimento
  beta = args[5] #constante do produto não associado ao crescimento

  mi = mimax * (C[1] / (Ks + C[1])) #Monod
  dCxdt = (mi - kd) * C[0] #eq para célula
  dCsdt = - (1/Yxs) * (mi - kd) * C[0] #eq para o substrato
  dCpdt = ((alfa * mi) + beta ) * C[0] #eq do produto parcialmente associado ao crescimento
  return dCxdt, dCsdt, dCpdt

#Definindo a função resíduo que será aplicada na evolução diferencial
lista = [1,1,1]
def rmse(parametros, *data):
  t, Cexp = data
  p = tuple(parametros) #Os parâmetros serão os argumentos extras da função EDO e devem estar no formato tuple
  simulacao = odeint(edo, Ci, t, args = p)
  residuo = simulacao - Cexp
  for i in range(0,3):
    residuo[:,i] = residuo[:,i] / lista[i]
  residuo = residuo.flatten()
  residuo = sum(residuo ** 2)
  return residuo

limites = [(0, 1),(0, 100),(0, 1),(0, 1),(0, 1),(0, 1)] #limites para cada um dos parâmetros
args = (t, Cexp)
novos_parametros = differential_evolution(rmse, limites, args = args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate') #aplicando a evolução diferencial
P = novos_parametros.x

def result():
    return P
