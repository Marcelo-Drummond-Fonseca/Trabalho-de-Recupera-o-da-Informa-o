import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from SPARQLWrapper import SPARQLWrapper, JSON
import networkx as nx

def preprocess_line(query):
    #Quase igual ao do preprocessing.py, só voltado para uma linha, a query.
    text = query
    text = text.replace('@pt', '')
    text = re.sub(r'[()\.,;\'"\[\]-]', '', text)
    text = text.lower()
    stop_words = set(stopwords.words('portuguese'))
    words = [word for word in text.split() if word.lower() not in stop_words]
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words

def compute_tfidf_vectors(preprocessed_lines, vectorizer):
    # Converte as linhas preprocessadas do corpus para vetores tfidf usando TfidfVectorizer.
    preprocessed_text = [' '.join(line) for line in preprocessed_lines]

    tfidf_matrix = vectorizer.fit_transform(preprocessed_text)
    feature_names = vectorizer.get_feature_names_out()

    return feature_names, tfidf_matrix

def vectorize_query(preprocessed_query):
    united_preprocessed_query = [' '.join(preprocessed_query)]
    query_tfidf = vectorizer.transform(united_preprocessed_query)
    return query_tfidf
    

def read_input_files(input_file, input_names):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    preprocessed_lines = [eval(line.strip()) for line in lines]
        
    with open(input_names, 'r', encoding='utf-8') as names_file:
        names = names_file.read().splitlines()

    return preprocessed_lines, names

def compute_cosine_similarity(query_vector, document_vectors):
    #Calcula as similaridades de cosseno entre a query e o corpus
    similarities = cosine_similarity(query_vector, document_vectors)
    return similarities
    
def filter_results(names_pool, results_list):
    filtered_results_list = []
    for i in range(len(names_pool)):
        outlink_list = []
        for outlink in results_list[i]:
            if outlink in names_pool:
                outlink_list.append(outlink)
        filtered_results_list.append(outlink_list)

    #print(f"Filtered Results List: {filtered_results_list}")
    return filtered_results_list
    
def pagerank(names_pool, links):
    graph = nx.DiGraph()
    for i, outlinks in enumerate(links):
        graph.add_node(names_pool[i])
        for outlink in outlinks:
            graph.add_edge(names_pool[i], outlink)
    pagerank_scores = nx.pagerank(graph, alpha=0.85)
    print("PageRank Scores:")
    for node, score in sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{node}: {score}")
    

#Variáveis iniciais
input_preprocessed_file = 'output_preprocessed.txt'
input_names_file = 'output_document_names.txt'
sparql_endpoint = "http://dbpedia.org/sparql"
vectorizer = TfidfVectorizer()

#Inicialização
print("Realizando inicialização (Leitura de dados preprocessados e computando vetores tf-idf)...")
preprocessed_lines, names = read_input_files(input_preprocessed_file, input_names_file)
feature_names, tfidf_matrix = compute_tfidf_vectors(preprocessed_lines, vectorizer)
#print(tfidf_matrix)

#Loop de busca:

while(True):

    query = input("Insira chave de Busca (1 ou no máximo 2 para melhor efeito): ")
    print("Vetorizando a query e calculando similaridade de cossenos...")
    preprocessed_query = preprocess_line(query)
    query_tfidf = vectorize_query(preprocessed_query)
    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix)
    #print(f"Similaridades de Cosseno {cosine_similarities}")

    # Inicializa listas para armazenar os nomes disponíveis (com cosineSimilarity > 0) e resultados das queries de sparql
    names_pool = []
    results_list = []

    print("Construindo relacionamentos para pagerank com SPARQL...")
    for index, similarity in enumerate(cosine_similarities[0]):
        if similarity != 0:
            #print(f"Index: {index}, Preprocessed Line: {preprocessed_lines[index]}")
            name = names[index]
            #print(f"First Part of Line: {name}")

            sparql = SPARQLWrapper(sparql_endpoint)
            sparql_query = f"""
            SELECT ?object
            WHERE {{
              <{name}> <http://dbpedia.org/ontology/wikiPageWikiLink> ?object.
            }}
            """
            #print(sparql_query)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)
            #Usando Try e Except pois deu erro algumas vezes.
            try:
                results = sparql.queryAndConvert()
                if results["results"]["bindings"]:
                    #Transforma o resultado em uma lista de strings com os nomes no mesmo formato que a lista de nomes gerada no preprocessamento
                    result_objects = [result['object']['value'] for result in results["results"]["bindings"]]
                    #print(f"DBpedia Objects: {result_objects}")
                    names_pool.append(name)
                    results_list.append(result_objects)
                #else:
                    #print("No results found for the SPARQL query.")
            except Exception as e:
                print(f"Error in SPARQL query: {e}")

    #print(f"\nResults List: {results_list}")
    #print(f"\nNames Pool: {names_pool}")

    # A lista de resultados contém todas as conexões que existem saindo dos vértices com similaridade > 0. 
    # Aqui é removido da lista todas as arestas que levam a vértices fora do corpus reduzido.
    print("Filtrando resultados...")
    filtered_results_list = filter_results(names_pool, results_list)

    # Finalmente, o Pagerank
    print("Realizando Pagerank...")
    pagerank(names_pool, filtered_results_list)