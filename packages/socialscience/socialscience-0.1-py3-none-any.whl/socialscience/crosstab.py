import pandas as pd
import numpy as np
from scipy.stats.contingency import expected_freq

def tabella_di_contingenza(dataframe, colonna_A, colonna_B, ordine_A = False, ordine_B = False, informativo = False, norm_axis = False):
    '''
    dataframe: inserire la tabella su cui si vuole fare la tabulazione incrociata
    colonna_A: inserire la stringa di testo che rappresenta l'intestazione della singola colonna
    colonna_B: inserire la stringa di testo che rappresenta l'intestazione della singola colonna
    ordine_A: inserire una lista di valori rappresentativi dell'ordine delle categorie della colonna A
    ordine_B: inserire una lista di valori rappresentativi dell'ordine delle categorie della colonna B
    informativo: True, permette di avere in una stessa tabella frequenze, frequenze attese e scarti. 
    '''
    
    crosstab = pd.crosstab(dataframe[colonna_A],dataframe[colonna_B], margins = True)
    
    if ordine_A != False:
        crosstab = crosstab.reindex(ordine_A, axis = 0)
    if ordine_B != False:
        crosstab = crosstab.reindex(ordine_B, axis = 1)
    if informativo == True:
        expected = pd.DataFrame(expected_freq(crosstab), index =  crosstab.index, columns = crosstab.columns)
        crosstab_norm_all = pd.crosstab(dataframe[colonna_A],dataframe[colonna_B], margins = True, normalize = "all").applymap(lambda x: ("( {:.2f})".format(x) ))
        crosstab_norm_index = pd.crosstab(dataframe[colonna_A],dataframe[colonna_B], margins = True, normalize = "index").applymap(lambda x: ("( {:.2f})".format(x) ))
        crosstab_norm_columns = pd.crosstab(dataframe[colonna_A],dataframe[colonna_B], margins = True, normalize = "columns").applymap(lambda x: ("( {:.2f})".format(x) ))
        if norm_axis == False:
            crosstab = crosstab.applymap(str) + " " + expected.applymap(lambda x: ("( {:.2f})".format(x) )) + " " + (crosstab - expected).applymap(lambda x: ("( {:.2f})".format(x) )) + " " + crosstab_norm_all
        if norm_axis == "index":
            crosstab = crosstab.applymap(str) + " " + expected.applymap(lambda x: ("( {:.2f})".format(x) )) + " " + (crosstab - expected).applymap(lambda x: ("( {:.2f})".format(x) )) + " " + crosstab_norm_index
        if norm_axis == "columns":
            crosstab = crosstab.applymap(str) + " " + expected.applymap(lambda x: ("( {:.2f})".format(x) )) + " " + (crosstab - expected).applymap(lambda x: ("( {:.2f})".format(x) )) + " " + crosstab_norm_columns
      
    return crosstab