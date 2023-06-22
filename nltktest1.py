import nltk
from autocorrect import Speller
import string

def nltk_check_function(message):
    messageToReturn = ''
    if '-' in message or '+' in message:
        messageToReturn = message
    else :
        message = message.lower()
        message = message.translate(str.maketrans("", "", string.punctuation))
        tokenizer = nltk.sent_tokenize(message)
        spell = Speller()
        corrected_tokenizer = []
        for sentence in tokenizer:
            words = nltk.word_tokenize(sentence)
            corrected_words = [spell(w) for w in words]
            corrected_sentence = " ".join(corrected_words)
            corrected_tokenizer.append(corrected_sentence)
        autocorrected_message = " ".join(corrected_tokenizer)
        messageToReturn = autocorrected_message
    return messageToReturn



message = nltk_check_function("waht is my name @ali")

print(message)