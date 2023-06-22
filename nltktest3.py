import nltk

def extract_relationship(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    relationship = None

    for word, tag in tagged:
        if tag == 'NN' and word.lower() == 'friend':
            relationship = word
        elif tag == 'NN' and word.lower() == 'brother':
            relationship = word
        elif tag == 'NN' and word.lower() == 'sister':
            relationship = word
        elif tag == 'NN' and word.lower() == 'father':
            relationship = word
        elif tag == 'NN' and word.lower() == 'mother':
            relationship = word
        elif tag == 'NN' and word.lower() == 'uncle':
            relationship = word
        elif tag == 'NN' and word.lower() == 'aunt':
            relationship = word
        elif tag == 'NN' and word.lower() == 'dont know':
            relationship = "dont know"

    return relationship

sentence = "yes he is my friend "
relationship = extract_relationship(sentence)

print(relationship)  # Output: brother