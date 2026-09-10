"""
Sawaal ke liye reference text laata hai.

Ye interview aur knowledge base ke beech ka pul hai. Sabse zaroori
baat: ye kabhi crash nahi karta. Knowledge base na ho, retriever
fail ho jaye, ya kuch match na kare - har haal mein khaali string
lauta deta hai, aur interview bina grounding ke chalta rehta hai.

Use:
    from grounding import get_reference
    text, sources = get_reference(question, topic)
"""

# Retriever ek hi baar banega, phir yaad rakha jayega.
_retriever = None
_tried_to_build = False


def _get_retriever():
    """
    Retriever banata hai. Ek baar fail ho gaya to dobara koshish
    nahi karta, warna har sawaal pe wahi error print hota rahega.
    """

    global _retriever, _tried_to_build

    if _tried_to_build:
        return _retriever

    _tried_to_build = True

    # Pehle embeddings, kyunki test mein woh behtar nikle:
    #   precision 88% vs 70%, useful 92% vs 83% (top 5)
    # Ollama band ho to BM25 pe chala jao - woh bina kisi model ke
    # chalta hai, isliye interview kabhi ruke nahi.
    try:
        from retriever_embed import EmbeddingRetriever

        retriever = EmbeddingRetriever()

        if retriever.chunks:
            _retriever = retriever
            return _retriever

    except Exception as error:
        print("  (embedding retriever nahi chala:", error, ")")
        print("  (BM25 pe ja raha hoon)")

    try:
        from retriever_bm25 import BM25Retriever

        retriever = BM25Retriever()

        if not retriever.chunks:
            print(
                "  (knowledge base khaali hai - "
                "evaluation bina reference ke chalegi)"
            )
            return None

        _retriever = retriever

    except Exception as error:
        print("  (reference nahi mil paya:", error, ")")
        _retriever = None

    return _retriever


def make_section_url(page_url, section):
    """
    Article ke URL mein section ka anchor jod deta hai.

    https://en.wikipedia.org/wiki/Relational_database
      + section "Normalization"
      = https://en.wikipedia.org/wiki/Relational_database#Normalization

    Isse link seedha usi section pe khulta hai, poore article pe nahi.
    "Introduction" hamara apna naam hai (article ki shuruaat ke liye),
    Wikipedia pe aisa koi heading nahi hoti, isliye uska anchor nahi.
    """

    if not page_url:
        return ""

    if not section or section == "Introduction":
        return page_url

    anchor = section.strip().replace(" ", "_")

    return page_url + "#" + anchor


def get_reference(question, topic, top_k=5):
    """
    Sawaal ke liye reference text aur uske sources laata hai.

    Return karta hai (reference_text, sources).

    Kuch na mile to ("", []) - matlab evaluation bina grounding ke
    hogi, jaise pehle hoti thi.
    """

    retriever = _get_retriever()

    if retriever is None:
        return "", []

    try:
        results = retriever.search(question, subject=topic, top_k=top_k)

    except Exception as error:
        print("  (reference dhoondhne mein dikkat:", error, ")")
        return "", []

    if not results:
        return "", []

    parts = []
    sources = []

    number = 0

    for result in results:

        number = number + 1

        # Har tukde ko ek number do. Model sirf ye number bolega,
        # aur URL hum apne data se bharenge - isliye model jhootha
        # link bana hi nahi sakta.
        parts.append(
            "[" + str(number) + "] From \"" + result["title"] + "\""
            + ", section \"" + result["section"] + "\":\n"
            + result["text"]
        )

        sources.append({
            "number": number,
            "chunk_id": result["chunk_id"],
            "title": result["title"],
            "section": result["section"],
            "url": make_section_url(
                result["source"], result["section"]
            ),
            "licence": result.get("licence", ""),
            "score": result["score"],
        })

    return "\n\n---\n\n".join(parts), sources
