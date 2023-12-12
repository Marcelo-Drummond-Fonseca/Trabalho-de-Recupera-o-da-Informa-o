# Trabalho-de-Recuperação-da-Informação

Marcelo Drummond Fonseca, DRE 117216621

Esse git inclui os arquivos de implementação para o trabalho final de Recuperação da Informação.

preprocessing.py realiza pre-processamento e formatação do dataset. Isso pode levar uma quantidade grande de tempo

main.py realiza a busca, passo a passo, no final devolvendo a lista de documentos em ordem decrescente de pagerank. Terá um processamento feito ao inicializar o programa, que pode demorar alguns minutos. O mais importante é que depois da query ser inserida, levará uma quantidade muito grande de tempo para terminar a execução da query, devido às queries SPARQL necessárias (com palavras relativamente comuns, demorou mais de 20 minutos para mim)

Cosine_only realiza somente a similaridade de cossenos, sem o pagerank, e foi utilizado para a validação.

O dataset em si era grande demais para o github. Está disponível em https://www.dropbox.com/scl/fo/p49ffqwdo38a7q1derstj/h?rlkey=bghi46uh19713cy5331hw9ny0&dl=0

Se desejar obter da fonte original, está disponível em https://downloads.dbpedia.org/2016-10/core/ (é o documento short_abstracts_en_uris_pt.ttl.bz2 )
