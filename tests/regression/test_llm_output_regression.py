# tests/regression/test_llm_output_regression.py

import pytest
from unittest.mock import patch
from app.llm import series_picker


@pytest.mark.parametrize(
    "series_name, mocked_response, expected_keywords",
    [
        (
            "Breaking Bad",
            "Walter White is a chemistry teacher who becomes Heisenberg.",
            ["Walter White", "Heisenberg"],
        ),
        (
            "Dark",
            "Jonas gets caught in a time loop in a German town.",
            ["Jonas", "time", "loop", "Germany"],
        ),
        (
            "Stranger Things",
            "Eleven and her friends in Hawkins fight against supernatural threats like the Demogorgon.",
            ["Eleven", "Hawkins", "Demogorgon"],
        ),
        (
            "Sherlock",
            "Holmes and Watson solve crimes in modern-day London.",
            ["Holmes", "Watson", "London"],
        ),
        (
            "Game of Thrones",
            "The battle for the Iron Throne involves the Starks, Lannisters and other noble houses of Westeros.",
            ["Stark", "Lannister", "Westeros"],
        ),
        (
            "Chernobyl",
            "A nuclear disaster in Chernobyl leads to radiation, cover-ups, and massive destruction.",
            ["nuclear", "Chernobyl", "radiation"],
        ),
    ],
)
def test_llm_output_regression(series_name, mocked_response, expected_keywords):
    """
    Ռեգրեսիոն թեստ․ ստուգում ենք մոկված GPT պատասխանները համապատասխան keyword-ներով։
    """
    with patch(
        "app.llm.series_picker.get_series_details_by_name_llm",
        return_value=mocked_response,
    ):
        result = series_picker.get_series_details_by_name_llm(series_name)
        result_lower = result.lower()

        found_keywords = [kw for kw in expected_keywords if kw.lower() in result_lower]

        assert len(found_keywords) >= 2, (
            f"Expected at least 2 keywords in response for '{series_name}', "
            f"but got only: {found_keywords}"
        )
