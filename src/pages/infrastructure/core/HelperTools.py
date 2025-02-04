import math
from typing import BinaryIO

import pandas as pd

import pickle

import time
import functools
import random
import logging
from collections import Counter, OrderedDict


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#------------------------------------------------------------------------------

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        logging.info(" ====> Duration {:.2f} secs: {}".format(run_time, func.__doc__))
        return value

    return wrapper_timer #  no "()" here, we need the object to be returned.

#------------------------------------------------------------------------------
# predicates
def is_el_filled(el, liste):
    return (el in liste) and (liste[el] is not None)

# Are there NO row duplicates?      #Types: pandas dataframe --> Boolean
validateIndex = lambda d: not any(d.duplicated(keep="first"))

#------------------------------------------------------------------------------
# Serialisierung    
@timer
def pickle_out(obj_name, datei_name):
    """Serialization"""
    p_out: BinaryIO
    with open(datei_name, "wb") as p_out:
        pickle.dump(obj_name, p_out)

@timer
def pickle_in(datei_name):
    """Deserialization"""
    with open(datei_name, "rb") as p_in:
        return pickle.load(p_in)

#------------------------------------------------------------------------------

def col_base_features(col, pattern):
    a = list(col.str.split(pat = pattern))
    return list([x[0] for x in a])


def determine_dyn_colorder(colvals, colorder_fixedpart, pdict):
    col_order = list(colvals)
    rem_list = ["Index", "ID", pdict["meta_typ"], pdict["meta_description"],"Wertebereich", "F_Aktiv", "F_PCA", "F_Szen"]
    for i in rem_list:
        try:
            col_order.remove(i)
        except ValueError:
            logging.error(f"'{i}' not found in the column order list.")



    return colorder_fixedpart + col_order


lam_split = lambda x:  x.split("$")[1]

tupToStr = lambda t: ". ".join(str(e) for e in [int(t[0]), t[1]])

# dfcn: DataFrame Col Name; zeichen: char der weg soll
#colNameRemChar = lambda x, y: x.str.replace(ch,'') for ch in list(y)

def cleanse_colnames(dfcn, zeichen):
    #dfcn ist kein Dataframe, sondern df.columns
    for v in list(zeichen):
        dfcn = dfcn.str.replace(v,'')
    return dfcn

ohlist_To_FeaturesList = lambda l: list(set([i.split("$")[0] for i in l]))
sortDictReverseOrderIntKey = \
    lambda d: sorted(list(d.items()),key=lambda x:x[0],reverse=True)

# -----------------------------------------------------------------------------
# prüfen ob "nan", "None" in liste, dictionary weg kann:
#x: list
remNanFromListFloat = lambda x: [i for i in x if str(i) != "nan"]
remNullItemsFromList = lambda x: [i for i in x if i is not None]
#d: dictionary
remNanFromDict = lambda d: {k: v for k, v in d.items() if str(v) != "nan"}
remNullItemsFromDict = lambda d: {k: v for k, v in d.items() if v is not None}

# -----------------------------------------------------------------------------
# Math: Sets
intersect = lambda x,y: list(set(x).intersection(y))

#------------------------------------------------------------------------------
# Math: Combinatorics
binom = lambda n,k: math.factorial(n) // math.factorial(k) // math.factorial(n - k)

#------------------------------------------------------------------------------
# Random generator for colors
getRandomColor = lambda _: "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

#------------------------------------------------------------------------------
# FreqCounter
def count_frequencies(arr):
    lcounter = Counter(arr)
    return OrderedDict(sorted(lcounter.items()))



#------------------------------------------------------------------------------
#Dataframe nach Reihen sortieren, neues mit neuem Index erzeugen - BEGIN
def pop_row_from_df(dframe, index_val):
    popped_row= dframe.loc[index_val, :].tolist()
    shrinked_df = dframe.drop(index_val)
    return popped_row, shrinked_df

@timer
def sort_df(dframe,col,asc):         #Pandas-df, String, Boolean
    """Sorts DataFrame"""

    df_col_list = dframe.columns.values
    result_df = pd.DataFrame(columns=df_col_list)
    while not dframe.empty:
    #for i in range(4):

        df_col = dframe[col]

        popped_stack_df_col = min(df_col) if asc == True else max(df_col)
        popped_stack_index_val = dframe \
            .index[dframe[col] == popped_stack_df_col] \
            .tolist()[0]

        #falls höchster/niedrigster Rang mehrfach vorliegt, wird der erste in Liste genommen 
        popped_row, dframe = pop_row_from_df(dframe, popped_stack_index_val[0])
        dict_row = dict(zip(df_col_list, popped_row))

        #     .append(dict_row, ignore_index = True)

        result_df = pd.concat([result_df, pd.DataFrame([dict_row])], ignore_index=True)

    return result_df

# END
#------------------------------------------------------------------------------
# Dataframes: Column name aliases (compare SQL "as")

#x: dframe, y: pdict
df_cols_assign_alias = \
    lambda x,y: x.rename(columns=dict(zip(y["scenario"], y["sc_alias"])))




