import numpy as np
import warnings
from package.nlp.embedding import Embedding
from gensim.models import FastText as fText
from sklearn.metrics.pairwise import cosine_similarity

warnings.simplefilter(action='ignore', category=UserWarning)


class TextRank4Sentence:
    fasttext = fText.load_fasttext_format('./data/duplicate.cbow')

    def __init__(self, damping=0.85, tol=1e-6, window_size=1, stride=1,
                 dim=300):
        self.damping = damping
        self.tol = tol
        self.window_size = window_size
        self.stride = stride
        self.dim = dim
        self.embedding = Embedding(model=self.fasttext,
                                   max_len=self.window_size,
                                   dim=self.dim, return_result=1,
                                   save_result=0
                                   )
        self.segmented_text = []

    def pagerank(self, transition_matrix):
        pr = np.ones(len(transition_matrix)).reshape(-1, 1) / len(
            transition_matrix)

        while True:
            pr_new = self.damping * np.dot(transition_matrix.T, pr) + \
                     (1 - self.damping) * np.ones(
                len(transition_matrix)).reshape(-1, 1) / len(pr)

            delta = np.sum([abs(i - j) for i, j in zip(pr_new, pr)])
            if delta <= self.tol * len(pr):
                return pr_new

            pr = pr_new

    def segment_text(self, text):
        words = text.split()
        verbatim = []
        i = 0
        while (i + 1) < len(words):
            verbatim.append(' '.join(words[i:i + self.window_size]))
            i += self.stride

        self.segmented_text = np.array(verbatim)
        return self.segmented_text

    def calculate_similarity(self, text):
        sim_mat = np.zeros([len(text), len(text)])

        for i in range(len(text)):
            for j in range(len(text)):
                if i != j:
                    temp_1 = \
                        self.embedding.transform_text_to_vector(
                            [], text[i]).mean(axis=0).reshape(1, self.dim)
                    temp_2 = \
                        self.embedding.transform_text_to_vector(
                            [], text[j]).mean(axis=0).reshape(1, self.dim)

                    sim_mat[i][j] = cosine_similarity(temp_1, temp_2)[0, 0]

        return sim_mat

    @staticmethod
    def normalize_matrix(matrix):
        # Normalize matrix by column
        norm = np.sum(matrix, axis=0)
        # this is ignore the 0 element in norm
        matrix = np.divide(matrix, norm, where=norm != 0)
        return matrix

    def rank_words(self, scores):
        ranked_words = sorted(
            ((scores[k], s) for k, s in enumerate(self.segmented_text)),
            reverse=True
        )
        return ranked_words

    def summarize(self, text):
        temp = self.segment_text(text)
        temp = self.calculate_similarity(temp)
        temp = self.normalize_matrix(temp)
        temp = self.pagerank(temp)
        temp = self.rank_words(temp)
        return temp




