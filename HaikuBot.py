import wikipedia
import re
import random
import string
import time
import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict

def syllables_in_word(word, dictionary):
    if word not in dictionary:
        return 0
    return len([ph for ph in dictionary[word] if ph.strip(string.ascii_letters)])

def randoo(words, syllables_left, word_graph):
        randList = []
        for word in words:
            for i in range(words[word]):
                if num_of_syllables[word] <= syllables_left:
                    randList.append(word)

        if not randList:
            return random.choice(list(word_graph.keys()))
        return random.choice(randList)
    
def markov(input_file, word_graph):
    prev_word = None
    for word in input_file.rstrip('?:!.,;"').split():
        word = word.lower()
        if word_graph.get(prev_word)==None:
            word_graph[prev_word]={}
        if word_graph[prev_word].get(word)==None:
            word_graph[prev_word][word]=0
        word_graph[prev_word][word]+=1
        prev_word = word

def generate_haiku(word_graph, search_query, end_word, num_of_syllables):
    final = ""
    start_word = search_query
    final+=start_word + ' '
    line_one_syllables_left = 5 - num_of_syllables[start_word]
    
    while line_one_syllables_left > 0:
        word=randoo(word_graph[start_word], line_one_syllables_left, word_graph)
        while word not in word_graph:
            word=randoo(word_graph[start_word], line_one_syllables_left, word_graph)
        final+=word + ' '
        start_word = word
        line_one_syllables_left-=num_of_syllables[word] 
    
    final+='\n'
    line_two_syllables_left = 7

    while line_two_syllables_left > 0:
        word=randoo(word_graph[start_word], line_two_syllables_left, word_graph)
        while word not in word_graph:
            word=randoo(word_graph[start_word], line_two_syllables_left, word_graph)
        final+=word + ' '
        start_word = word
        line_two_syllables_left-=num_of_syllables[word] 

    final+='\n'

    end_word = randoo(end_words, 100, word_graph)
    line_three_syllables_left = 5 - num_of_syllables[end_word]

    while line_three_syllables_left > 0:
        word=randoo(word_graph[start_word], line_three_syllables_left, word_graph)
        while word not in word_graph:
            word=randoo(word_graph[start_word], line_three_syllables_left, word_graph)
        final+=word + ' '
        start_word = word
        line_three_syllables_left-=num_of_syllables[word] 

    final+=end_word

    return final

d = dict(cmudict.entries())
search_query = 'dog'
relevant_sentences = ""
translator = str.maketrans(dict.fromkeys(string.punctuation))

for sentence in wikipedia.page(search_query).content.split('.'):
    if search_query in sentence:
        relevant_sentences+=sentence + '. '

relevant_sentences = re.sub(r'\d+', '', relevant_sentences)

end_words = {}
for word in relevant_sentences.split():
    word = word.lower()
    if '.' in word:
        word = word.translate(translator)
        if syllables_in_word(word, d) != 0:
            if end_words.get(word) == None:
                end_words[word] = 0
            end_words[word]+=1

num_of_syllables = {}

word_graph = {}
input_text = ""
for word in relevant_sentences.translate(translator).split():
    word = word.lower()
    if syllables_in_word(word, d) != 0:
        if word not in num_of_syllables.keys():
            num_of_syllables[word] =  syllables_in_word(word, d)
        input_text+=word
        input_text+= ' '

markov(input_text, word_graph)

print(generate_haiku(word_graph, search_query, end_words, num_of_syllables))









