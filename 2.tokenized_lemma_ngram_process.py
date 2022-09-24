# -*- coding: utf-8 -*-
import os
import jieba
import spacy
import string

from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.models.word2vec import LineSentence

import os
import codecs
import spacy
import pandas as pd
import itertools as it

nlp = spacy.load("en")
punctuation_exclude = set(string.punctuation)
path = os.getcwd()


def punct_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """

    return token.is_punct or token.is_space


def line_review(filename):
    """
    generator function to read in text content from the file
    and un-escape the original line breaks in the text
    """

    with open(filename, encoding='utf_8') as f:
        for text in f:
            #yield text.replace('\\n', '\n')
            yield text


def lemmatized_sentence_corpus(filename):
    """
    generator function to use spaCy to parse text content,
    lemmatize the text, and yield sentences
    """

    for parsed_review in nlp.pipe(line_review(filename),
                                  batch_size=10000, n_threads=4):

        for sent in parsed_review.sents:
            yield u' '.join([token.lemma_ for token in sent
                             if not punct_space(token)])


def savefile(savepath, content):
    fp = open(savepath, "w", encoding='utf-8', errors='ignore')
    fp.write(content)
    fp.close()


def readfile(path):
    fp = open(path, "r", encoding='utf-8', errors='ignore')
    content = fp.read()
    fp.close()
    return content


# this function is used to list all files in one folder but ingore the hidden file
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def generate_unigram_sentences(fileName):
    # this is a bit time consuming - make the if statement True
    # if you want to execute data prep yourself.
    if 1 == 1:

        with codecs.open(unigram_sentences_filepath, 'w', encoding='utf_8') as f:
            for sentence in lemmatized_sentence_corpus(fileName):
                f.write(sentence + '\n')


def build_bigram_model(unigram_sentences_filepath):
    # this is a bit time consuming - make the if statement True
    # if you want to execute modeling yourself.
    unigram_sentences = LineSentence(unigram_sentences_filepath)

    if 1 == 1:
        bigram_model = Phrases(unigram_sentences)
        #bigram_model = Phraser(unigram_sentences)

        bigram_model.save(bigram_model_filepath)

    # load the finished model from disk
    bigram_model = Phrases.load(bigram_model_filepath)
    #bigram_model = Phraser().load(bigram_model_filepath)
    return unigram_sentences,bigram_model


def generate_bigram_sentences(bigram_sentences_filepath, unigram_sentences, bigram_model):
    # this is a bit time consuming - make the if statement True
    # if you want to execute data prep yourself.


    if 1 == 1:

        with open(bigram_sentences_filepath, 'w', encoding='utf_8') as f:

            for unigram_sentence in unigram_sentences:
                bigram_sentence = u' '.join(bigram_model[unigram_sentence])

                f.write(bigram_sentence + '\n')


def build_trigram_model(bigram_sentences_filepath):
    # this is a bit time consuming - make the if statement True
    # if you want to execute modeling yourself.

    bigram_sentences = LineSentence(bigram_sentences_filepath)

    if 1 == 1:
        trigram_model = Phrases(bigram_sentences)

        trigram_model.save(trigram_model_filepath)

    # load the finished model from disk
    trigram_model = Phrases.load(trigram_model_filepath)
    return bigram_sentences,trigram_model


def generate_trigram_sentences(trigram_sentences_filepath, bigram_sentences, trigram_model):
    # this is a bit time consuming - make the if statement True
    # if you want to execute data prep yourself.
    if 1 == 1:

        with codecs.open(trigram_sentences_filepath, 'w', encoding='utf_8') as f:

            for bigram_sentence in bigram_sentences:
                trigram_sentence = u' '.join(trigram_model[bigram_sentence])

                f.write(trigram_sentence + '\n')


# this function is used to generate tokenized,lemmalized application_research_files using trigramm model based on
# the cleaned research files from step 1. Spacy is used instead of NLTK
def generate_trigram_applications_research_files(bigram_model, trigram_model):
    # this is a bit time consuming - make the if statement True
    # if you want to execute data prep yourself.
    if 1 == 1:

        with open(trigram_application_research_files_path, 'w', encoding='utf_8') as f:

            for parsed_review in nlp.pipe(line_review(cleaned_application_research_files_path),
                                          batch_size=10000, n_threads=4):
                # lemmatize the text, removing punctuation and whitespace
                unigram_sentences = [token.lemma_ for token in parsed_review
                                     if not punct_space(token)]

                # apply the first-order and second-order phrase models
                bigram_sentences = bigram_model[unigram_sentences]
                trigram_sentences = trigram_model[bigram_sentences]

                # remove any remaining stopwords
                trigram_sentences = [term for term in trigram_sentences
                                     if term not in spacy.en.English.Defaults.stop_words]

                # write the transformed review as a line in the new file
                trigram_sentences = u' '.join(trigram_sentences)
                f.write(trigram_sentences + '\n')


def compare_orginal_transformed():
    print(u'Original:' + u'\n')

    for research in it.islice(line_review(cleaned_application_research_files_path), 150, 151):
        print(research)

    print(u'----' + u'\n')
    print(u'Transformed:' + u'\n')

    with open(trigram_application_research_files_path, encoding='utf_8') as f:
        for research in it.islice(f, 150, 151):
            print(research)


'''
this function  is used to tokenize and lemmanize cleaned text using spacy instead of nltk.
At the same time, we remove stopwords and punctuation
'''


def tokenize_lemma_spacy(text):
    doc = nlp(text)

    # print("doc:", doc.text.split())

    # step 1:
    unigram_content = generate_unigram_sentences(text)

    tokens = [token.orth_ for token in doc if token.orth_ not in stop_words and token.orth_ not in punctuation_exclude]
    lemma = [word.lemma_ for word in nlp(" ".join(tokens))]
    return lemma


def load_stopword():
    f_stop = open(path + '/input/stopwords.txt')
    sw = set([line.strip() for line in f_stop])
    f_stop.close()
    return sw


# this function  is used to do pre-processing over cleaned data that we got from 0.cleanRawData.py
def preprocessingCleanedData(catelist, corpus_path, tokenized_path):
    for mydir in catelist:
        class_path = corpus_path + mydir + "/"  # concate path of sub-directory of raw data set
        seg_dir = tokenized_path + mydir + "/"  # concate path of sub-directory of tokenized data set
        if not os.path.exists(seg_dir):  # if not exist,create this folder
            os.makedirs(seg_dir)
        # file_list = os.listdir(class_path)
        file_list = listdir_nohidden(class_path)
        for file_path in file_list:
            fullname = class_path + file_path
            content = readfile(fullname).strip()  # read file content
            content = content.replace("\r\n", "").strip()  # rsemove \n, \r

            content_seg = tokenize_lemma_spacy(content)

            savefile(seg_dir + file_path, " ".join(content_seg))


if __name__ == '__main__':
    stop_words = load_stopword()
    research_files_clean_path = "research_files_clean/"  # path of cleaned research files that is from 0.

    cleaned_application_research_files_path = os.path.join(path + '/output','cleaned_application_research_files.txt')

    unigram_sentences_filepath = os.path.join(path + '/output', 'unigram_sentences_all.txt')

    bigram_model_filepath = os.path.join(path + '/output', 'bigram_model_all')

    bigram_sentences_filepath = os.path.join(path + '/output','bigram_sentences_all')

    trigram_model_filepath = os.path.join(path + '/output','trigram_model_all')

    trigram_sentences_filepath = os.path.join(path + '/output','trigram_sentences_all')


    trigram_application_research_files_path = os.path.join(path + '/output', 'trigram_transformed_applications_all.txt')



    research_files_catelist = listdir_nohidden(research_files_clean_path)  # access all sub-directories under this folder

    generate_unigram_sentences(cleaned_application_research_files_path)

    unigram_sentences, bigram_model = build_bigram_model(unigram_sentences_filepath)

    generate_bigram_sentences(bigram_sentences_filepath, unigram_sentences, bigram_model)

    bigram_sentences,trigram_model = build_trigram_model(bigram_sentences_filepath)

    generate_trigram_sentences(trigram_sentences_filepath, bigram_sentences, trigram_model)

    generate_trigram_applications_research_files(bigram_model, trigram_model)


    print("tokenizing cleaned data is over")
