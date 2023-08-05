import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import AnchoredText

def gini(series):
    """Calculate the Gini coefficient of a pandas series."""
    try:
        array = series.apply(lambda x: float(x)).values
    except:
        return "all values must be integer or float"


    array = array.flatten() #all values are treated equally, arrays must be 1d
    if np.amin(array) < 0:
        array -= np.amin(array) #values cannot be negative
    array += 0.0000001 #values cannot be 0
    array = np.sort(array) #values must be sorted
    index = np.arange(1,array.shape[0]+1) #index per array element
    n = array.shape[0]#number of array elements
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))) #Gini coefficient

def Sq(frequency_table):
    series = frequency_table
    prob = series / series.sum()
    return [(prob*prob).sum(),  '{:.3f}'.format((prob*prob).sum())]

def Sq_norm(frequency_table):
    #prob = series / series.sum()
    series = frequency_table
    k=len(series)
    sq_x = Sq(series)[0]
    return [(sq_x-(1/k)) / (1-(1/k)), '{:.3f}'.format((sq_x-(1/k)) / (1-(1/k)))]

def Eq(frequency_table):
    series = frequency_table
    sq_norm_x = Sq_norm(series)
    return [(1-sq_norm_x[0]), '{:.3f}'.format((1-sq_norm_x[0]))]

def Sq_output(frequency_table):
    return {"Eq": Eq(frequency_table),
        "Sq": Sq(frequency_table),
        "Sq_Norm": Sq_norm(frequency_table)}

def frequency_table(dataframe, variable, save=False, data_type="categorical", ordinal_list=False):
    '''
    dataframe: pandas dataframe
    variable: select variable 
    save: namefile for saving table in excel
    data_type:
        "categorical": nominal values
        "ordinal": ordinal values
        "cardinal": int or float values
    ordinal_list: list of ordered value for ordinal data_type
    '''

    


    frequency = dataframe[variable].value_counts(dropna=False)
    percentual = dataframe[variable].value_counts(normalize=True, dropna=False) * 100
    distribution = pd.concat([frequency, percentual], axis=1)
    distribution.columns = ["Frequency", "%"]
    if data_type == "categorical":
        pass
    elif data_type == "ordinal":
        try:
            distribution = distribution.reindex(ordinal_list)
            distribution = distribution.fillna(0)
            distribution["Cumulate"] = distribution["%"].cumsum()
        except:
            try:
                distribution = distribution.loc[ordinal_list]
                distribution = distribution.fillna(0)
                distribution["Cumulate"] = distribution["%"].cumsum()

            except:
                print("error, categories doesn't corrispond with ordinal_list")


    elif data_type == "cardinal":
        distribution.sort_index(inplace=True)

        try:
            distribution["Cumulate"] = distribution["%"].cumsum()

        except:
            print("error with cumulate values")

    distribution.loc["Total"] = distribution.apply(sum)

    distribution["%"] = distribution["%"].round(2)
    try:
        if data_type == "cardinal" or data_type == "ordinal":
            distribution.loc["Total", "%"] = ""
            distribution.loc["Total", "Cumulate"] = ""
    except:
        pass

    if save == False:
        return distribution
    else:
        distribution.to_excel(str(save) + ".xlsx")
        return distribution

def frequency_plot(dataframe, variable, ordinal_list=False, data_type="categorical",
    Y="%", x_label="Values", y_label="%", figsize=(12, 8), missing=None):
    '''
    dataframe: pandas dataframe
    variable: select variable 
    save: namefile for saving table in excel
    data_type:
        "categorical": nominal values
        "ordinal": ordinal values
        "cardinal": int or float values
    ordinal_list: list of ordered value for ordinal data_type
    x_label: etichetta asse x
    y_label: etichetta_asse y
    '''
    
    if data_type == "categorical":
        p_color = 'muted'
    elif data_type == "ordinal":
        p_color = "Blues_d"
    elif data_type == "cardinal":
        p_color = "Blues_d"
        
    distribution = frequency_table(dataframe = dataframe,
                                    variable = variable,
                                    ordinal_list = ordinal_list,
                                    data_type = data_type)
    distribution = distribution.drop("Total")

    if missing != None:
        distribution = distribution.drop(missing)

    fig, ax = plt.subplots(figsize=figsize)
    x = 0

    # distribution.index = distribution.index.map(lambda x: str(x))
    if data_type=="categorical" or data_type=="ordinal":
        g = sns.barplot(x=distribution.index, y=Y, data=distribution, ax=ax, palette=p_color, order=distribution.index)
        for index, row in distribution.iterrows():
            stringa = "N.{},\n {}%".format(row["Frequency"], row["%"])
            g.text(x, row[Y] - row[Y] * 0.50, stringa, color="black", ha="center")
            x = x + 1
            g.set_xticklabels(g.get_xticklabels(), rotation=90)
            g.set(xlabel=x_label, ylabel=y_label)
        Sq_output_value = Sq_output(distribution["Frequency"])
        print(Sq_output_value)
        anc = AnchoredText(f"Eq: {Sq_output_value['Eq'][1]}\nSq: {Sq_output_value['Sq'][1]}\nSq_Norm: {Sq_output_value['Sq_Norm'][1]} " , loc="upper left", frameon=False)
        ax.add_artist(anc)
    elif data_type=="cardinal":
        gini_value = str(gini(dataframe[variable]).round(4))
        mean = str(dataframe[variable].mean().round(4))
        std = str(dataframe[variable].std().round(4))
        anc = AnchoredText(f"gini = {gini_value}\nmean = {mean}\nstd = {std}", loc="upper left", frameon=False)
        
        #anc_b = AnchoredText(f , loc="lower left", frameon=False)
        if dataframe.shape[0] < 15:
            g = sns.distplot(dataframe[variable], kde=True, rug=True, ax=ax, bins=5)
            ax.add_artist(anc)
            #ax.add_artist(anc_b)
        else:
            g = sns.distplot(dataframe[variable], kde=True, rug=True, ax=ax)
            ax.add_artist(anc)
            #ax.add_artist(anc_b)
    return g


   


if __name__ == "__main__":

    #### TESTING ####
    data = pd.DataFrame({
        "sex": ["M", "F", "M", "F", "F"],
        "Height": [190,165,178, 176, 167],
        "Education": ["Primary", "Secondary", "Primary", "Secondary", "Tertiary"],
        "income" : [1000, 870, 860, 965, 760]
    })

    print("test frequency table categorical")
    print(frequency_table(data, "sex"))
    print("test frequency plot categorical")
    frequency_plot(data, "sex")
    plt.show()
    print("test frequency table ordinal")
    print(frequency_table(data, "Education", data_type = "ordinal", ordinal_list=["Primary", "Secondary", "Tertiary"]))
    print("test frequency plot ordinal")
    frequency_plot(data, "Education", data_type = "ordinal", ordinal_list=["Primary", "Secondary", "Tertiary"])
    plt.show()
    print("test frequency table cardinal")
    print(frequency_table(data, "income", data_type = "cardinal"))
    print("test frequency plot ordinal")
    
    
    frequency_plot(data, "income", data_type = "cardinal")
    plt.show() 
    print(Sq_output(frequency_table(data, "sex")["Frequency"]))