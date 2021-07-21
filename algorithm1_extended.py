#primer algoritmo de asociación de tópicos
from Scripts.training import obtainTopics
from Scripts.training.generalFunctions import obtainArrayDocTopics, createRulesCSV, createRulesCSVAllRelatedTopics

LIBRARY_EXECUTED = 0
ALL_RELATED_TOPICS = []
ALL_TOPICS_APPENDED = []

def relevanceFirstTopicSolution(main_doc_response, list_docs_high):
    global ALL_RELATED_TOPICS
    ALL_RELATED_TOPICS = []
    #genera un array de los tópicos del documento principal cada posición del array representa un nivel de jerarquía
    main_doc_topics_original = obtainArrayDocTopics(main_doc_response);
    main_doc_topics = main_doc_topics_original[:];
    ALL_RELATED_TOPICS.append(main_doc_topics_original[0])
    for doc in list_docs_high:
        # genera un array de los tópicos del documento similar orden k cada posición del array representa un nivel de jerarquía
        doc_rank_topics = obtainArrayDocTopics(doc);

        for i_rank, topic in enumerate(doc_rank_topics):
            #verifica si el tópico se encuentra en el documento principal
            if topic not in ALL_RELATED_TOPICS:
                if topic in main_doc_topics:
                    i_main = main_doc_topics.index(topic);
                    if i_main != 0 and i_main != i_rank:
                        #llama a la función que analiza cuando el tópico existe en el documento principal
                        replaceTopicWhenItExists(main_doc_topics, main_doc_response, i_main, main_doc_topics_original, topic)
                    if i_main == i_rank:
                        createRulesCSV("relevance_1", str(main_doc_topics_original[0]), "put", str(topic))
                        ALL_RELATED_TOPICS.append(topic)
                    # si el tópico no se encuentra en el documento principal se lo añade en su nivel de
                    # jerarquía topics_0
                    #creación de regla
                else:
                    createRulesCSV("relevance_1", str(main_doc_topics_original[0]), "put", str(topic))
                    ALL_RELATED_TOPICS.append(topic)
                    break

    createRulesCSVAllRelatedTopics(main_doc_topics_original[0], ALL_RELATED_TOPICS)



def replaceTopicWhenItExists(main_doc_topics, main_doc_response, i_main, main_doc_topics_original, topic_high_document="0"):
    global LIBRARY_EXECUTED
    global next_augmented_topic

    #recupera todos los tópicos del documento principal en un array
    topics_main_document = obtainTopics.obtainDocumentTopics(main_doc_response['txt_t'], LIBRARY_EXECUTED)
    #recupera el tópico antes de que se le añada uno
    next_augmented_topic = main_doc_topics[0]
    ALL_TOPICS_APPENDED.extend([next_augmented_topic,topic_high_document])
    #recorre el tópico inmediatamente inferior hacia la posición del tópico current
    main_doc_topics[0] = main_doc_topics[0] + ' ' + topic_high_document;
    #recorre todos los tópicos de jerarquias inferiores una posición
    while i_main < len(main_doc_topics):
        main_doc_topics[i_main] = topics_main_document[i_main + 1];
        i_main = i_main + 1
    LIBRARY_EXECUTED += 1
    #asocia tópicos
    createRulesCSV("relevance_1", main_doc_topics_original[0], "move", topic_high_document)
    ALL_RELATED_TOPICS.append(topic_high_document);
    return main_doc_topics