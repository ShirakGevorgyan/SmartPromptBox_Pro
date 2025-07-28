from unittest.mock import patch, MagicMock
from app.llm import series_picker

# 📌 Մոկված պատասխանը՝ սերիալի բովանդակությամբ
MOCK_SERIES_TEXT = """
🎥 Վերնագիր՝ Breaking Bad (2008)  
🎭 Ժանրը՝ Դրամա  
🎬 Ռեժիսոր՝ Vince Gilligan  
🎭 Դերասաններ՝ Bryan Cranston, Aaron Paul, Anna Gunn, Bob Odenkirk, Dean Norris  
📜 Սյուժե՝ Քիմիայի ուսուցիչը դառնում է մետամֆետամինի արտադրող՝ ֆինանսական խնդիրներից ելնելով։  
📊 IMDb գնահատական՝ 9.5  
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)  
🎞️ Դիտելու հղում՝ [IMDB](https://imdb.com)
"""

# ✅ Test 1: get_random_series_llm
@patch("app.llm.series_picker.replace_plot_with_refined")
@patch("app.llm.series_picker.client")
def test_get_random_series_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_SERIES_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_SERIES_TEXT

    result = series_picker.get_random_series_llm()
    assert "Breaking Bad" in result
    assert "🎭 Ժանրը" in result


# ✅ Test 2: suggest_series_by_description_llm
@patch("app.llm.series_picker.replace_plot_with_refined")
@patch("app.llm.series_picker.client")
def test_suggest_series_by_description_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_SERIES_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_SERIES_TEXT

    result = series_picker.suggest_series_by_description_llm("թմրանյութերի բիզնեսում հայտնված ուսուցիչ")
    assert "Bryan Cranston" in result


# ✅ Test 3: get_series_details_by_name_llm
@patch("app.llm.series_picker.replace_plot_with_refined")
@patch("app.llm.series_picker.client")
def test_get_series_details_by_name_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_SERIES_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_SERIES_TEXT

    result = series_picker.get_series_details_by_name_llm("Breaking Bad")
    assert "Vince Gilligan" in result


# ✅ Test 4: get_series_by_genre_llm
@patch("app.llm.series_picker.replace_plot_with_refined")
@patch("app.llm.series_picker.client")
def test_get_series_by_genre_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_SERIES_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_SERIES_TEXT

    result = series_picker.get_series_by_genre_llm("դրամա")
    assert "🎞️ Դիտելու հղում" in result


# ✅ Test 5: get_top_10_series_llm
@patch("app.llm.series_picker.replace_plot_with_refined")
@patch("app.llm.series_picker.client")
def test_get_top_10_series_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_SERIES_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_SERIES_TEXT

    result = series_picker.get_top_10_series_llm()
    assert "📜 Սյուժե" in result
