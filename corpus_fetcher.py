"""
Wikipedia se knowledge base download karta hai.

Chalane ka tareeka:

    python3 corpus_fetcher.py

Har article yahan save hoga:
    knowledge/<SUBJECT>/<article>.md

File ke upar source URL aur licence likha hota hai, kyunki Wikipedia
ka text CC BY-SA hai aur attribution dena zaroori hai.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request

from corpus_topics import TOPICS


KNOWLEDGE_DIR = "knowledge"

USER_AGENT = "CrackProof/0.1 (student project, local use)"


def make_filename(title):
    """
    "Class (computer programming)"  ->  "class_computer_programming.md"
    """

    name = ""

    for letter in title:
        if letter.isalnum():
            name = name + letter
        else:
            name = name + "_"

    # Ek se zyada underscore ko ek bana do
    while "__" in name:
        name = name.replace("__", "_")

    return name.strip("_").lower() + ".md"


def download_article(title):
    """
    Ek article ka text laata hai.

    Return karta hai (text, url).
    Agar article na mile to (None, None).
    """

    # Wikipedia ka public API. Ye scraping nahi hai.
    settings = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": "1",   # HTML nahi, seedha text do
        "redirects": "1",     # purane naam ko naye pe bhej do
        "titles": title,
    }

    url = "https://en.wikipedia.org/w/api.php?"
    url = url + urllib.parse.urlencode(settings)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    with urllib.request.urlopen(request, timeout=30) as answer:
        data = json.loads(answer.read())

    pages = data["query"]["pages"]

    # API ek hi page bhejta hai, par dictionary ke andar
    for page in pages.values():

        if "extract" not in page:
            return None, None

        real_title = page["title"]

        link = real_title.replace(" ", "_")
        link = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(link)

        return page["extract"], link

    return None, None


def remove_reference_sections(text):
    """
    "See also", "References" jaise sections hata deta hai.
    Inme padhne layak kuch nahi hota.
    """

    unwanted = [
        "see also", "references", "external links",
        "further reading", "notes", "bibliography",
    ]

    good_lines = []
    skipping = False

    for line in text.split("\n"):

        clean_line = line.strip()

        # Wikipedia heading aise dikhta hai:  == Heading ==
        is_heading = (
            clean_line.startswith("==")
            and clean_line.endswith("==")
        )

        if is_heading:
            heading_name = clean_line.strip("= ").lower()
            skipping = heading_name in unwanted

        if not skipping:
            good_lines.append(line)

    return "\n".join(good_lines).strip()


def save_article(subject, title, text, url):
    """File mein likhta hai aur path return karta hai."""

    folder = os.path.join(KNOWLEDGE_DIR, subject)
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, make_filename(title))

    top = (
        "# " + title + "\n\n"
        "<!--\n"
        "source: " + url + "\n"
        "licence: CC BY-SA 4.0 (Wikipedia)\n"
        "subject: " + subject + "\n"
        "-->\n\n"
    )

    with open(path, "w") as f:
        f.write(top + text + "\n")

    return path


def main():

    # Normally hum sirf naye articles download karte hain.
    # Sab kuch dobara chahiye to:  python3 corpus_fetcher.py --refresh
    refresh = "--refresh" in sys.argv

    if refresh:
        print("\n--refresh diya hai: saare articles dobara aayenge\n")
    else:
        print("\nSirf naye articles download honge.")
        print("Sab dobara chahiye to:  python3 corpus_fetcher.py --refresh\n")

    saved = 0
    skipped = 0
    not_found = []

    for subject in TOPICS:

        for title in TOPICS[subject]:

            # Ye file pehle se hai kya?
            path = os.path.join(
                KNOWLEDGE_DIR,
                subject,
                make_filename(title)
            )

            if os.path.exists(path) and not refresh:
                skipped = skipped + 1
                continue

            print("  [" + subject + "] " + title + " ... ", end="")

            # Wikipedia kabhi-kabhi beech mein rok deta hai.
            # 3 baar koshish karo, beech mein thoda ruk ke.
            text = None
            url = None
            problem = None

            for koshish in range(3):

                try:
                    text, url = download_article(title)
                    problem = None
                    break

                except Exception as error:
                    problem = error
                    time.sleep(3)

            if problem is not None:
                print("FAILED:", problem)
                not_found.append(subject + " / " + title)
                continue

            if text is None:
                print("NOT FOUND")
                not_found.append(subject + " / " + title)
                continue

            text = remove_reference_sections(text)

            path = save_article(subject, title, text, url)

            saved = saved + 1
            print(len(text), "chars ->", path)

            # Wikipedia ke server pe zyada bojh mat daalo
            time.sleep(1)

    print("")
    print("  Naye download hue :", saved)
    print("  Pehle se the      :", skipped, "(dobara download nahi kiye)")
    print("  Folder            :", KNOWLEDGE_DIR + "/")

    if not_found:
        print("\nYe nahi mile (corpus_topics.py mein naam theek karo):")
        for item in not_found:
            print("  ", item)


if __name__ == "__main__":
    main()
