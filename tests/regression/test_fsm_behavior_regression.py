# tests/regression/test_fsm_behavior_regression.py

from app.telegram_bot.handlers.series_menu_handler import SeriesStates
from app.telegram_bot.handlers.random_songs_handler import SongStates


def test_series_states_exist_and_correct():
    expected_states = {
        "waiting_for_description",
        "waiting_for_series_name",
        "waiting_for_genre",
    }

    actual_states = {
        attr
        for attr in dir(SeriesStates)
        if not attr.startswith("_") and isinstance(getattr(SeriesStates, attr), object)
    }

    assert expected_states.issubset(actual_states)


def test_song_states_exist_and_correct():
    expected_states = {
        "waiting_for_genre",
        "waiting_for_description",
        "waiting_for_artist",
    }

    actual_states = {
        attr
        for attr in dir(SongStates)
        if not attr.startswith("_") and isinstance(getattr(SongStates, attr), object)
    }

    assert expected_states.issubset(actual_states)
