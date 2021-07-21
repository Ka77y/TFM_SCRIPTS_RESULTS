import networkx as nx
from IPython.core.display import display, HTML
import csv
import json
from Scripts.RulesAlgorithms.AprioriAlgorithm import generateRules, generateRules_withoutFilter
from pyvis.network import Network
import matplotlib.pyplot as plt

level = 0
list_capitals = []
capitals = {}
final_final_levels_list = []
general_levels_list = []
max_levels = 3
rules_associate = {}
main_rule_topics_list = []
required_levels = 2

def csv_element():
    line_count = 0
    with open(r'../../Scripts/training/rules_tender_related_topics_27052021.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')


        main_topics_list = []

        for row in csv_reader:
            list_topics = []
            if line_count == 0:
                line_count = 1
            else:
                try:
                    for x in range(0,len(row)):
                        list_topics.append(row[x].replace("[","").replace("\\","").replace("'","").replace("]","").replace("rule:","").replace(" ",""))
                    main_rule_topics_list.append(row[0].replace("[","").replace("\\","").replace("'","").replace("]","").replace("rule:","").replace(" ",""))
                except:
                    pass
                main_topics_list.append(list(set(list_topics)))
    return main_topics_list

def parseListOfObject_to_listOfLists():
    newList = []
    for i in range(0, len(list_capitals)):
        if (list_capitals[i]["level"] == level and len(list_capitals[i]["consequents"]) != 0):
            newList.append(list_capitals[i]["consequents"])
    aux_funcion(newList)

def obtain_levels_list(topics_liist):
    levels_list = []
    for topic in topics_liist:
        level_list = obtain_consequents(topic)
        if len(level_list) > 0:
            levels_list.append(list(set(level_list)))

    #para sacar consecuentes list_capitals[1]["consequents"]

def obtain_consequents(topic):
    level_list = []
    level_object = {}
    antecedent = frozenset({topic}) if 'Topic_' in topic else frozenset({'Topic_' + topic})
    level_n = rules_aux_df[rules_aux_df['antecedents'] == antecedent]
    level_n = level_n['consequents'].tolist()
    for consequent in level_n:
        print(consequent)
        for x in consequent:
            level_list.append(x)

    level_object["antecedent"] = topic
    level_object["level"] = level
    level_object["consequents"] = level_list
    capitals[topic+"_"+str(level)] = level_object
    list_capitals.append(level_object)
    return level_list

def operateListOfLists(topics_topics_list):
    global level
    level += 1
    for topics_list in topics_topics_list:
        obtain_levels_list(topics_list)
    parseListOfObject_to_listOfLists()

def aux_funcion(topics_topics_list):
    final_levels_list = []

    print(final_levels_list)
    kl = []
    kl.extend(x for x in final_levels_list if x not in kl)
    final_levels_list = list(kl)
    final_final_levels_list.extend(final_levels_list)
    if(level <= max_levels):
        operateListOfLists(topics_topics_list)
        #aux_funcion(final_levels_list, rules_aux_df)
    print("final")

    return final_final_levels_list

def buildAssociateRulesLevelBased():
    method_rules_associate = {}

    next_level_aux_list = []
    aux_list = []
    aux_keys_list = []
    key_input = ""
    method_rules_associate = buildAssociateRulesLevelBased_aux(main_topics_list, 0, key_input)
    for n in range(1, max_levels):
        aux_list = []
        aux_keys_list = []
        for key in method_rules_associate.keys():
            aux_list.append(list(set(method_rules_associate[key]["level_"+str(n)])))
            aux_keys_list.append(key)
        for j in range (0, len(aux_list)):
            key = aux_keys_list[j]
            key_consequents_list = [aux_list[j]]
            method_rules_associate[key] = buildAssociateRulesLevelBased_aux(key_consequents_list, n, key)[key]
            method_rules_associate
    method_rules_associate

def buildAssociateRulesLevelBased_aux(topics_list_input, n, key):
    rules_associate_method = {}
    rule_key = ""

    for topic_list in topics_list_input:
        list_method_aux = []
        topic_levels_object = {}
        for topic in topic_list:
            for i in range(0, len(list_capitals)):
                if (list_capitals[i]["antecedent"] == topic and len(list_capitals[i]["consequents"]) != 0):
                    list_method_aux.extend(list_capitals[i]["consequents"])
        topic_levels_object["level_"+str(n+1)] = list(set(list_method_aux))

        if key == "":
            rule_key = str(topic_list)
            rules_associate[rule_key] = topic_levels_object
        else:
            rule_key = key


        rules_associate[rule_key]["level_" + str(n + 1)] = list(set([x.replace("Topic_", "") for x in list_method_aux]))
        rules_associate_method[rule_key] = topic_levels_object
        rules_associate_method

    return rules_associate_method

def unidirectionalAssociateRules():
    for i, topics_list in enumerate(main_topics_list):
        obj_aux_method = rules_associate[str(topics_list)]
        for x in range(1, required_levels+1):
            for j in obj_aux_method["level_"+str(x)]:
                # file2 = open("../rules_phase_dataset_id_15072021.csv", "a")  # write mode
                # file2.write("\n" + str(doc_c['id'] + "," + str(doc_c['topics0_t'].split()) + "," + str(
                #     doc_c['topics1_t'].split()) + "," + str(doc_c['topics2_t'].split())).replace('[', '').replace(']',
                #                                                                                                   '').replace(
                #     ' ', '').replace("'", ""))
                # file2.close()

                fileresult = open("extended_associated_rules_27072021.csv", "a")  # write mode
                fileresult.write("\n" + str(j) + "," + main_rule_topics_list[i])
                fileresult.close()

if __name__ == '__main__':
    final_topics_list_filter_aux = []
    main_topics_list = csv_element()
    rules_aux_df = generateRules_withoutFilter()
    aux_aux_aux_list = aux_funcion(main_topics_list)

    buildAssociateRulesLevelBased()
    jsonString = json.dumps(rules_associate)
    jsonFile = open("extended_rules.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    unidirectionalAssociateRules()

    for list_aux in aux_aux_aux_list:
        final_topics_list_filter_aux.extend(list_aux)

    final_topics_list_filter = [frozenset({x})for x in list(set(final_topics_list_filter_aux))]
    rules_2517_aux = rules_aux_df[(rules_aux_df['antecedents'].isin(final_topics_list_filter)) & (rules_aux_df['consequents'].isin(final_topics_list_filter))]
    #rules_2517_aux = rules_aux_df[(rules_aux_df['antecedents'].isin(final_topics_list_filter))]
    rules_2517_aux.to_csv('filtered.csv', index=False)
    G = nx.from_pandas_edgelist(rules_aux_df,
                                source="antecedents",
                                target="consequents",
                                edge_attr="lift")
    print("final_levels_list")
    nx.draw(G, with_labels=True)
    plt.savefig("simple_path.png")
    plt.show()

