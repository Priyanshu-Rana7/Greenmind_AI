# GreenMind AI - Local Knowledge Base Retriever (RAG)

import os
import re
import math

class RAGStore:
    def __init__(self, kb_dir="knowledge_base"):
        self.kb_dir = kb_dir
        self.documents = []  # List of dicts: {"source": filename, "text": passage_text}
        self.vocab = set()
        self.doc_vectors = []
        self.idf = {}
        
        # Load and index the knowledge base
        self._load_knowledge_base()
        self._build_index()

    def _clean_text(self, text):
        """Cleans text and converts it into a list of lowercase tokens."""
        text = text.lower()
        # Remove markdown symbols and punctuation
        text = re.sub(r'[^\w\s-]', '', text)
        tokens = text.split()
        # Filter short/common stop words
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "is", "are", "was", "were", "of", "by", "our", "your", "we", "us", "it", "its"}
        return [t for t in tokens if t not in stopwords]

    def _load_knowledge_base(self):
        """Reads all txt files from the knowledge base directory and splits them into logical paragraphs."""
        if not os.path.exists(self.kb_dir):
            return

        for filename in os.listdir(self.kb_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(self.kb_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                        # Split by double newlines or markdown headings to get meaningful chunks
                        # We split by headings to keep heading context, or paragraphs
                        chunks = re.split(r'\n(?=##?\s)', content)
                        
                        for chunk in chunks:
                            chunk_str = chunk.strip()
                            if len(chunk_str) > 100:  # Skip trivial empty blocks
                                # Formulate a friendly source name
                                source_name = filename.replace("_", " ").replace(".txt", "").title()
                                self.documents.append({
                                    "source": source_name,
                                    "text": chunk_str
                                })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def _build_index(self):
        """Builds a TF-IDF index over all documents in memory."""
        if not self.documents:
            return

        # 1. Populate vocabulary and count Term Frequencies (TF) for each document
        doc_tfs = []
        doc_word_counts = []
        
        for doc in self.documents:
            tokens = self._clean_text(doc["text"])
            doc_word_counts.append(len(tokens))
            
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
                self.vocab.add(t)
            doc_tfs.append(tf)

        # 2. Compute Inverse Document Frequency (IDF)
        n_docs = len(self.documents)
        for term in self.vocab:
            # Count how many documents contain this term
            docs_with_term = sum(1 for tf in doc_tfs if term in tf)
            # Log IDF formulation
            self.idf[term] = math.log(1.0 + (n_docs / (1.0 + docs_with_term)))

        # 3. Create document TF-IDF vectors
        for i, tf in enumerate(doc_tfs):
            vector = {}
            for term, freq in tf.items():
                # TF-IDF = TF * IDF
                vector[term] = freq * self.idf[term]
            self.doc_vectors.append(vector)

    def _cosine_similarity(self, vec1, vec2):
        """Computes cosine similarity between two sparse term vectors."""
        intersection = set(vec1.keys()) & set(vec2.keys())
        if not intersection:
            return 0.0
            
        dot_product = sum(vec1[x] * vec2[x] for x in intersection)
        
        sum1 = sum(val**2 for val in vec1.values())
        sum2 = sum(val**2 for val in vec2.values())
        
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
            
        return dot_product / denominator

    def retrieve(self, query, top_k=3):
        """
        Retrieves the top_k most relevant documents/passages matching the query.
        Returns a list of dicts: [{"source": source, "text": text, "score": similarity_score}]
        """
        if not self.documents:
            return []

        # Convert query to TF-IDF vector
        query_tokens = self._clean_text(query)
        query_tf = {}
        for t in query_tokens:
            query_tf[t] = query_tf.get(t, 0) + 1
            
        query_vector = {}
        for term, freq in query_tf.items():
            if term in self.vocab:
                query_vector[term] = freq * self.idf[term]

        if not query_vector:
            # Fallback to returning the first few files if no matching tokens found
            return [{"source": doc["source"], "text": doc["text"], "score": 0.0} for doc in self.documents[:top_k]]

        # Compute similarities
        results = []
        for i, doc_vector in enumerate(self.doc_vectors):
            score = self._cosine_similarity(query_vector, doc_vector)
            results.append({
                "source": self.documents[i]["source"],
                "text": self.documents[i]["text"],
                "score": score
            })

        # Sort by score descending
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results[:top_k]

# Simple test harness
if __name__ == "__main__":
    store = RAGStore()
    print(f"Loaded {len(store.documents)} sections into knowledge base.")
    query = "How to save electricity in hostels?"
    matches = store.retrieve(query, top_k=2)
    for idx, match in enumerate(matches):
        print(f"\nMatch {idx+1} (Score: {match['score']:.3f}) from [{match['source']}]:")
        print(match['text'][:200] + "...")
