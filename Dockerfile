# CrackProof - Hugging Face Spaces ke liye
#
# HF Spaces Docker chalata hai. Ye file usko batati hai ki app kaise
# banani aur chalani hai.

FROM python:3.11-slim

# Hugging Face container ko root ke bina chalata hai, isliye ek
# normal user banate hain
RUN useradd -m -u 1000 user
USER user

ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Pehle sirf requirements copy karo.
# Isse Docker inhe cache kar leta hai - code badalne par packages
# dobara install nahi hote, aur build tez rehti hai.
COPY --chown=user requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Ab baaki code
COPY --chown=user . .

# HF Spaces 7860 par sunta hai
ENV PORT=7860

EXPOSE 7860

# Flask ka apna server sirf development ke liye hai, isliye gunicorn.
#
# timeout 180 isliye ki evaluation mein Groq ko kuch second lagte hain
# aur usse pehle worker mara nahi jaana chahiye.
CMD gunicorn server:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 180
