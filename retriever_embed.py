"""
Embedding retriever - matlab se tukde dhoondhne wala.

BM25 shabd match karta hai. Ye meaning match karta hai. Isliye
"reduce redundancy" aur "normalize" ko ye ek jaisa samajh sakta hai,
jabki BM25 ke liye woh do alag shabd hain.

Har tukde ko numbers ki ek lambi list (vector) mein badalte hain.
Do cheezon ka matlab paas-paas ho to unke vectors bhi paas-paas
hote hain. Phir bas naapna hai ki kaunsa vector sawaal ke vector ke
sabse kareeb hai.

Model laptop pe chalta hai (ollama), isliye:
  - koi API key nahi
  - koi quota nahi
  - internet ke bina bhi chalega

Pehli baar chalane pe saare 1884 tukde embed karne padte hain, jisme
kuch minute lagte hain. Uske baad result knowledge/embeddings.json
mein save ho jaata hai aur agli baar turant load ho jaata hai.

Use:
    python3 retriever_embed.py          # pehli baar: embeddings banao
"""

import json
import os
import urllib.request

import numpy

from knowledge_base import load_chunks


EMBEDDINGS_FILE = os.path.join("knowledge", "embeddings.json")

MODEL = "nomic-embed-text"

OLLAMA_URL = "http://localhost:11434/api/embeddings"


def get_embedding(text):
    """
    Ek text ko numbers ki list mein badalta hai.

    Ollama local pe chalta hai, isliye koi key ya quota nahi.
    """

    payload = {
        "model": MODEL,
        "prompt": text,
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as answer:
            data = json.loads(answer.read())

    except urllib.error.HTTPError as error:

        if error.code == 404:
            raise RuntimeError(
                "Ollama ke paas '" + MODEL + "' model nahi hai.\n"
                "Ek baar ye chalao:  ollama pull " + MODEL
            ) from None
        raise

    except urllib.error.URLError:
        raise RuntimeError(
            "Ollama chal nahi raha. Ye chalao:  ollama serve"
        ) from None

    return data["embedding"]


def build_embeddings():
    """
    Saare tukdon ke embeddings banata hai aur file mein save karta hai.

    Ye dheema kaam hai (har tukde ke liye ek call). Isliye ek baar
    karke save kar lete hain.
    """

    chunks = load_chunks()

    if not chunks:
        print("Koi tukda nahi mila. Pehle chalao: python3 knowledge_base.py")
        return None

    print("\n" + str(len(chunks)) + " tukdon ke embeddings bana raha hoon.")
    print("Pehli baar hai isliye time lagega. Ek hi baar karna padta hai.\n")

    vectors = []

    for position in range(len(chunks)):

        # Title aur section bhi jodte hain, taaki tukde ko apna
        # context pata rahe.
        full_text = (
            chunks[position]["title"] + ". "
            + chunks[position]["section"] + ". "
            + chunks[position]["text"]
        )

        vectors.append(get_embedding(full_text))

        done = position + 1

        if done % 100 == 0 or done == len(chunks):
            print("  " + str(done) + " / " + str(len(chunks)))

    with open(EMBEDDINGS_FILE, "w") as f:
        json.dump({"model": MODEL, "vectors": vectors}, f)

    print("\nSave hua:", EMBEDDINGS_FILE)

    return vectors


def load_embeddings():
    """Save kiye hue embeddings padhta hai. Na ho to None deta hai."""

    if not os.path.exists(EMBEDDINGS_FILE):
        return None

    with open(EMBEDDINGS_FILE) as f:
        data = json.load(f)

    return data["vectors"]


class EmbeddingRetriever:
    """
    Interface bilkul BM25Retriever jaisa hai, taaki dono ko ek hi
    tarah se test kar sakein.
    """

    def __init__(self, chunks=None):

        if chunks is None:
            chunks = load_chunks()

        self.chunks = chunks

        vectors = load_embeddings()

        if vectors is None:
            vectors = build_embeddings()

        # numpy array mein daal do, taaki hisaab tez ho
        self.vectors = numpy.array(vectors, dtype="float32")

        # Har vector ki lambai 1 kar do. Iske baad do vectors ka
        # simple dot product hi unki similarity ban jaata hai.
        lengths = numpy.linalg.norm(self.vectors, axis=1, keepdims=True)
        lengths[lengths == 0] = 1
        self.vectors = self.vectors / lengths

    def search(self, question, subject=None, top_k=3):

        question_vector = numpy.array(
            get_embedding(question), dtype="float32"
        )

        length = numpy.linalg.norm(question_vector)

        if length > 0:
            question_vector = question_vector / length

        # Sabhi tukdon se similarity ek saath nikal lo
        scores = self.vectors.dot(question_vector)

        # Kaunse tukdon mein dhoondhna hai
        allowed = list(range(len(self.chunks)))

        if subject:

            wanted = subject.strip().upper()

            matching = []
            for position in allowed:
                if self.chunks[position]["subject"].upper() == wanted:
                    matching.append(position)

            if matching:
                allowed = matching

        pairs = []
        for position in allowed:
            pairs.append((float(scores[position]), position))

        pairs.sort(reverse=True)

        results = []

        for score, position in pairs[:top_k]:
            chunk = dict(self.chunks[position])
            chunk["score"] = round(score, 3)
            results.append(chunk)

        return results


if __name__ == "__main__":

    retriever = EmbeddingRetriever()

    print("\nTukde load hue:", len(retriever.chunks))

    question = "Why do we normalize a database?"

    print("\nSawaal:", question, "\n")

    for result in retriever.search(question, subject="DBMS"):
        print("  score", result["score"],
              "|", result["source_file"],
              "| section:", result["section"])
        print("   ", result["text"][:120].replace("\n", " "), "...")
        print()
