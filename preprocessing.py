import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
nltk.download('stopwords')

def preprocess_line(line):
    # Realizea Preprocessamento de cada linha, incluindo formatação, remoção de stopwords, e stemming.
    text = re.search('"([^"]*)"', line).group(1)
    text = text.replace('@pt', '')
    text = re.sub(r'[()\.,;\'"\[\]]', '', text)
    text = text.lower()
    stop_words = set(stopwords.words('portuguese'))
    words = [word for word in text.split() if word.lower() not in stop_words]
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words

def preprocess_file(input_file, output_file, output_file_names):
    #Preprocessamento do arquivo total
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    preprocessed_lines = [preprocess_line(line) for line in lines]

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for preprocessed_line in preprocessed_lines:
            outfile.write(str(preprocessed_line) + '\n')
            
    with open(output_file_names, 'w', encoding='utf-8') as outfile_names:
        for line in lines:
            entity = re.search('<([^>]*)>', line).group(1)
            outfile_names.write(entity + '\n')

# Specify input and output file paths
input_file_path = 'short_abstracts_en_uris_pt.ttl'  # Replace with your file path
output_file_path = 'output_preprocessed.txt'  # Replace with your desired output file path
output_file_names_path = 'output_document_names.txt' # Replace with your desired output file path for the names

# Call the preprocess_file function
preprocess_file(input_file_path, output_file_path, output_file_names_path)