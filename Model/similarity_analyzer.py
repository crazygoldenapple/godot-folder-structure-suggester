from sklearn.metrics.pairwise import cosine_similarity

class SimilarityAnalyzer:
    def __init__(self, vector_matrix, vectorizer):
        self.matrix = vector_matrix
        self.vectorizer = vectorizer
        self.similarity_matrix = cosine_similarity(self.matrix)

    def top_k_similar_files(self, k=5, threshold=0.3):
        n = self.similarity_matrix.shape[0]
        results = []

        for i in range(n):
            for j in range(i + 1, n):
                sim = self.similarity_matrix[i][j]
                if sim >= threshold:
                    file_i = self.vectorizer.get_filename_by_index(i)
                    file_j = self.vectorizer.get_filename_by_index(j)
                    results.append((sim, file_i, file_j))

        results.sort(reverse=True, key=lambda x: x[0])
        return results[:k]
