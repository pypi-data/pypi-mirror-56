import pandas as pd
import numpy as np
from scipy.stats.contingency import expected_freq


def dist_frequenza(matrice, colonna, save=False, tipo="categoriale", lista_ordinale=False):
    '''
    matrice: passare un dataframe di pandas
    colonna: indicare la colonna su cui effettuare la distribuzione di frequenza
    save: [False oppure nome del file] scegli se salvare o meno la tabella in excel
    tipo:
        "categoriale": classi non ordinate
        "ordinale": classi ordinate
        "cardinale": valori numerici
    lista_ordinale: una lista di valori attraverso il cui ordinare il risultato del tipo ordinale
    '''

    frequenza = matrice[colonna].value_counts(dropna=False)
    percentuale = matrice[colonna].value_counts(normalize=True, dropna=False) * 100
    distribuzione = pd.concat([frequenza, percentuale], axis=1)
    distribuzione.columns = ["Frequenze", "Percentuale"]
    if tipo == "categoriale":
        pass
    elif tipo == "ordinale":
        try:
            distribuzione = distribuzione.reindex(lista_ordinale)
            distribuzione = distribuzione.fillna(0)
            distribuzione["Cumulata"] = distribuzione["Percentuale"].cumsum()

            # distribuzione["cumsum"] = distribuzione[colonna].cumsum()
        except:
            try:
                distribuzione = distribuzione.loc[lista_ordinale]
                distribuzione = distribuzione.fillna(0)
                distribuzione["Cumulata"] = distribuzione["Percentuale"].cumsum()

            except:
                print("errore, non corrispondenza con le categorie")


    elif tipo == "cardinale":
        distribuzione.sort_index(inplace=True)

        try:
            distribuzione["Cumulata"] = distribuzione["Percentuale"].cumsum()

        except:
            print("errore nella rimozione dell'incrocio Totale - Cumulata")

    distribuzione.loc["Totale"] = distribuzione.apply(sum)

    distribuzione["Percentuale"] = distribuzione["Percentuale"].round(2)
    try:
        # distribuzione["Cumulata"] = distribuzione["Cumulata"].round(2)
        if tipo == "cardinale" or tipo == "ordinale":
            distribuzione.loc["Totale", "Cumulata"] = ""
    except:
        pass

    if save == False:
        return distribuzione
    else:
        distribuzione.to_excel(str(save) + ".xlsx")
        return distribuzione


def estrai_valore(cella):
    try:
        return int(cella[0])
    except:
        return cella


def tabella_di_contingenza(dataframe, colonna_A, colonna_B, ordine_A=False, ordine_B=False, informativo=False,
                           norm_axis=False):
    '''
    dataframe: inserire la tabella su cui si vuole fare la tabulazione incrociata
    colonna_A: inserire la stringa di testo che rappresenta l'intestazione della singola colonna
    colonna_B: inserire la stringa di testo che rappresenta l'intestazione della singola colonna
    ordine_A: inserire una lista di valori rappresentativi dell'ordine delle categorie della colonna A
    ordine_B: inserire una lista di valori rappresentativi dell'ordine delle categorie della colonna B
    iformativo: True, permette di avere in una stessa tabella frequenze, frequenze attese e scarti.
    '''
    # qui aggiuntere tabella con scarti e percentuale.
    # qui andrebbero inserite anche le percentuali di riga
    crosstab = pd.crosstab(dataframe[colonna_A], dataframe[colonna_B], margins=True)
    # normalize : boolean, {‘all’, ‘index’, ‘columns’}

    if ordine_A != False:
        crosstab = crosstab.reindex(ordine_A, axis=0)
    if ordine_B != False:
        crosstab = crosstab.reindex(ordine_B, axis=1)
    if informativo == True:
        expected = pd.DataFrame(expected_freq(crosstab), index=crosstab.index, columns=crosstab.columns)
        crosstab_norm_all = pd.crosstab(dataframe[colonna_A], dataframe[colonna_B], margins=True,
                                        normalize="all").applymap(lambda x: ("( {:.2f})".format(x)))
        crosstab_norm_index = pd.crosstab(dataframe[colonna_A], dataframe[colonna_B], margins=True,
                                          normalize="index").applymap(lambda x: ("( {:.2f})".format(x)))
        crosstab_norm_columns = pd.crosstab(dataframe[colonna_A], dataframe[colonna_B], margins=True,
                                            normalize="columns").applymap(lambda x: ("( {:.2f})".format(x)))
        if norm_axis == False:
            crosstab = crosstab.applymap(str) + " " + expected.applymap(lambda x: ("( {:.2f})".format(x))) + " " + (
            crosstab - expected).applymap(lambda x: ("( {:.2f})".format(x))) + " " + crosstab_norm_all
        if norm_axis == "index":
            crosstab = crosstab.applymap(str) + " " + expected.applymap(lambda x: ("( {:.2f})".format(x))) + " " + (
            crosstab - expected).applymap(lambda x: ("( {:.2f})".format(x))) + " " + crosstab_norm_index
        if norm_axis == "columns":
            crosstab = crosstab.applymap(str) + " " + expected.applymap(lambda x: ("( {:.2f})".format(x))) + " " + (
            crosstab - expected).applymap(lambda x: ("( {:.2f})".format(x))) + " " + crosstab_norm_columns

    return crosstab


def plot_dist_frequenza(distribuzione, tipo="categoriale", Y="Percentuale", x_label="Valori", y_label="Percentuale",
                        figsize=(12, 8), missing=None):
    '''
    distribuzione: inserire risultato della funzione dist_frequenza
    tipo:
        "categoriale": classi non ordinate
        "ordinale": classi ordinate
        "cardinale": valori numerici
    x_label: etichetta asse x
    y_label: etichetta_asse y
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    if tipo == "categoriale":
        p_color = 'muted'
    elif tipo == "ordinale":
        p_color = "Blues_d"
    elif tipo == "cardinale":
        p_color = "Blues_d"
        print("------------------------------------------------------------------------------")
        print(
            "si consiglia di utilizzare una diversa visualizzazione: cerca sul motore di ricerca sns.distplot ed applicalo sulla matrice dati originaria ")
        print("------------------------------------------------------------------------------")
    distribuzione = distribuzione.iloc[:-1, :]

    if missing != None:
        distribuzione = distribuzione.drop(missing)

    fig, ax = plt.subplots(figsize=figsize)
    x = 0

    # distribuzione.index = distribuzione.index.map(lambda x: str(x))
    g = sns.barplot(x=distribuzione.index, y=Y, data=distribuzione, ax=ax, palette=p_color, order=distribuzione.index)
    for index, row in distribuzione.iterrows():
        stringa = "N.{},\n {}%".format(row.Frequenze, row.Percentuale)
        g.text(x, row[Y] - row[Y] * 0.50, stringa, color="black", ha="center")
        x = x + 1
    g.set_xticklabels(g.get_xticklabels(), rotation=90)
    g.set(xlabel=x_label, ylabel=y_label)
    return g


def recode_da_dizionario(x, dizionario, nan=False, totale=True):
    '''
    da applicare ad un vettore o ad una matrice dati tramite la funzione map, applymap
    x: il valore da ricodificare
    dizionario: il dizionario da cui estrarre i valori di recodifica E.G.
                              {1: "sinistra",
                              2: "centro sinistra",
                              3: "centro",
                              4: "centro destra",
                              5: "destra"}
    nan: True, ricodifica i valori non presenti dentro il dizionario in nan
    totale: se True non ricodifica la modalità "Totale" generata automaticamente da dist_frequenza in nan

    '''
    try:
        return dizionario[x]
    except:
        if x == "Totale" and totale == True:
            return x
        elif nan == True:
            return np.nan
        else:
            return x