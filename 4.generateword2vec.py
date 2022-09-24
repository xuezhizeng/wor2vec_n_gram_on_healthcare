from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import os
import pandas as pd


path = os.getcwd()

trigram_sentences_filepath = os.path.join(path + '/output','trigram_sentences_all')


trigram_sentences = LineSentence(trigram_sentences_filepath)

word2vec_filepath = os.path.join(path + '/output', 'word2vec_model_all')


import sys

# this is a bit time consuming - make the if statement True
# if you want to train the word2vec model yourself.
if 0 == 1:

    # initiate the model and perform the first epoch of training
    research2vec = Word2Vec(trigram_sentences, size=300, window=5,
                        min_count=20, sg=1, workers=4)
    print('First epoch completed')
    research2vec.save(word2vec_filepath)

    # perform another 11 epochs of training
    for i in range(1, 12):
        sys.stderr.write('\rOn {}'.format(i))
        research2vec.train(trigram_sentences, total_examples=research2vec.corpus_count, epochs=research2vec.iter)
        research2vec.save(word2vec_filepath)

# load the finished model from disk
research2vec = Word2Vec.load(word2vec_filepath)
research2vec.init_sims()

print(u'{} training epochs so far.'.format(research2vec.train_count))


print(u'{:,} terms in the research2vec vocabulary.'.format(len(research2vec.wv.vocab)))


# build a list of the terms, integer indices,
# and term counts from the food2vec model vocabulary
ordered_vocab = [(term, voc.index, voc.count)
                 for term, voc in research2vec.wv.vocab.items()]



# sort by the term counts, so the most common terms appear first
ordered_vocab = sorted(ordered_vocab, key=lambda x: -x[2])



# unzip the terms, integer indices, and counts into separate lists
ordered_terms, term_indices, term_counts = zip(*ordered_vocab)





# create a DataFrame with the food2vec vectors as data,
# and the terms as row labels
word_vectors = pd.DataFrame(research2vec.wv.syn0norm[term_indices, :],
                            index=ordered_terms)



print(len(word_vectors))


print(word_vectors.head)



def get_related_terms(token, topn=10):
    """
    look up the topn most similar terms to token
    and print them as a formatted list
    """

    for word, similarity in research2vec.most_similar(positive=[token], topn=topn):

        print(u'{:20} {}'.format(word, round(similarity, 3)))




print(get_related_terms(u'tumour'))



print("\n\n")

print(get_related_terms(u'influenza'))



print("\n\n")


print(get_related_terms(u'breast'))



print("\n\n")

print(get_related_terms(u'australian'))




def word_algebra(add=[], subtract=[], topn=1):
    """
    combine the vectors associated with the words provided
    in add= and subtract=, look up the topn most similar
    terms to the combined vector, and print the result(s)
    """
    answers = research2vec.most_similar(positive=add, negative=subtract, topn=topn)

    for term, similarity in answers:
        print(term)


print("======================")
print(word_algebra(add=[u'brain', u'tumour']))
print(word_algebra(add=[u'breast', u'tumour']))
print(word_algebra(add=[u'australian', u'tumour']))



print("======================")
word_algebra(add=[u'breast', u'cancer'], subtract=[u'brain'])


print("======================")
word_algebra(add=[u'gbm', u'cancer'], subtract=[u'hgg'])


print("======================")
word_algebra(add=[u'breast', u'cancer'], subtract=[u'influenza'])



print("========testing==============")
word_algebra(add=[u'brain_cancer', u'medication'], subtract=[u'breast_cancer'])



print("========testing==============")
word_algebra(add=[u'brain_cancer', u'tmz'], subtract=[u'hgg'])


print("========testing==============")

word_algebra(add=[u'breast_cancer', u'treatment'])



print("========testing==============")
word_algebra(add=[u'influenza', u'treatment'])



print("========testing==============")
print(get_related_terms(u'motor_neuron'))


print("========testing==============")
print(get_related_terms(u'hamartoma'))