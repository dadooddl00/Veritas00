"""Appelants LLM — interfaces API Anthropic et OpenAI-compatible."""

import os
import requests


FEATURE_SYSTEM_PROMPT = """Analyse le prompt utilisateur et retourne UNIQUEMENT un JSON valide.
Tu ne dois produire QUE des CONSTATS sur le texte, jamais de décision de politique
(pas de verification/stakes_level/external_sources — ces champs sont calculés
ailleurs par des règles déterministes, pas par toi).

{
  "truth_apt": true/false,
  "contains_hypothesis": true/false,
  "contains_causal_claim": true/false,
  "contains_causal_question": true/false,
  "contains_quantitative_claim": true/false,
  "is_controversial_topic": true/false,
  "explicit_depth_request": true/false,
  "is_sensitive_topic": true/false,
  "mentions_current_fact": true/false,
  "analysis_confidence": 0.XX,
  "uncertainty_level": 0.XX
}

Distinction importante :
- contains_causal_claim : le texte AFFIRME une relation de cause à effet
  ("le vaccin X cause Y").
- contains_causal_question : le texte DEMANDE une explication
  ("pourquoi le ciel est bleu ?") — ce n'est PAS une affirmation à vérifier.

Réponds exclusivement avec l'objet JSON. Pas de texte, pas de markdown, pas de ```."""


def _extract_json_block(content: str) -> str:
    """Extrait le bloc JSON d'une réponse LLM."""
    start = content.find('{')
    end = content.rfind('}') + 1
    if start < 0 or end <= start:
        raise RuntimeError("Aucun objet JSON trouvé dans la réponse du LLM")
    return content[start:end]


def anthropic_caller(prompt: str, model: str = "claude-sonnet-5") -> str:
    """Format API Anthropic natif : system séparé, header x-api-key,
    endpoint /v1/messages (différent du format OpenAI-compatible)."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Définis ANTHROPIC_API_KEY dans l'environnement")

    payload = {
        "model": model,
        "max_tokens": 700,
        "system": FEATURE_SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": f"Prompt à analyser : {prompt}"}],
        "temperature": 0.1,
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post("https://api.anthropic.com/v1/messages",
                                  json=payload, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur d'appel API Anthropic : {e}") from e

    try:
        content = response.json()["content"][0]["text"]
    except (KeyError, IndexError, ValueError) as e:
        raise RuntimeError(f"Réponse API Anthropic mal formée : {e}") from e

    return _extract_json_block(content)


def openai_compatible_caller(prompt: str, model: str = "grok-3") -> str:
    """Appelant compatible OpenAI (xAI, OpenAI, etc.)."""
    api_key = os.getenv("XAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("API_BASE_URL", "https://api.x.ai/v1")

    if not api_key:
        raise ValueError("Définis XAI_API_KEY ou OPENAI_API_KEY dans l'environnement")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": FEATURE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Prompt à analyser : {prompt}"},
        ],
        "temperature": 0.1,
        "max_tokens": 700,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post(f"{base_url}/chat/completions", json=payload, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Erreur d'appel API : {e}") from e

    try:
        content = response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        raise RuntimeError(f"Réponse API mal formée : {e}") from e

    return _extract_json_block(content)


def llm_caller(prompt: str) -> str:
    """Dispatcher : Anthropic en priorité si sa clé est présente, sinon xAI/OpenAI."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return anthropic_caller(prompt)
    if os.getenv("XAI_API_KEY") or os.getenv("OPENAI_API_KEY"):
        return openai_compatible_caller(prompt)
    raise ValueError("Définis ANTHROPIC_API_KEY, XAI_API_KEY ou OPENAI_API_KEY dans l'environnement")
