import os.path
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
from nltk.tokenize import word_tokenize
import re


class Similarity:
    def __init__(self, orig_html, html, d2v):
        nltk.download('punkt')
        self.data = self.html2list(text=orig_html)
        self.data2 = self.html2list(text=html)
        self.d2v = d2v
        self.synchronize = [[0.0 for _ in range(len(self.data2))] for _ in range(len(self.data))]
        self.tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()),
                                           tags=[str(i)]) for i, _d in enumerate(self.data)]
        self.max_epochs = 100
        self.vec_size = 20
        self.alpha = 0.025
        self.model = Doc2Vec(vector_size=self.vec_size,
                             alpha=self.alpha,
                             min_alpha=0.00025,
                             min_count=1,
                             dm=1)
        self.model.build_vocab(self.tagged_data)

    def html2list(self, text):
        result = re.findall(r"<p>(.*?)</p>", text, flags=re.DOTALL | re.UNICODE)
        return result

    def train(self):
        if os.path.exists(self.d2v):
            self.model = Doc2Vec.load(self.d2v)
            print("d2v model loaded")
        else:
            for epoch in range(self.max_epochs):
                print('iteration {0}'.format(epoch))
                self.model.train(self.tagged_data,
                                 total_examples=self.model.corpus_count,
                                 epochs=20)
                self.model.alpha -= 0.0002
                self.model.min_alpha = self.model.alpha
            self.model.save(self.d2v)
            print("d2v model saved")
        i = 0
        j = 0
        for d in self.data2:
            self.test_data = word_tokenize(d.lower())
            self.v1 = self.model.infer_vector(self.test_data, epochs=100)
            self.similar_doc = self.model.docvecs.most_similar([self.v1], topn=10)
            for s in self.similar_doc:
                self.synchronize[int(s[0])][i] = s[1]
                j += 1
            print(f"i={i}")
            i += 1
        print("j=" + str(j))
        self.synchronize = np.asarray(self.synchronize, dtype=np.float)
        return self.synchronize, self.data, self.data2

    def output_sentences(self, most_similar):
        for label, index in [('MOST', 0), ('SECOND-MOST', 1),
                             ('MEDIAN', len(most_similar) // 2),
                             ('LEAST', len(most_similar) - 1)]:
            print(u'%s %s: %s\n' % (label, most_similar[index][1], self.data[int(most_similar[index][0])]))
