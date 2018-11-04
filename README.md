# Projet Python

Projet Python - Dashboard  
Dataset regroupant tous les projets de la plateforme de financement participatif Kickstarter depuis 2009  
378661 projets avec chacun 15 variables tel que le pays, le nom du projet, le montant demandé, le montant récolté, etc.  


## Installation des packages Python

Déjà tout dans le fichier .py mais au cas où :  

import numpy as np  
import pandas as pd  
import dash  
from dash.dependencies import Input, Output  
import dash_core_components as dcc  
import dash_html_components as html  
#import iso3166  
import plotly.plotly as py  
import plotly.figure_factory as ff  
import plotly.graph_objs as go  
from plotly import __version__  
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot  
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']  


## Le script

Ouvrir une invite de commande et se placer dans le dossier du projet.
Executer kickstarter_dash.py à partir de cette invite de commande : python kickstarter_dash.py.  
Attendre que le fichier csv soit télécharger et que le dashboard soit construit.  
Quand l'invite de commande affichera :  


* Restarting with stat  
* Debugger is active!  
* Debugger PIN: 627-896-911  
* Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)  
 

Le dashboard est prêt. Copier l'addresse IP qui s'affiche et entrer la dans un navigateur.  
Ne pas fermer l'invite de commande pendant l'utilisation du dashboard
  
S'il y a besoin de recharger le csv, décommenter la ligne "#ksprojects=pd.read_csv("ks-projects-201801.csv",encoding = 'utf8')".  
Cela permet de charger directement le csv localement (ce qui va beaucoup plus vite).



