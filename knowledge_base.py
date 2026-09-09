"""
knowledge/ ki badi files ko chhote tukdon mein todta hai.

Ye seedha 1500 character gin kar nahi kaatta. Aisa karne se ek
concept beech se tut jaata hai. Iske bajaye:

  1. Pehle file ko SECTIONS mein todo (Wikipedia ke == Heading ==)
  2. Section chhota hai to poora ek tukda ban jaata hai
  3. Bada hai to paragraph pe todo
  4. Paragraph bhi bada ho to sentence pe todo
  5. Har tukde ke aage pichhle tukde ka thoda hissa jod do (overlap),
     taaki border pe koi baat kat na jaye

Har tukda apna section heading bhi yaad rakhta hai, isliye model ko
pata rehta hai ki ye text kis baare mein hai.

Chalane ka tareeka:

    python3 knowledge_base.py

Result knowledge/chunks.json mein save hota hai.
Koi API call nahi, koi download nahi. Sab offline kaam hai.
"""

import json
import os


KNOWLEDGE_DIR = "knowledge"

CHUNKS_FILE = os.path.join(KNOWLEDGE_DIR, "chunks.json")

# Ek tukda kitna bada ho. Grounding test mein ~1800 character ka
# reference kaam kar gaya tha, isliye aas-paas hi rakh rahe hain.
CHUNK_SIZE = 1500

# Pichhle tukde ka itna hissa agle tukde ke shuru mein jodenge.
OVERLAP_SIZE = 200

# Itne se chhota tukda bekaar hai (jaise akela heading).
MIN_CHUNK_SIZE = 200


def read_file_info(path):
    """
    Ek .md file padhta hai aur header ki jaankari alag karta hai.

    Header aisa dikhta hai:

        # Database normalization

        <!--
        source: https://...
        licence: CC BY-SA 4.0 (Wikipedia)
        subject: DBMS
        -->

    Return karta hai ek dictionary.
    """

    with open(path) as f:
        content = f.read()

    info = {
        "title": "",
        "source": "",
        "licence": "",
        "subject": "",
    }

    for line in content.split("\n"):

        clean = line.strip()

        if clean.startswith("# ") and info["title"] == "":
            info["title"] = clean[2:].strip()

        if clean.startswith("source:"):
            info["source"] = clean[len("source:"):].strip()

        if clean.startswith("licence:"):
            info["licence"] = clean[len("licence:"):].strip()

        if clean.startswith("subject:"):
            info["subject"] = clean[len("subject:"):].strip()

    # Header ke baad ka asli text
    if "-->" in content:
        info["text"] = content.split("-->", 1)[1].strip()
    else:
        info["text"] = content.strip()

    return info


def split_into_sections(text):
    """
    Text ko sections mein todta hai.

    Wikipedia ke plain text mein heading aise dikhti hai:
        == Objectives ==
        === Sub heading ===

    Return karta hai list of (heading, body).
    Pehle heading se pehle wale text ka heading "Introduction" hota hai.
    """

    sections = []

    heading = "Introduction"
    body_lines = []

    for line in text.split("\n"):

        clean = line.strip()

        is_heading = (
            clean.startswith("==")
            and clean.endswith("==")
            and len(clean) > 4
        )

        if is_heading:

            # Purana section band karo
            body = "\n".join(body_lines).strip()

            if body != "":
                sections.append((heading, body))

            # Naya section shuru
            heading = clean.strip("= ").strip()
            body_lines = []

        else:
            body_lines.append(line)

    # Aakhri section bhi daal do
    body = "\n".join(body_lines).strip()

    if body != "":
        sections.append((heading, body))

    return sections


def split_by_separator(text, separator):
    """
    Text ko ek separator pe todkar CHUNK_SIZE ke tukde banata hai.

    Tukde tabhi todta hai jab zaroorat ho, warna jodta rehta hai.
    """

    pieces = text.split(separator)

    chunks = []
    current = ""

    for piece in pieces:

        if piece.strip() == "":
            continue

        # Jodne se bada ho jayega? To pehle wala band karo.
        too_big = len(current) + len(piece) + len(separator) > CHUNK_SIZE

        if too_big and current != "":
            chunks.append(current.strip())
            current = piece

        elif current == "":
            current = piece

        else:
            current = current + separator + piece

    if current.strip() != "":
        chunks.append(current.strip())

    return chunks


def split_text(text):
    """
    Text ko tukdon mein todta hai, sabse bade border se shuru karke.

    Pehle paragraph pe todne ki koshish. Agar koi tukda phir bhi bada
    hai to line pe todo. Phir bhi bada ho to sentence pe. Yahi
    "recursive" ka matlab hai - hum halke-halke chhote border pe
    jaate hain, seedhe beech shabd mein nahi kaatte.
    """

    # Chhota hai to todne ki zaroorat hi nahi
    if len(text) <= CHUNK_SIZE:
        return [text.strip()]

    # Sabse bade border se sabse chhote tak.
    # Aakhir mein " " hai - yaani shabd ke beech me. Isse aage nahi
    # jaate, kyunki uske baad shabd hi kat jayega.
    separators = ["\n\n", "\n", ". ", " "]

    chunks = [text]

    for separator in separators:

        new_chunks = []

        for chunk in chunks:

            if len(chunk) <= CHUNK_SIZE:
                new_chunks.append(chunk)
            else:
                new_chunks.extend(split_by_separator(chunk, separator))

        chunks = new_chunks

        # Sab tukde theek size ke ho gaye? To ruk jao.
        still_big = False

        for chunk in chunks:
            if len(chunk) > CHUNK_SIZE:
                still_big = True

        if not still_big:
            break

    return chunks


def add_overlap(chunks):
    """
    Har tukde ke shuru mein pichhle tukde ka aakhri hissa jodta hai.

    Isse border pe koi baat kat kar aadhi nahi rehti. Pehle tukde ke
    aage kuch nahi jodte.
    """

    if len(chunks) < 2:
        return chunks

    with_overlap = [chunks[0]]

    for number in range(1, len(chunks)):

        previous = chunks[number - 1]

        tail = previous[-OVERLAP_SIZE:]

        # Aadhe shabd se shuru na ho, isliye pehle space ke baad se lo
        if " " in tail:
            tail = tail.split(" ", 1)[1]

        with_overlap.append(tail.strip() + " ... " + chunks[number])

    return with_overlap


def make_chunk_id(subject, file_name, section, number):
    """
    Har tukde ka sthir naam.

    Ginti wala id (0, 1, 2...) tab badal jaata hai jab koi nayi file
    add ho. Ye id file aur section pe based hai, isliye nayi file add
    karne se purane ids nahi hilte.
    """

    clean_section = ""

    for letter in section.lower():
        if letter.isalnum():
            clean_section = clean_section + letter
        else:
            clean_section = clean_section + "_"

    while "__" in clean_section:
        clean_section = clean_section.replace("__", "_")

    clean_section = clean_section.strip("_")

    return (
        subject + "/" + file_name
        + "#" + clean_section
        + "#" + str(number)
    )


def build():
    """Saari files padhkar chunks banata hai."""

    all_chunks = []

    for subject in sorted(os.listdir(KNOWLEDGE_DIR)):

        folder = os.path.join(KNOWLEDGE_DIR, subject)

        # Sirf folders chahiye, chunks.json jaisi file nahi
        if not os.path.isdir(folder):
            continue

        for file_name in sorted(os.listdir(folder)):

            if not file_name.endswith(".md"):
                continue

            path = os.path.join(folder, file_name)

            info = read_file_info(path)

            file_subject = info["subject"]

            if file_subject == "":
                file_subject = subject

            sections = split_into_sections(info["text"])

            made = 0

            for heading, body in sections:

                pieces = split_text(body)
                pieces = add_overlap(pieces)

                number = 0

                for piece in pieces:

                    if len(piece) < MIN_CHUNK_SIZE:
                        continue

                    all_chunks.append({
                        "chunk_id": make_chunk_id(
                            file_subject, file_name, heading, number
                        ),
                        "subject": file_subject,
                        "title": info["title"],
                        "section": heading,
                        "source_file": file_name,
                        "source": info["source"],
                        "licence": info["licence"],
                        "text": piece,
                    })

                    number = number + 1
                    made = made + 1

            print("  [" + file_subject + "] " + file_name
                  + " -> " + str(len(sections)) + " sections, "
                  + str(made) + " tukde")

    with open(CHUNKS_FILE, "w") as f:
        json.dump(all_chunks, f, indent=2)

    return all_chunks


def load_chunks():
    """
    chunks.json padhta hai.

    Baaki code ise use karega. File na ho to khaali list deta hai,
    taaki kuch crash na ho.
    """

    if not os.path.exists(CHUNKS_FILE):
        return []

    with open(CHUNKS_FILE) as f:
        return json.load(f)


def main():

    if not os.path.exists(KNOWLEDGE_DIR):
        print("\nknowledge/ folder nahi mila.")
        print("Pehle ye chalao:  python3 corpus_fetcher.py\n")
        return

    print("\nFiles ko section aur paragraph ke hisaab se tod raha hoon...\n")

    chunks = build()

    if not chunks:
        print("\nKoi tukda nahi bana. knowledge/ khaali lagta hai.")
        return

    per_subject = {}
    total_length = 0
    biggest = 0

    for chunk in chunks:
        subject = chunk["subject"]
        per_subject[subject] = per_subject.get(subject, 0) + 1
        total_length = total_length + len(chunk["text"])

        if len(chunk["text"]) > biggest:
            biggest = len(chunk["text"])

    print("\n" + "=" * 45)
    print("Kul tukde:", len(chunks))
    print("")

    for subject in sorted(per_subject):
        print("  " + subject + ": " + str(per_subject[subject]))

    print("")
    print("Average tukda :", int(total_length / len(chunks)), "characters")
    print("Sabse bada    :", biggest, "characters")
    print("Save hua      :", CHUNKS_FILE)
    print("=" * 45 + "\n")


if __name__ == "__main__":
    main()
