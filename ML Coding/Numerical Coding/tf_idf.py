"""
Implement TF-IDF (Term Frequency-Inverse Document Frequency)
Task: Implement TF-IDF (Term Frequency-Inverse Document Frequency)
Your task is to implement a function that computes the TF-IDF scores for a query against a given corpus of documents.

Write a function compute_tf_idf(corpus, query) that takes the following inputs:

corpus: A list of documents, where each document is a list of words.
query: A list of words for which you want to compute the TF-IDF scores.
The function should return a list of lists containing the TF-IDF scores for the query words in each document, rounded to five decimal places.

Example
Example:
import numpy as np

corpus = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "chased", "the", "cat"],
    ["the", "bird", "flew", "over", "the", "mat"]
]
query = ["cat"]

print(compute_tf_idf(corpus, query))

# Expected Output:
# [[0.21461], [0.25754], [0.0]]
"""

import numpy as np

def compute_tf_idf(corpus, query):
    """
    Compute TF-IDF scores for a query against a corpus of documents using only NumPy.
    The output TF-IDF scores retain five decimal places.
    """
    vocab = sorted(set(word for document in corpus for word in document).union(query))
    word_to_index = {word: idx for idx, word in enumerate(vocab)}

    tf = np.zeros((len(corpus), len(vocab)))

    for doc_idx, document in enumerate(corpus):
        for word in document:
            word_idx = word_to_index[word]
            tf[doc_idx, word_idx] += 1
        tf[doc_idx, :] /= len(document)

    df = np.count_nonzero(tf > 0, axis=0)

    num_docs = len(corpus)
    idf = np.log((num_docs + 1) / (df + 1)) + 1

    tf_idf = tf * idf

    query_indices = [word_to_index[word] for word in query]
    tf_idf_scores = tf_idf[:, query_indices]

    tf_idf_scores = np.round(tf_idf_scores, 5)

    return tf_idf_scores.tolist()
