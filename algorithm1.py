#primer algoritmo de asociación de tópicos
from Scripts.training import obtainTopics
from Scripts.training.generalFunctions import obtainArrayDocTopics, createRulesCSV

FOCUS_DOC_SOLUTION = 0
LIBRARY_EXECUTED = 0

def relevanceFirstTopicSolution(main_doc_response, list_docs_high):
    global FOCUS_DOC_SOLUTION

    #recupera el primer documento high que es encontrado desde la retroalimentación
    try:
        first_doc_result_response = list_docs_high[FOCUS_DOC_SOLUTION];
    except:
        first_doc_result_response = ['none']
        pass
    #genera un array de los tópicos del documento principal cada posición del array representa un nivel de jerarquía
    main_doc_topics = obtainArrayDocTopics(main_doc_response);
    #genera un array de los tópicos del documento similar orden k cada posición del array representa un nivel de jerarquía
    first_doc_result_topics = obtainArrayDocTopics(first_doc_result_response);

    for_flag = 0
    for i_rank, topic in enumerate(first_doc_result_topics):
        if for_flag == 1:
            break;
        else:
            try:
                #verifica si el tópico se encuentra en el documento principal
                i_main = main_doc_topics.index(topic);
                if i_rank < i_main:
                    #llama a la función que analiza cuando el tópico existe en el documento principal
                    replaceTopicWhenItExists(i_rank, main_doc_topics, main_doc_response, topic)
                    for_flag = 1
            except:
                find_topic = 0
                for j in range(0,3):
                    if topic in main_doc_topics[j]:
                        # find_topic = 1 cuando se encuentra el tópico en el documento principal
                        # si el tópico se encuentra en el documento principal pero no cumple las condiciones para que se
                        # realice sobre este alguna acción, se analiza el siguiente tópico
                        find_topic = 1
                else:
                    if find_topic == 0:
                        for_flag = 1
                        # si el tópico no se encuentra en el documento principal se lo añade en su mismo nivel de
                        # jerarquía del documento similar orden k
                        #creación de regla
                        createRulesCSV("relevance_1", str(main_doc_topics[i_rank]), "put", str(topic))
                        break

    if for_flag == 0:
        #se analiza si existen más documentos clasificados con relevancia alta en la retroalimentación
        FOCUS_DOC_SOLUTION += 1
        if FOCUS_DOC_SOLUTION < len(list_docs_high):
            relevanceFirstTopicSolution()

def replaceTopicWhenItExists(i_rank, main_doc_topics, main_doc_response, topic_high_document=0):
    global LIBRARY_EXECUTED
    global next_augmented_topic

    for x in range(i_rank, len(main_doc_topics)):
        #recupera todos los tópicos del documento en un array
        topics_main_document = obtainTopics.obtainDocumentTopics(main_doc_response['txt_t'], LIBRARY_EXECUTED)
        #recupera el tópico antes de que se le añada uno
        next_augmented_topic = main_doc_topics[x]
        #recorre el tópico inmediatamente inferior hacia la posición del tópico current
        main_doc_topics[x] = main_doc_topics[x] + ' ' + main_doc_topics[x + 1];
        x = x + 1
        #recorre todos los tópicos de jerarquias inferiores una posición
        while x < len(main_doc_topics):
            main_doc_topics[x] = topics_main_document[x + 1];
            x = x + 1
        LIBRARY_EXECUTED += 1
        break
    #asocia tópicos
    createRulesCSV("relevance_1", next_augmented_topic, "move", topic_high_document, i_rank)
    return main_doc_topics