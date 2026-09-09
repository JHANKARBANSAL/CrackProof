"""
Rubric padhta hai - yaani "achha answer kaisa hota hai".

Ye facts se alag cheez hai. Facts har topic ke alag hote hain aur
Wikipedia se aate hain. Rubric GENERIC hai - ek hi rubric OOP, DBMS,
OS sab pe lagti hai. Isliye ise dhoondhna nahi padta, har baar
seedha bhej dete hain.

Rubric SOLO Taxonomy (Biggs & Collis, 1982) pe based hai, jo
understanding ki QUALITY naapne ka published framework hai.

File: knowledge/rubrics/solo_rubric.md
Tum ise khol ke edit kar sakti ho. Kuch dobara generate nahi hota.
"""

import os


RUBRIC_FILE = os.path.join("knowledge", "rubrics", "solo_rubric.md")

# Ek baar padh ke yaad rakh lo
_rubric_text = None
_already_read = False


def get_rubric():
    """
    Rubric ka text deta hai.

    File na mile to khaali string, taaki interview ruke nahi.
    """

    global _rubric_text, _already_read

    if _already_read:
        return _rubric_text

    _already_read = True

    if not os.path.exists(RUBRIC_FILE):
        print("  (rubric file nahi mili:", RUBRIC_FILE, ")")
        _rubric_text = ""
        return _rubric_text

    try:
        with open(RUBRIC_FILE) as f:
            content = f.read()

    except Exception as error:
        print("  (rubric padh nahi paya:", error, ")")
        _rubric_text = ""
        return _rubric_text

    # Header comment hata do, model ko uski zaroorat nahi
    if "-->" in content:
        content = content.split("-->", 1)[1]

    _rubric_text = content.strip()

    return _rubric_text
