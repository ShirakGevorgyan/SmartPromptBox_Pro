"""Utilities for extracting and refining Armenian plot sections from long texts.

The helpers are used to:
- extract only the '📜 Սյուժե' (Plot) part from a richer answer,
- sanitize noisy characters/markup,
- optionally send the plot through the LLM for a cleaner Armenian rewrite,
- replace the original plot segment inside the full text.
"""

import re


def extract_plot_only(text: str) -> str:
    """Extract only the '📜 Սյուժե' (Plot) section from a larger Armenian text.

    Uses a regex boundary up to the next known section marker or line.

    Args:
        text: Full answer that contains multiple sections.

    Returns:
        The captured plot text without the heading, or an empty string if missing.
    """
    match = re.search(
        r"📜 Սյուժե՝(.*?)(?:\n[^\n]*?(?:🎭|🎬|🎥|📊|▶️|🎞️|💸|💰|🤔|📢|$))",
        text,
        re.DOTALL,
    )
    return match.group(1).strip() if match else ""


MAX_PLOT_LENGTH = 800


def clean_garbage_from_plot(text: str) -> str:
    """Remove non-Armenian noise, code fragments and technical tokens from plot.

    The cleaning step keeps Armenian letters, digits and basic punctuation,
    and collapses multiple spaces into a single space.

    Args:
        text: Raw plot text (possibly noisy).

    Returns:
        A cleaned plot string suitable for display or LLM refinement.
    """
    text = re.sub(
        r"[^\u0531-\u0587\u0561-\u0587\u0531-\u0556\u0561-\u0587։,։…()\sA-Za-z0-9-]",
        " ",
        text,
    )

    text = re.sub(r"\s{2,}", " ", text).strip()

    return text


def refine_plot_description(raw_text: str, client) -> str:
    """Ask the LLM to rewrite the plot in clear, concise Armenian.

    The function trims, cleans and (if too long) truncates the input before
    sending it to the LLM. It returns the improved text only.

    Args:
        raw_text: Original plot text (may include noise).
        client: An OpenAI-like client with `chat.completions.create(...)`.

    Returns:
        The refined Armenian plot paragraph(s) as plain text.
    """
    raw_text = raw_text.strip()

    cleaned_input = clean_garbage_from_plot(raw_text)

    if len(cleaned_input) > MAX_PLOT_LENGTH:
        cleaned_input = cleaned_input[:MAX_PLOT_LENGTH].rsplit(".", 1)[0] + "։"

    prompt = f"""
Դու սյուժեների խմբագիր ես։

Քեզ կտրվելու է ֆիլմի կամ սերիալի սյուժեն։ Քո խնդիրն է՝

- Գրիր այն գրագետ, պարզ և ընթեռնելի լեզվով
- Հեռացրու անհասկանալի կամ չհամակցված նախադասությունները
- Մի փոխիր իմաստը, միայն բարելավիր ձևակերպումը

Սյուժեն՝
\"\"\"{cleaned_input}\"\"\"

Գրիր միայն բարելավված տարբերակը՝ առանց բացատրություն կամ նշումներ ավելացնելու։
"""
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.5
    )
    return response.choices[0].message.content.strip()


def replace_plot_with_refined(full_text: str, client) -> str:
    """Replace the original plot section inside the full text with its refined version.

    If no plot section is found, the function returns `full_text` unchanged.

    Args:
        full_text: The full multi-section answer.
        client: An OpenAI-like client for refinement.

    Returns:
        The updated `full_text` with the refined plot substituted in place.
    """
    original_plot = extract_plot_only(full_text)
    if not original_plot:
        return full_text

    cleaned_plot = refine_plot_description(original_plot, client)
    return full_text.replace(original_plot, cleaned_plot, 1)
