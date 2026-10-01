import runpy

import pytest

TEST_CASES = [
    pytest.param(
        "abbreviation.py",
        "Белорусский государственный университет информатики и радиоэлектроники",
        "Аббревиатура: БГУИР",
        id="abbreviation-bsuir",
    ),
    pytest.param(
        "abbreviation.py",
        "Министерство антимонопольного регулирования и торговли",
        "Аббревиатура: МАРТ",
        id="abbreviation-mart",
    ),
    pytest.param(
        "abbreviation.py",
        "Национальный центр электронных услуг",
        "Аббревиатура: НЦЭУ",
        id="abbreviation-nces",
    ),
    pytest.param("calculator.py", "1+2+3+4", "Сумма: 10", id="calculator-sum-single-digits"),
    pytest.param("calculator.py", "10+20+30+40", "Сумма: 100", id="calculator-sum-double-digits"),
    pytest.param("calculator.py", "2*2*2*2*2", "Произведение: 32", id="calculator-multiplication"),
    pytest.param("chess_case.py", "One TWO Three FOUR", "ONE two THREE four", id="chess-case-four-words"),
    pytest.param("chess_case.py", "ПрИвЕт МИР из PYTHON", "ПРИВЕТ мир ИЗ python", id="chess-case-mixed-case"),
    pytest.param("chess_case.py", "  one   two  three  ", "ONE two THREE", id="chess-case-extra-spaces"),
    pytest.param(
        "hashtags.py",
        "Учимся с #Python, пишем #код и снова #Python!",
        "#Python #код",
        id="hashtags-unique-in-order",
    ),
    pytest.param(
        "hashtags.py",
        "Теги: #one, #two и #three_3.",
        "#one #two #three_3",
        id="hashtags-separated-by-punctuation",
    ),
    pytest.param(
        "palindrome.py",
        "А роза упала на лапу Азора!",
        "Палиндром",
        id="palindrome-ignore-case-and-punctuation",
    ),
    pytest.param("palindrome.py", "Python — это здорово", "Не палиндром", id="palindrome-negative"),
    pytest.param(
        "palindromes_count.py",
        "Дед пошёл искать шалаш и топот",
        "Палиндромов: 4",
        id="palindromes-count-example",
    ),
    pytest.param("palindromes_count.py", "А бб Ввв гд", "Палиндромов: 3", id="palindromes-count-mixed-case"),
    pytest.param("palindromes_count.py", "python code", "Палиндромов: 0", id="palindromes-count-zero"),
    pytest.param(
        "phone_formatter.py",
        "(29) 123-45-67",
        "+375291234567",
        id="phone-formatter-valid",
    ),
    pytest.param(
        "phone_formatter.py",
        "29-123-456-789",
        "Некорректный номер",
        id="phone-formatter-too-many-digits",
    ),
    pytest.param(
        "phone_formatter.py",
        "29A1234567",
        "Некорректный номер",
        id="phone-formatter-invalid-character",
    ),
    pytest.param(
        "reversed_sentence.py",
        "Python делает задачи понятнее",
        "понятнее задачи делает Python",
        id="reversed-sentence-example",
    ),
    pytest.param(
        "reversed_sentence.py",
        "один два три",
        "три два один",
        id="reversed-sentence-extra-spaces",
    ),
    pytest.param("reversed_sentence.py", "Python", "Python", id="reversed-sentence-single-word"),
    pytest.param("reversed_words.py", "Python is fun", "nohtyP si nuf", id="reversed-words-example"),
    pytest.param("reversed_words.py", "Привет мир", "тевирП рим", id="reversed-words-cyrillic"),
    pytest.param("reversed_words.py", "one two", "eno owt", id="reversed-words-extra-spaces"),
    pytest.param("series_encoding.py", "aaabbcaaaa", "a3b2c1a4", id="series-encoding-example"),
    pytest.param("series_encoding.py", "abcd", "a1b1c1d1", id="series-encoding-single-character-runs"),
    pytest.param("series_encoding.py", "zzzz", "z4", id="series-encoding-single-run"),
    pytest.param(
        "string_stats.py",
        "Дом 42!",
        "3 буквы, 2 цифры, 1 пробел и 1 другой символ",
        id="string-stats-example",
    ),
    pytest.param(
        "string_stats.py",
        "Python",
        "6 буквы, 0 цифры, 0 пробел и 0 другой символ",
        id="string-stats-only-letters",
    ),
    pytest.param(
        "string_stats.py",
        "1\nA?",
        "1 буквы, 1 цифры, 0 пробел и 2 другой символ",
        id="string-stats-other-characters",
    ),
    pytest.param(
        "string_sum.py",
        "Заказ: 12 ручек, 3 блокнота и 105 скрепок",
        "Сумма чисел: 120",
        id="string-sum-example",
    ),
    pytest.param("string_sum.py", "Нет чисел", "Сумма чисел: 0", id="string-sum-zero"),
]


def pytest_generate_tests(metafunc):
    if {"script", "user_input", "expected"}.issubset(metafunc.fixturenames):
        metafunc.parametrize(("script", "user_input", "expected"), TEST_CASES)


@pytest.fixture
def hw_path(base_hw_path):
    return base_hw_path / "homeworks_01"


@pytest.mark.timeout(30)
def test_homework_script(monkeypatch, capsys, hw_path, script, user_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: user_input)

    runpy.run_path(hw_path / script)

    output = capsys.readouterr().out
    assert expected in output, f"Скрипт {script} для ввода {user_input!r} должен вывести {expected!r}"
