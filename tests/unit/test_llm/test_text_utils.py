from app.llm.text_utils import (
    extract_plot_only,
    clean_garbage_from_plot,
    refine_plot_description,
    replace_plot_with_refined
)

from unittest.mock import MagicMock

FAKE_TEXT = """
🎥 Վերնագիր (2024)
📜 Սյուժե՝
Մի երիտասարդ ձգտում է փոխել աշխարհը՝ ճանապարհի ընթացքում հանդիպելով տարօրինակ կերպարների։
🎭 Ժանրը՝ Դրամա
📊 IMDb գնահատական՝ 8.2
"""

# ✅ Test extract_plot_only
def test_extract_plot_only():
    plot = extract_plot_only(FAKE_TEXT)
    assert "փոխել աշխարհը" in plot
    assert "ժանրը" not in plot

# ✅ Test clean_garbage_from_plot
def test_clean_garbage_from_plot_removes_garbage():
    dirty = "Սա նորմալ ✅✅ տեքստ է 👻 բայց ունի ###$% technical <> <> նշաններ..."
    cleaned = clean_garbage_from_plot(dirty)
    assert "✅" not in cleaned
    assert "👻" not in cleaned
    assert "<>" not in cleaned
    assert "տեքստ" in cleaned

# ✅ Test refine_plot_description with mocked GPT client
def test_refine_plot_description_mocked():
    raw_plot = "Սա սյուժե է, որը պետք է բարելավվի։"

    # Mock GPT client
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Սա բարելավված սյուժեն է։"))
    ]

    result = refine_plot_description(raw_plot, fake_client)
    assert "բարելավված" in result

# ✅ Test replace_plot_with_refined using fake client and full text
def test_replace_plot_with_refined():
    full_text = """
🎥 Վերնագիր
📜 Սյուժե՝
Սա սյուժե է, որը պետք է բարելավվի։
🎭 Ժանրը՝ Դրամա
"""

    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Սա բարելավված սյուժե է։"))
    ]

    result = replace_plot_with_refined(full_text, fake_client)
    assert "բարելավված սյուժե" in result
    assert "պետք է բարելավվի" not in result
