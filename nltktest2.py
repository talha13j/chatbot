import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree


text = "my Name is Ali"

def get_name(message):
    nltk_results = ne_chunk(pos_tag(word_tokenize(message)))
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            name = ''
            for nltk_result_leaf in nltk_result.leaves():
                name += nltk_result_leaf[0] + ' '
            return name
        
print(get_name(text))