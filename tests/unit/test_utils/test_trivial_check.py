import pytest
from app.utils.trivial_check import is_trivial_question

@pytest.mark.parametrize("input_text", [
    "Բարև", 
    "բարև ջան", 
    "Հահա, լավն էր", 
    "ես ուրախ եմ", 
    "Ո՞նց ես", 
    "ԼԱՎ ԵՄ", 
    "Այո", 
    "ոչ"
])
def test_trivial_returns_true(input_text):
    assert is_trivial_question(input_text) is True


@pytest.mark.parametrize("input_text", [
    "Ինչ է GPT-ն", 
    "Նկարագրի ինձ Արարատ լեռը", 
    "Ո՞վ է գրել Համլետը", 
    "Ինչպես աշխատում է մեքենայական ուսուցումը",
    "Ի՞նչ կլինի վաղը եղանակը",
    "ես սիրում եմ ծրագրավորում",
    "արագության բանաձևը ինչ է"
])
def test_trivial_returns_false(input_text):
    assert is_trivial_question(input_text) is False
