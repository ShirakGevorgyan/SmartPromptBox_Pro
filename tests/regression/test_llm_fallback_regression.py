from unittest.mock import patch
from app.llm.series_picker import get_series_details_by_name_llm


def test_llm_fallback_on_gpt_failure():
    """
    Ռեգրեսիոն թեստ․ GPT-4o տապալվելու դեպքում վերադարձվում է fallback հաղորդագրություն։
    """
    fallback_text = (
        "Հնարավոր չէ ստանալ տվյալներ «Breaking Bad» սերիալի մասին այս պահին։"
    )

    with patch(
        "app.llm.series_picker.client.chat.completions.create",
        side_effect=Exception("GPT 500 error"),
    ):
        result = get_series_details_by_name_llm("Breaking Bad")

        assert result == fallback_text
