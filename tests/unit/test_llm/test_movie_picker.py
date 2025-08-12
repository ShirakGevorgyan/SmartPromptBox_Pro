from unittest.mock import patch, MagicMock
from app.llm import movie_picker


MOCK_MOVIE_TEXT = """
🎥 Վերնագիր` Interstellar (2014)
🎭 Ժանրը՝ Գիտաֆանտաստիկա
🎬 Ռեժիսոր՝ Christopher Nolan
🎭 Դերասաններ՝ Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine, Matt Damon
📜 Սյուժե՝ Մարդկությունը փրկելու առաքելությամբ ուղարկված խումբը ճանապարհվում է միջաստղային ճանապարհորդության։
📊 IMDb գնահատական՝ 8.6
▶️ Տրեյլեր՝ [Դիտել YouTube-ում](https://youtube.com)
🎞️ Դիտելու հղում՝ [IMDB](https://imdb.com)
"""


@patch("app.llm.movie_picker.replace_plot_with_refined")
@patch("app.llm.movie_picker.client")
def test_get_random_movie_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_MOVIE_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_MOVIE_TEXT

    result = movie_picker.get_random_movie_llm()
    assert "Interstellar" in result
    assert "🎭 Ժանրը" in result


@patch("app.llm.movie_picker.replace_plot_with_refined")
@patch("app.llm.movie_picker.client")
def test_suggest_movies_by_description_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_MOVIE_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_MOVIE_TEXT

    result = movie_picker.suggest_movies_by_description_llm(
        "մի տխուր բայց հուսադրող ֆիլմ"
    )
    assert "Matthew McConaughey" in result


@patch("app.llm.movie_picker.replace_plot_with_refined")
@patch("app.llm.movie_picker.client")
def test_get_movie_details_by_name_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_MOVIE_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_MOVIE_TEXT

    result = movie_picker.get_movie_details_by_name_llm("Interstellar")
    assert "Christopher Nolan" in result


@patch("app.llm.movie_picker.replace_plot_with_refined")
@patch("app.llm.movie_picker.client")
def test_get_movies_by_genre_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_MOVIE_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_MOVIE_TEXT

    result = movie_picker.get_movies_by_genre_llm("գիտաֆանտաստիկա")
    assert "🎥 Վերնագիր" in result


@patch("app.llm.movie_picker.replace_plot_with_refined")
@patch("app.llm.movie_picker.client")
def test_get_top_10_movies_llm(mock_client, mock_replace_plot):
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=MOCK_MOVIE_TEXT))
    ]
    mock_replace_plot.return_value = MOCK_MOVIE_TEXT

    result = movie_picker.get_top_10_movies_llm()
    assert "IMDB" in result
