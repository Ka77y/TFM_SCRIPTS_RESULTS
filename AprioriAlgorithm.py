import csv

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd
from pandas.core.common import flatten

def generateRules(inputList):
    data = pd.read_csv("../rules_phase_dataset_id_21062021.csv", header=None)
    data_aux = data.drop(data.columns[0], axis=1)

    apriori_dataframe = pd.get_dummies(data_aux, prefix='Topic')

    items_together = apriori(apriori_dataframe, min_support=0.001, use_colnames=True)
    rules = association_rules(items_together,metric='confidence', min_threshold=1)
    rules.to_csv("all_rules_all_27062021.csv")

    rules_df = relatedTopics(data_aux, inputList)

    rules_resultant = rules[rules.antecedents.isin(rules_df)]
    return rules_resultant
def generateRules_withoutFilter():
    data = pd.read_csv("../rules_phase_dataset_id_21062021.csv", header=None)
    data_aux = data.drop(data.columns[0], axis=1)

    apriori_dataframe = pd.get_dummies(data_aux, prefix='Topic')

    items_together = apriori(apriori_dataframe, min_support=0.001, use_colnames=True)
    rules = association_rules(items_together,metric='confidence', min_threshold=1)
    rules.to_csv("all_rules_all_27062021.csv")
    rules_3313 = rules[rules['antecedents'] == frozenset({'Topic_69'})]

    return rules

def relatedTopics(data,inputList):
    data_aux = set(list(flatten(data[data.isin(inputList).any(axis=1)].values.tolist())))
    data_list = [('Topic_' + x).replace("\"", "\'") for x in data_aux if pd.isnull(x) == False]
    data_2517_aux = [frozenset(list(sub.split(" "))) for sub in data_list]

    return data_2517_aux

if __name__ == '__main__':
    #generateRules(['2517', '3318', '668'])
    generateRules_withoutFilter()