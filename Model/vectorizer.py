from sklearn.feature_extraction.text import TfidfVectorizer

class Vectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, token_dict):
        self.filenames = list(token_dict.keys())
        corpus = [' '.join(tokens) for tokens in token_dict.values()]
        matrix = self.vectorizer.fit_transform(corpus)
        return matrix

    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out()

    def get_filename_by_index(self, index):
        return self.filenames[index]
