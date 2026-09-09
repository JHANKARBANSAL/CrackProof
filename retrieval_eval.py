"""
Retriever kitna achha hai - ye naapta hai.

test_queries.json mein har sawaal ke saath likha hai ki uska jawab
kis file mein hona chahiye. Ye script check karta hai ki retriever
ne top-K results mein woh file laayi ya nahi.

Do numbers nikalte hain:

  recall@k  - kitne sawaalon mein sahi file top-k mein aayi
  hit rate  - kitne results mein se sahi file wale the

Use:
    python3 retrieval_eval.py
"""

import json


TEST_FILE = "test_queries.json"


def load_test_queries():

    with open(TEST_FILE) as f:
        return json.load(f)


def evaluate(retriever, name, top_k=3, use_subject=True, show=True):
    """
    Ek retriever ko test set pe chalata hai aur score deta hai.

    retriever ke paas .search(question, subject, top_k) hona chahiye.
    """

    queries = load_test_queries()

    hits = 0
    useful_chunks = 0
    total_correct_results = 0
    total_results = 0

    misses = []

    for query in queries:

        subject = query["subject"] if use_subject else None

        results = retriever.search(
            query["question"],
            subject=subject,
            top_k=top_k
        )

        found_files = []
        for result in results:
            found_files.append(result["source_file"])

        expected = query["expected_files"]

        # Kitne results sahi file se the
        correct_here = 0
        for file_name in found_files:
            if file_name in expected:
                correct_here = correct_here + 1

        total_correct_results = total_correct_results + correct_here
        total_results = total_results + len(found_files)

        # Kya kam se kam ek sahi file aayi?
        if correct_here > 0:
            hits = hits + 1
        else:
            misses.append({
                "question": query["question"],
                "expected": expected,
                "got": found_files,
            })

        # ASLI SAWAAL: laaye hue tukde mein jawab hai bhi ya nahi?
        # Sahi file aa jaana kaafi nahi - galat section aa sakta hai.
        wanted_words = query.get("expected_keywords", [])

        if wanted_words:

            all_text = ""
            for result in results:
                all_text = all_text + " " + result["text"].lower()

            found_words = 0
            for word in wanted_words:
                if word.lower() in all_text:
                    found_words = found_words + 1

            # Aadhe se zyada keyword mil gaye to tukda kaam ka hai
            if found_words >= (len(wanted_words) + 1) // 2:
                useful_chunks = useful_chunks + 1

    recall = hits / len(queries) if queries else 0
    usefulness = useful_chunks / len(queries) if queries else 0
    precision = (
        total_correct_results / total_results if total_results else 0
    )

    if show:

        print("\n" + "=" * 55)
        print(name + "   (top " + str(top_k)
              + ", subject filter: " + str(use_subject) + ")")
        print("=" * 55)

        print("  recall@" + str(top_k) + " : "
              + str(hits) + "/" + str(len(queries))
              + "  = " + str(round(recall * 100)) + "%")

        print("  precision  : "
              + str(total_correct_results) + "/" + str(total_results)
              + "  = " + str(round(precision * 100)) + "%")

        print("  USEFUL     : "
              + str(useful_chunks) + "/" + str(len(queries))
              + "  = " + str(round(usefulness * 100)) + "%"
              + "   (tukde mein asli jawab tha?)")

        if misses:
            print("\n  Ye sawaal miss hue:")
            for miss in misses:
                print("\n    Q: " + miss["question"][:80])
                print("    chahiye tha : " + ", ".join(miss["expected"]))
                print("    mila        : " + ", ".join(miss["got"]))

    return {
        "name": name,
        "recall": recall,
        "precision": precision,
        "usefulness": usefulness,
        "hits": hits,
        "total": len(queries),
    }


def main():

    from retriever_bm25 import BM25Retriever
    from retriever_embed import EmbeddingRetriever

    print("\nBM25 taiyaar kar raha hoon...")
    bm25 = BM25Retriever()
    print("Tukde:", len(bm25.chunks))

    print("\nEmbedding retriever taiyaar kar raha hoon...")
    dense = EmbeddingRetriever()

    scores = []

    scores.append(evaluate(bm25, "BM25     ", top_k=3))
    scores.append(evaluate(dense, "EMBEDDING", top_k=3))
    scores.append(evaluate(bm25, "BM25     ", top_k=5, show=False))
    scores.append(evaluate(dense, "EMBEDDING", top_k=5, show=False))

    print("\n\n" + "=" * 55)
    print("SUMMARY")
    print("=" * 55)

    for score in scores:
        print("  " + score["name"]
              + "  recall " + str(round(score["recall"] * 100)) + "%"
              + "  precision " + str(round(score["precision"] * 100)) + "%"
              + "  USEFUL " + str(round(score["usefulness"] * 100)) + "%")


if __name__ == "__main__":
    main()
