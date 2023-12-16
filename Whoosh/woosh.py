from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser

def remove_stopwords(query):
    stopwords = ['a', 'the', 'an', 'and', 'or', 'but', 'about', 'above', 'after', 'along', 'amid', 'among', 'as', 'at', 'by', 'for', 'from', 'in', 'into', 'like', 'minus', 'near', 'of', 'off', 'on', 'onto', 'out', 'over', 'past', 'per', 'plus', 'since', 'till', 'to', 'up', 'via', 'vs', 'with', 'that', 'can', 'cannot', 'could', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would', 'have', 'had', 'has', 'having', 'be', 'is', 'am', 'are', 'was', 'were', 'being', 'been', 'get', 'gets', 'got', 'gotten', 'getting', 'seem', 'seeming', 'seems', 'seemed', 'enough', 'both', 'all', 'your', 'those', 'this', 'these', 'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my', 'its', 'his', 'her', 'every', 'either', 'each', 'any', 'another', 'an', 'a', 'just', 'mere', 'such', 'merely', 'right', 'no', 'not', 'only', 'sheer', 'most', 'rather', 'somewhat', 'sufficiently', 'same', 'different', 'such', 'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which', 'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', 'anything', 'anytime', 'anywhere', 'everybody', 'everyday', 'everyone', 'everyplace', 'everything', 'everywhere', 'whatever', 'whenever', 'wherever', 'whichever', 'whoever', 'whomever', 'he', 'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their', 'theirs', 'you', 'your', 'yours', 'me', 'my', 'mine', 'I', 'we', 'us', 'much', 'and/or']

    # Convertendo para minúsculas 
    cleaned_query = query.lower()
    
    # Separando as palavras da consulta
    words = cleaned_query.split()
    
    # Removendo stopwords da consulta
    cleaned_words = [word for word in words if word not in stopwords]
    
    # Reconstruindo a consulta sem as stopwords
    cleaned_query = ' '.join(cleaned_words)
    
    return cleaned_query

# Defina o esquema dos documentos
schema = Schema(id=ID(unique=True, stored=True),
                title=TEXT(stored=True),
                author=TEXT(stored=True),
                bibliography=TEXT(stored=True),
                content=TEXT(stored=True))

# Crie um índice Whoosh
index_dir = "C:\\Users\\maxwe\\OneDrive\\Área de Trabalho\\cran\\whoosh"
ix = create_in(index_dir, schema)

writer = ix.writer()
current_document = {}
with open('C:\\Users\\maxwe\\OneDrive\\Área de Trabalho\\cran\\cran.all.1400', 'r') as file:
    documents = []
    current_document = {}
    content_started = False  # Indicador para começar a ler o conteúdo do documento
    line = file.readline()
    
    while line:  
        if line.startswith(".I"):
            if current_document:
                # Adiciona o documento atual à lista de documentos
                writer.add_document(**current_document)
                current_document = {}  # Limpa as informações do documento atual

            current_document['id'] = line.split()[1].strip()  # Obter o ID do documento
        
        try:
            line = next(file).strip()  # Lê a próxima linha
        except StopIteration:
            break  # Se acabaram as linhas, pare
        
        if line.startswith(".T"):
            content_started = True
            current_document['title'] = ""  # Inicializa o título do documento
            line = next(file).strip()  # Pula para a próxima linha após a tag

            while line and not line.startswith((".I", ".T", ".A", ".B", ".W")):
                current_document['title'] +=  remove_stopwords(line) + " "  # Lê o título do documento
                try:
                    line = next(file).strip()  # Lê a próxima linha
                except StopIteration:
                    break  # Se acabaram as linhas, pare

        if line.startswith(".A"):
            content_started = True
            current_document['author'] = ""  # Inicializa o autor do documento
            line = next(file).strip()  # Pula para a próxima linha após a tag

            while line and not line.startswith((".I", ".T", ".A", ".B", ".W")):
                current_document['author'] += line + " " # Lê o autor do documento
                try:
                    line = next(file).strip()  # Lê a próxima linha
                except StopIteration:
                    break  # Se acabaram as linhas, pare
                
        if line.startswith(".B"):
            content_started = True
            current_document['bibliography'] = ""  # Inicializa o conteúdo do documento
            line = next(file).strip()  # Pula para a próxima linha após a tag

            while line and not line.startswith((".I", ".T", ".A", ".B", ".W")):
                current_document['bibliography'] +=  line  + " "  # Lê o conteúdo do documento
                try:
                    line = next(file).strip()  # Lê a próxima linha
                except StopIteration:
                    break  # Se acabaram as linhas, pare

        if line.startswith(".W"):
            content_started = True
            current_document['content'] = ""  # Inicializa o conteúdo do documento
            line = next(file).strip()  # Pula para a próxima linha após a tag

            while line and not line.startswith((".I", ".T", ".A", ".B", ".W")):
                current_document['content'] +=  remove_stopwords(line) + " "
                # Lê o conteúdo do documento
                try:
                    line = next(file).strip()  # Lê a próxima linha
                except StopIteration:
                    break  # Se acabaram as linhas, pare
        
        
    # Adiciona o último documento à lista de documentos
    if current_document:
        writer.add_document(**current_document)

writer.commit()

def busca(original_query):
    # Abrir o índice dos documentos
    document_index = open_dir("C:\\Users\\maxwe\\OneDrive\\Área de Trabalho\\cran\\whoosh")

    # Definir os campos onde deseja pesquisar
    fields = ["content"]

    # Criar um parser de consulta para pesquisar em vários campos
    query_parser = MultifieldParser(fields, schema=document_index.schema)

    # Remover stopwords, se necessário
    query_without_stopwords = remove_stopwords(original_query)

    # Substituir espaços por " OR "
    query_with_OR = query_without_stopwords.replace(" ", " OR ")

    query = query_parser.parse(query_with_OR)

    # Realizar a busca
    with document_index.searcher() as searcher:
        results = searcher.search(query)

        if len(results) > 0:
            #print("Documentos encontrados:")
            found_ids = []  # Lista para armazenar os IDs encontrados
            for result in results:
                #print(f"ID: {result['id']} - Score: {result.score}")
                found_ids.append(int(result['id']))  # Adiciona o ID encontrado à lista
                #print("\n")
            return found_ids  # Retorna a lista de IDs encontrados
        else:
            #print("Nenhum documento encontrado para esta consulta.")
            return []  # Retorna uma lista vazia, já que nenhum documento foi encontrado

def extract_queries_from_cranqry(file_path):
    queries = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_query_id = None
        current_query = None
        for line in lines:
            if line.startswith('.I'):
                if current_query_id and current_query:
                    queries[current_query_id] = remove_stopwords(current_query) + " "
                current_query_id = line.split()[1].strip()
                current_query = ''
            elif line.startswith('.W'):
                continue
            else:
                current_query += line.strip() + ' '
        # Adicionar a última consulta
        if current_query_id and current_query:
            queries[current_query_id] = remove_stopwords(current_query)
    return queries

def extract_relevant_documents(file_path):
    relevant_docs = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            query_id, doc_id, relevance = map(int, line.strip().split())
            if query_id not in relevant_docs:
                relevant_docs[query_id] = []
            relevant_docs[query_id].append((doc_id, relevance))

    # Ordenar os documentos relevantes e manter somente os 10 primeiros
    for query_id, docs in relevant_docs.items():
        sorted_docs = sorted(docs, key=lambda x: x[1], reverse=True)[:10]
        relevant_docs[query_id] = [doc[0] for doc in sorted_docs]

    return relevant_docs

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import time

counter = 0
media = 0

# Caminho para o arquivo cranqrel
cranqrel_file_path = 'C:\\Users\\maxwe\\OneDrive\\Área de Trabalho\\cran\\cranqrel'

# Extrair documentos relevantes do arquivo cranqrel
relevant_documents = extract_relevant_documents(cranqrel_file_path)
    
# Caminho para o arquivo cran.qry
qry_file_path = 'C:\\Users\\maxwe\\OneDrive\\Área de Trabalho\\cran\\cran.qry'

# Extrair as consultas do arquivo cran.qry
queries = extract_queries_from_cranqry(qry_file_path)

start_time = time.time()
for query_id, query_text in queries.items():
    if int(query_id) > 225:
        break
    counter = counter + 1
    
    
    results = busca(query_text)

    
    relevant_docs_found = results  # A lista de IDs encontrados já é retornada por busca()

    relevant_docs_current_query = relevant_documents[int(query_id.lstrip('0'))]

    # print(f"Consulta ID: {query_id}")
    # print(f"Documentos Relevantes: {relevant_docs_current_query}")
    # print(f"Documentos Encontrados na Busca: {relevant_docs_found}")

    # Converter relevant_docs_found para um conjunto para facilitar a comparação
    relevant_docs_found_set = set(relevant_docs_found)

    # Encontrar a interseção entre os documentos relevantes da consulta e os encontrados na busca
    common_docs = relevant_docs_found_set.intersection(relevant_docs_current_query)
    
    media = media + len(common_docs)/len(relevant_documents[int(query_id.lstrip('0'))])

    # print(f"Total de Documentos Relevantes para esta consulta: {len(relevant_docs_current_query)}")
    # print(f"Documentos Encontrados na Busca: {len(relevant_docs_found)}")
    #print(f"Documentos Relevantes Encontrados na Busca: {len(common_docs)}")
    #print("\n")
end_time = time.time()   
print("Acurácia Média = ",(media/counter)*100)
execution_time = end_time - start_time
print(f"Tempo total de execução das buscas: {execution_time:.4f} segundos")