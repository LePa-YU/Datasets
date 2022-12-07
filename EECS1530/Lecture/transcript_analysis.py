import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('maxent_ne_chunker')
nltk.download('words')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk import ne_chunk
from nltk.util import ngrams
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.probability import FreqDist

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from collections import Counter
import string
import inspect
import re

import time
import os
from os import walk

STOP_WORDS = set(stopwords.words('english'))
START_TIME = time.time()
READ_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'EECS2311\\Lecture_Transcripts'))
WRITE_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'EECS2311\\Lecture_Transcript_Keywords'))

def read_files(READ_PATH):
    print("read_files")
    print(READ_PATH)
    filenames = next(walk(READ_PATH), (None, None, []))[2]  # [] if no file

    # Go through all files individually
    for file in filenames:
        filename = READ_PATH+'\\'+file
        file_location = WRITE_PATH +'\\'+file.replace(" ", "_").split('.txt')[0]
        keyword_file_name = file_location.replace(" ", "_").split('.')[0]+'_keywords.txt'
        print(filename)
        print(file_location)
        print(keyword_file_name)

        # Checks if the result file exists
        if not os.path.exists(keyword_file_name):
            find_keywords(filename, keyword_file_name)
        else:
            print(keyword_file_name+" file exists.")
    return 0

def find_keywords(filename, keyword_file_name):
    print("find_keywords")

    with open(filename, 'r') as file:
        # counter_content, top_tfidf, top_tfidf_ = content_cleanup(file.read())
        counter_content, fdist, chunk, stem_top_tfidf, lem_top_tfidf, token_top_tfidf = content_cleanup(file.read())

        counter_content = [k for k, v in counter_content.most_common(n=25) if v > 1]
        fdist = fdist.most_common(25)
        combination = Counter(counter_content+list(lem_top_tfidf)+list(token_top_tfidf))
        # +list(stem_top_tfidf)

        with open(keyword_file_name, 'w') as file:
            file.write("Frequency distinct: \n")
            file.write(str(sorted(fdist)))
            # file.write("\n")
            # file.write("Counter: \n")
            # file.write(str(sorted(counter_content)))
            file.write("\n")
            file.write("tfidf: \n")
            file.write(str(sorted(token_top_tfidf)))
            file.write("\n")
            file.write("Stemmed tfidf: \n")
            file.write(str(sorted(stem_top_tfidf)))
            file.write("\n")
            file.write("Lemma tfidf: \n")
            file.write(str(sorted(lem_top_tfidf)))
            file.write("\n")
            file.write("Combination items: \n")
            file.write(str(sorted(combination.items())))
            file.write("\n")
            file.write("Combination most_common: \n")
            file.write(str(combination.most_common()))
            # file.write("\n")
            # file.write("Entity recognition: \n")
            # file.write(str(chunk))

        # input("Press enter to continue...")

def content_cleanup(content):
    ps = PorterStemmer()
    lemma = WordNetLemmatizer()

    # Remove Error: marker
    # Remove punctuation and numbers
    # Remove all words under 2 characters
    content = content.replace("Error:","")
    content = content.translate(str.maketrans('', '', string.punctuation))
    content = content.translate(str.maketrans('', '', string.digits))
    content = ' '.join(word for word in content.split() if len(word)>2)

    # print(content)

    word_tokens = word_tokenize(content)

    word_tokens = [word for word in word_tokens if not word.lower() in STOP_WORDS]

    # print(content)
    # input("Press enter to continue...")

    # stems words
    stemmed_content = [ps.stem(word) for word in word_tokens]
    lemma_content = [lemma.lemmatize(word) for word in word_tokens]

    # use Counter to count words
    counter_content = Counter(word_tokens)
    fdist = FreqDist(word_tokens)

    # Used stemmed and tokenized words to create tfidf
    stem_top_tfidf, stem_tfidf = tfidf_content([' '.join(stemmed_content)])
    lem_top_tfidf, lem_tfidf = tfidf_content([' '.join(lemma_content)])
    token_top_tfidf, token_tfidf = tfidf_content([' '.join(word_tokens)])

    # Named entity recognition
    tags = pos_tag(word_tokens)
    chunk = ne_chunk(tags)

    return counter_content, fdist, chunk, stem_top_tfidf, lem_top_tfidf, token_top_tfidf

# def filter_content(word_tokens):
#     punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
#     filtered_content = [word for word in word_tokens if not word.lower() in STOP_WORDS] # remove stop words
#     filtered_content = [word.lower() for word in filtered_content if not word in punctuations] # remove punctuations
#     filtered_content = [re.sub('[^A-Za-z]+', '', word) for word in filtered_content] # only keep words (no numbers, special characters)
#     filtered_content = list(filter(None, filtered_content)) # filter out any empty strings in list
#
#     return filtered_content

def tfidf_content(content):
    # vectorizer = TfidfVectorizer()
    # vectors = vectorizer.fit_transform(content)
    # feature_names = vectorizer.get_feature_names_out()
    # dense = vectors.todense()
    # denselist = dense.tolist()
    # df = pd.DataFrame(denselist, columns=feature_names)

    vectorizer = TfidfVectorizer(analyzer = 'word', stop_words='english')
    tfidf_wm = vectorizer.fit_transform(content)
    tfidf_tokens = vectorizer.get_feature_names_out()

    df = pd.DataFrame(data = tfidf_wm.toarray(), index=['1'], columns = tfidf_tokens)

    # print(df)

    top = tfidf_wm.toarray().max(axis=0).argsort()[-25:]
    return np.asarray(tfidf_tokens)[top], df



    # print(tfidf_top(denselist,feature_names))

    # print(df)
    # input("Press enter to continue...")

    # return df


def tfidf_top(row, features, top_n=25):
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df


read_files(READ_PATH)
