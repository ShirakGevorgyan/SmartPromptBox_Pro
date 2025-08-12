import re


def extract_plot_only(text: str) -> str:
    """
    Վերհանում է միայն 📜 Սյուժե հատվածը ամբողջական տեքստից։
    """
    match = re.search(
        r"📜 Սյուժե՝(.*?)(?:\n[^\n]*?(?:🎭|🎬|🎥|📊|▶️|🎞️|💸|💰|🤔|📢|$))",
        text,
        re.DOTALL,
    )
    return match.group(1).strip() if match else ""


MAX_PLOT_LENGTH = 800


def clean_garbage_from_plot(text: str) -> str:
    """
    Հանում է անկապ տեքստը՝ ոչ հայերեն սիմվոլներ, կոդային հատվածներ և տեխնիկական արտահայտություններ
    """
    text = re.sub(
        r"[^\u0531-\u0587\u0561-\u0587\u0531-\u0556\u0561-\u0587։,։…()\sA-Za-z0-9-]",
        " ",
        text,
    )

    text = re.sub(r"\s{2,}", " ", text).strip()

    return text


def refine_plot_description(raw_text: str, client) -> str:
    """
    Վերաձևակերպում է սյուժեն պարզ ու գեղեցիկ հայերենով։
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
    """
    Փոխարինում է 📜 Սյուժե հատվածը՝ բարելավված տարբերակով, ամբողջական պատասխանում։
    """
    original_plot = extract_plot_only(full_text)
    if not original_plot:
        return full_text

    cleaned_plot = refine_plot_description(original_plot, client)
    return full_text.replace(original_plot, cleaned_plot, 1)
