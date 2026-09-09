"""
The single place the whole project talks to a language model.

Every prompt in CrackProof goes through ask_llm(). Switching provider
is therefore a one-line change in .env, and nothing else in the project
needs to know which model answered.

Set the provider in .env:

    LLM_PROVIDER=groq       free, thousands of requests/day, gpt-oss-120b
    LLM_PROVIDER=gemini     free tier is only 20 requests/day
    LLM_PROVIDER=ollama     runs on this laptop, unlimited, works offline
"""

import json
import os
import time

from dotenv import load_dotenv


load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()


# Default model per provider. Override in .env with LLM_MODEL if needed.
DEFAULT_MODELS = {
    "groq": "openai/gpt-oss-120b",
    "gemini": "gemini-2.5-flash",
    "ollama": "qwen3:8b",
}

MODEL = os.getenv("LLM_MODEL", "").strip() or DEFAULT_MODELS.get(PROVIDER)


# Filled in lazily so we only build the client we actually use, and so
# a missing key for an unused provider never breaks the project.
_client = None


def _quota_message():
    print("\n  The daily quota for this provider is finished.")
    print("  Options: wait for the reset, enable billing, or switch")
    print("  provider in .env (LLM_PROVIDER=groq / gemini / ollama).")


# =========================================================
# PROVIDERS
#
# Each returns a plain string. When a schema is given it must return
# JSON text matching that schema; ask_llm() does the parsing.
# =========================================================

def _strict_json_schema(node):
    """
    Make a Pydantic JSON schema acceptable to strict mode.

    Strict structured output requires every object in the schema,
    including nested definitions like DepthEvidence, to say
    additionalProperties: false and to list all of its properties as
    required. Pydantic does not add those, so we walk the schema and
    add them.
    """

    if isinstance(node, dict):

        if node.get("type") == "object" and "properties" in node:
            node["additionalProperties"] = False
            node["required"] = list(node["properties"].keys())

        for value in node.values():
            _strict_json_schema(value)

    elif isinstance(node, list):
        for item in node:
            _strict_json_schema(item)

    return node


def _call_groq(prompt, schema):

    global _client

    if _client is None:

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. Get a free key at "
                "https://console.groq.com and add it to .env"
            )

        # Groq speaks the OpenAI protocol, so the openai package works.
        from openai import OpenAI

        _client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    kwargs = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    if schema is not None:
        kwargs["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": schema.__name__,
                "schema": _strict_json_schema(
                    schema.model_json_schema()
                ),
                "strict": True,
            },
        }

    response = _client.chat.completions.create(**kwargs)

    return response.choices[0].message.content


def _call_gemini(prompt, schema):

    global _client

    if _client is None:

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. Add it to your .env file."
            )

        from google import genai

        _client = genai.Client(api_key=api_key)

    from google.genai import types

    config = None

    if schema is not None:
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        )

    response = _client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config
    )

    # Gemini parses the schema itself, so hand back JSON text and let
    # ask_llm() do the same parsing step as every other provider.
    if schema is not None and response.parsed is not None:
        return response.parsed.model_dump_json()

    return response.text


def _call_ollama(prompt, schema):

    # Ollama runs locally and needs no key at all.
    import urllib.request

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    }

    if schema is not None:
        payload["format"] = schema.model_json_schema()

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as connection:
            body = json.loads(connection.read())

    except urllib.error.HTTPError as error:

        if error.code == 404:
            raise RuntimeError(
                f"Ollama does not have the model '{MODEL}'. "
                f"Download it once with:  ollama pull {MODEL}"
            ) from None

        raise

    except urllib.error.URLError:
        raise RuntimeError(
            "Ollama is not running. Start it with:  ollama serve"
        ) from None

    return body.get("response")


PROVIDERS = {
    "groq": _call_groq,
    "gemini": _call_gemini,
    "ollama": _call_ollama,
}


# =========================================================
# THE ONE FUNCTION THE REST OF THE PROJECT USES
# =========================================================

def ask_llm(prompt, schema=None, retries=3):
    """
    Send one prompt to whichever provider .env selects.

    schema=None  -> returns plain text
    schema=Model -> returns that Pydantic model, already parsed

    Returns None if it fails every time. It NEVER raises, so a bad
    network moment or an exhausted quota can no longer crash the
    interview and throw away answers the candidate already gave.
    """

    call = PROVIDERS.get(PROVIDER)

    if call is None:
        print(
            f"\n  Unknown LLM_PROVIDER '{PROVIDER}'. "
            f"Use one of: {', '.join(PROVIDERS)}"
        )
        return None

    for attempt in range(1, retries + 1):

        try:
            raw = call(prompt, schema)

            if raw is None or not str(raw).strip():
                raise ValueError("The model returned an empty response")

            if schema is None:
                return str(raw).strip()

            return schema.model_validate_json(raw)

        except Exception as error:

            message = str(error)

            is_rate_limited = (
                "RESOURCE_EXHAUSTED" in message or "429" in message
            )

            # A DAILY quota will not clear in a few seconds, so stop.
            # A per-minute rate limit will, so wait longer and retry.
            if is_rate_limited:

                lowered = message.lower()

                daily = (
                    "per day" in lowered
                    or "perday" in lowered
                    or "requestsperday" in lowered
                )

                if daily:
                    _quota_message()
                    return None

                print(
                    f"  {PROVIDER} rate limit hit, "
                    f"waiting before retry {attempt} of {retries}"
                )

                if attempt < retries:
                    time.sleep(20)
                    continue

                _quota_message()
                return None

            # A missing key will not fix itself either.
            if "not found" in message and "_API_KEY" in message:
                print(f"\n  {message}")
                return None

            print(
                f"  {PROVIDER} call failed "
                f"(attempt {attempt} of {retries}): {message[:200]}"
            )

            if attempt < retries:
                time.sleep(2)

    return None


def describe():
    """One line saying which model is actually being used."""
    return f"{PROVIDER} / {MODEL}"
