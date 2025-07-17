from sklearn.cluster import KMeans

class ClusteringEngine:
    def __init__(self, matrix, vectorizer):
        self.matrix = matrix
        self.vectorizer = vectorizer

    def cluster(self, k=6):
        self.model = KMeans(n_clusters=k, random_state=42)
        self.labels = self.model.fit_predict(self.matrix)
        return self._group_files_by_cluster()

    def _group_files_by_cluster(self):
        grouped = {}
        for idx, label in enumerate(self.labels):
            fname = self.vectorizer.get_filename_by_index(idx)
            grouped.setdefault(label, []).append(fname)
        return grouped

    def get_top_keywords_per_cluster(self, top_n=5):
        keywords = self.vectorizer.get_feature_names()
        centroids = self.model.cluster_centers_
        cluster_keywords = {}

        for i, center in enumerate(centroids):
            top_indices = center.argsort()[-top_n:][::-1]
            top_words = [keywords[idx] for idx in top_indices]
            cluster_keywords[i] = top_words

        return cluster_keywords
