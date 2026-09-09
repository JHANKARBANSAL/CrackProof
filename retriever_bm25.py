"""
BM25 - shabdon ke aadhaar pe tukde dhoondhne wala.

Ye samajhna aasan hai: jo tukda sawaal ke shabd zyada baar use karta
hai, woh upar aata hai. Par ek zaroori twist hai - jo shabd har jagah
aata hai (jaise "the", "data") uski keemat kam, aur jo kam jagah aata
hai (jaise "deadlock", "1NF") uski keemat zyada.

Koi model, koi download, koi API nahi. Sirf ginti.

Use:
    from retriever_bm25 import BM25Retriever
    r = BM25Retriever()
    results = r.search("Why do we normalize a database?", subject="DBMS")
"""

import math
import re

from knowledge_base import load_chunks


# BM25 ke do standard settings.
# K1 - ek shabd bar-bar aane se score kitna badhe (saturation).
# B  - lambe tukdon ko kitna neeche kiya jaye.
K1 = 1.5
B = 0.75


def tokenize(text):
    """
    Text ko chhote shabdon mein todta hai.

    Sab lowercase, aur sirf letters/numbers rakhte hain. Isse
    "ACID," aur "acid" ek hi maane jaate hain.
    """

    text = text.lower()

    # Jo letter ya number nahi hai use space bana do
    cleaned = re.sub(r"[^a-z0-9]+", " ", text)

    return cleaned.split()


class BM25Retriever:

    def __init__(self, chunks=None):

        if chunks is None:
            chunks = load_chunks()

        self.chunks = chunks

        # Har tukde ke shabd pehle se nikal ke rakh lo,
        # taaki har search pe dobara na karna pade.
        self.words_per_chunk = []
        self.counts_per_chunk = []
        self.lengths = []

        for chunk in chunks:

            # Section heading aur title bhi jodte hain, kyunki unme
            # topic ka naam hota hai jo dhoondhne mein madad karta hai.
            full_text = (
                chunk["title"] + " "
                + chunk["section"] + " "
                + chunk["text"]
            )

            words = tokenize(full_text)

            counts = {}
            for word in words:
                counts[word] = counts.get(word, 0) + 1

            self.words_per_chunk.append(words)
            self.counts_per_chunk.append(counts)
            self.lengths.append(len(words))

        if self.lengths:
            self.average_length = sum(self.lengths) / len(self.lengths)
        else:
            self.average_length = 0

        # Har shabd kitne tukdon mein aata hai
        self.chunks_with_word = {}

        for counts in self.counts_per_chunk:
            for word in counts:
                self.chunks_with_word[word] = (
                    self.chunks_with_word.get(word, 0) + 1
                )

        self.total_chunks = len(chunks)

    def idf(self, word):
        """
        Shabd kitna khaas hai.

        Har jagah milne wala shabd -> kam value.
        Kam jagah milne wala shabd -> zyada value.
        """

        seen_in = self.chunks_with_word.get(word, 0)

        if seen_in == 0:
            return 0.0

        top = self.total_chunks - seen_in + 0.5
        bottom = seen_in + 0.5

        return math.log(1 + top / bottom)

    def score_chunk(self, position, query_words):
        """Ek tukde ka score nikalta hai."""

        counts = self.counts_per_chunk[position]
        length = self.lengths[position]

        score = 0.0

        for word in query_words:

            if word not in counts:
                continue

            times = counts[word]

            top = times * (K1 + 1)

            bottom = times + K1 * (
                1 - B + B * length / self.average_length
            )

            score = score + self.idf(word) * (top / bottom)

        return score

    def search(self, question, subject=None, top_k=3):
        """
        Sawaal ke sabse milte-julte tukde deta hai.

        subject diya ho to sirf usi subject mein dhoondhta hai. Woh
        subject na mile to poore corpus mein dhoondh leta hai, taaki
        khaali haath na lautein.
        """

        query_words = tokenize(question)

        # Kaunse tukdon mein dhoondhna hai
        allowed = range(len(self.chunks))

        if subject:

            wanted = subject.strip().upper()

            matching = []
            for position in range(len(self.chunks)):
                if self.chunks[position]["subject"].upper() == wanted:
                    matching.append(position)

            # Subject mila to usi mein dhoondo, warna sab mein
            if matching:
                allowed = matching

        scored = []

        for position in allowed:
            score = self.score_chunk(position, query_words)
            if score > 0:
                scored.append((score, position))

        scored.sort(reverse=True)

        results = []

        for score, position in scored[:top_k]:
            chunk = dict(self.chunks[position])
            chunk["score"] = round(score, 3)
            results.append(chunk)

        return results


if __name__ == "__main__":

    retriever = BM25Retriever()

    print("\nTukde load hue:", len(retriever.chunks))

    question = "Why do we normalize a database?"

    print("\nSawaal:", question, "\n")

    for result in retriever.search(question, subject="DBMS"):
        print("  score", result["score"],
              "|", result["source_file"],
              "| section:", result["section"])
        print("   ", result["text"][:120].replace("\n", " "), "...")
        print()
