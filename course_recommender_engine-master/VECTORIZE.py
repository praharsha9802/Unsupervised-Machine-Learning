import nltk
from gensim.models import Word2Vec

class Vectorize():

    def join_corpus(self, corpus, col_name):
        joined_corpus = ''
        for i in corpus[col_name]:
            if i==None:
                continue
            joined_corpus = joined_corpus + ' '.join(i)
        return joined_corpus

    def w2v(self, corpus, col_name):
        corpus = self.join_corpus(corpus, col_name)
        w2vModel = Word2Vec(
            min_count = 2, window = 5, sg = 1,
            hs = 0,negative =5, alpha=0.03,
            min_alpha=0.0007,seed = 19
        )
        w2vModel.build_vocab(
            sentences = [nltk.word_tokenize(sent) for sent in corpus.split('.')],
            progress_per=200
        )
        w2vModel.train(
            corpus,
            total_examples = w2vModel.corpus_count,
            epochs=10
        )
        vectorized = w2vModel[w2vModel.wv.vocab]
        return vectorized