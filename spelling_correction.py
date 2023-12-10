
import os, sys, gc, warnings
import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')

input_file_location = 'data.txt'

# ! pip install seaborn

# We will preprocess the data by reading the file from the default directory and then prepare a list of words in the
# entire corpus, we will also lowercase the words while processing them

# Initiating the word list here
word_list = []

# read the file and append words one by one
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        for word in line.split():
            word_list.append(word.lower())

# This will be our new vocabulary
vocab = set(word_list)

# Initiating the word_count dictionary and populating it
word_count_dict = {}
word_count_dict = Counter(word_list)
# print(f"There are {len(word_count_dict)} key values pairs")

# Initalize the probability dictionary
probs = {}
total_words = sum(word_count_dict.values())

for word, word_count in word_count_dict.items():
    word_prob = word_count/total_words
    probs[word] = word_prob
# print(f"Length of probs is {len(probs)}")

# Let us use both the dictionaries for both word counts and probabilities and display an example word.
# print(f"P('thee') is {probs['thee']:.4f}")
# print(word_count_dict['thee'])

def delete_letter(word):
    delete_list = []
    split_list = []
    split_list = [(word[:i], word[i:]) for i in range(len(word))]
    delete_list = [L+R[1:] for L, R in split_list]
    return delete_list

def switch_letter(word):
    switch_list = []
    split_list = []
    split_list = [(word[:i], word[i:]) for i in range(len(word))]
    switch_list = [L + R[1] + R[0] + R[2:] for L, R in split_list if len(R)>=2]
    return switch_list

def replace_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    replace_list = []
    split_list = []
    split_list = [(word[0:i], word[i:]) for i in range(len(word))]
    replace_list = [L + letter + (R[1:] if len(R)>1 else '') for L, R in split_list if R for letter in letters]
    replace_set = set(replace_list)
    replace_list = sorted(list(replace_set))
    return replace_list

def insert_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_list = []
    split_list = []
    split_list = [(word[0:i], word[i:]) for i in range(len(word)+1)]
    insert_list = [L + letter + R for L, R in split_list for letter in letters]
    return insert_list

def edit_one_letter(word, allow_switches = True):
    edit_one_set = set()
    edit_one_set.update(delete_letter(word))
    if allow_switches: edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))
    if word in edit_one_set: edit_one_set.remove(word)
    return edit_one_set

def edit_two_letter(word, allow_switches = True):
    edit_two_set = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for word in edit_one:
        if word:
            edit_two = edit_one_letter(word, allow_switches=allow_switches)
            edit_two_set.update(edit_two)

    return edit_two_set

def get_spelling_suggestions(word, probs, vocab, n=1, default_probability=0.0):
    suggestions = (
        [word] if word in vocab else
        edit_one_letter(word).intersection(vocab) or
        edit_two_letter(word).intersection(vocab)
    )

    # Filter out single-character suggestions
    valid_suggestions = [s for s in suggestions if len(s) > 1]

    # Find the word with the maximum probability
    max_word = max(valid_suggestions, key=lambda s: probs.get(s, default_probability), default=None)

    if max_word:
        max_prob = probs.get(max_word, default_probability)
        return [[max_word, max_prob]]

    return []


default_probability = 0.0

result = get_spelling_suggestions("furthar", probs, vocab, 3, default_probability)
# print(result)

# my_words = ['dys','furthar','mercuryn','hapy','artism']
# tmp_corrections = []
# for word_c in my_words:
#     tmp_corrections.append(get_spelling_suggestions(word_c, probs, vocab, 3))
# for i, word in enumerate(my_words):
#     print(' ')
#     print(f'Word - {my_words[i]}')
#     for j, word_prob in enumerate(tmp_corrections[i]):
#       if(word_prob):
#         print(f"word - {j}: {word_prob[0]}, probability {word_prob[1]:.6f}")

def correctSentence(sentence):
  final_sentence=""
  for w in sentence.split(' '):
    result = get_spelling_suggestions(w.lower(), probs, vocab, 3, default_probability)
    if(result):
      final_sentence+=result[0][0]+" "
    else:
      final_sentence+=w+" "
  # print(sentence)
#   print(final_sentence)
  return final_sentence

# sentence="corrct ths sentnce"
# (correctSentence(sentence))

