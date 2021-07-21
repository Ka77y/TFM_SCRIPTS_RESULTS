import json
import requests
import sys

sys.path.insert(1, '../')

URI_OBTAIN_DOCUMENT_INFORMATION = 'http://librairy.linkeddata.es/solr/tbfy/select?q=id:'
URI_INFERENCES = 'https://librairy.linkeddata.es/jrc-en-model/inferences'
URI_LIST_TOPICS = 'http://librairy.linkeddata.es/jrc-en-model/topics'
URI_DOCUMENT_RANK = 'http://localhost:8081/ranks'
URI_SEND_NEW_DOCUMENT_TOPICS = 'http://localhost:8983/solr/documents/update?commit=true'
results_rank_feedback = "results_rank_test_27052021.json"
rank_body_template = "rank_template.json"


def readJsonFile(jsonFileName):
    with open(jsonFileName) as json_file:
        data = json.load(json_file)
        return data

def loadJsonRankTemplate(id):
    data = readJsonFile(rank_body_template)
    data['reference']['document']['id'] = id
    document_rank = getDocumentRank(data)
    return document_rank

# envía una petición post
def postRequestApi(uri, body):
    headers = {'content-type': 'application/json'}
    r = requests.post(uri, data=json.dumps(body), auth=('demo', '2019'), headers=headers)
    return r

# obtiene la información del documento desde la bd
def getDocumentInformationApi(id):
    request = URI_OBTAIN_DOCUMENT_INFORMATION + id
    r = requests.get(request).json()
    json_string = r['response']['docs']

    return json_string

def getDocumentRank(body):
    new_rank_docs_id = []
    r = postRequestApi(URI_DOCUMENT_RANK, body).content
    new_rank_docs = json.loads(r.decode('ISO-8859-1'))['response']['docs']
    for doc in new_rank_docs:
        new_rank_docs_id.append(doc['id'])

    return new_rank_docs_id

def getDocumentListInformation(rank_list):
    list_docs_ranking = []
    document_information_query = ' OR id:'.join([str(elem) for elem in rank_list])
    list_docs_ranking[:] = getDocumentInformationApi(document_information_query)
    return list_docs_ranking

def obtainArrayDocTopics(document):
    doc = use_response_2(document)
    return [doc['topics0_t'], doc['topics1_t'], doc['topics2_t']]

# model: position o relevance -> dependiendo del modelo de feedback ejecutado
# topic_main_doc: el topic del main document que fue modificado
# action: put -> si se agregó un tópico junto al tópico de main document, move -> si se recorrió el tópico del
    # main document junto a uno de los tópicos de las ptras jerarquías
def createRulesCSV(model, topic_main_doc, action, topic_rank_doc, index_move=-1 ):
    rule = "rule: "+model+","+str(index_move)+","+topic_main_doc+","+action+","+topic_rank_doc
    file = open('rules_tender_27052021.csv', 'a')
    file.write('\n'+rule)
    file.close()

def createRulesCSVAllRelatedTopics(topic_main_doc, related_topics ):
    rule = "rule: "+topic_main_doc+","+str(related_topics)
    file = open('rules_tender_related_topics_27052021.csv', 'a')
    file.write('\n'+rule)
    file.close()

def rollbackNewTopicsIndex():
    postRequestApi(URI_SEND_NEW_DOCUMENT_TOPICS, 0)

#funcion que en el caso de que no exista el tópico 2 en el documento lo añade con un valor de 0
def use_response_2(doc):
    try:
        a = doc['topics2_t']
        return doc
    except:
        doc['topics2_t'] = "0"
        return doc

#funcion que en el caso de que no exista el tópico 1 en el documento lo añade con un valor de 0
def use_response_1(doc):
    try:
        a = doc['topics1_t']
        return doc
    except:
        doc['topics1_t'] = "0"
        return doc

if __name__ == '__main__':
    print(readJsonFile())
