import runpy

import pytest


def run_script(hw_path, script, **inputs):
    inputs["testing"] = bool(inputs)
    return runpy.run_path(hw_path / script, init_globals=inputs)


@pytest.fixture
def hw_path(base_hw_path):
    return base_hw_path / "homeworks_02"


@pytest.mark.parametrize(
    ("sales", "common", "leaders"),
    [
        (None, {"1984", "Мастер и Маргарита"}, ["Мастер и Маргарита"]),
        (
            [
                ("Дюна", "Буква", 2),
                ("1984", "Буква", 3),
                ("Гарри Поттер", "Буква", 10),
                ("Дюна", "Книжный мир", 3),
                ("1984", "Книжный мир", 2),
            ],
            {"Дюна", "1984"},
            ["Гарри Поттер"],
        ),
    ],
    ids=["example", "other-data"],
)
def test_bestsellers(hw_path, sales, common, leaders):
    result = run_script(hw_path, "bestsellers.py", **({} if sales is None else {"sales": sales}))
    assert result["common_books"] == common
    assert result["bestsellers"] == leaders


@pytest.mark.parametrize(
    ("attempts", "expected"),
    [
        (None, ["bob", "charlie"]),
        (
            [
                ("dmitry", False),
                ("dmitry", False),
                ("dmitry", True),
                ("dmitry", False),
                ("dmitry", False),
                ("dmitry", False),
                ("dmitry", True),
            ],
            ["dmitry"],
        ),
    ],
    ids=["example", "reset-and-ignore"],
)
def test_block_entries(hw_path, attempts, expected):
    result = run_script(hw_path, "block_entries.py", **({} if attempts is None else {"attempts": attempts}))
    assert result["blocked_users"] == expected


@pytest.mark.parametrize(
    ("transactions", "total", "money"),
    [
        (None, 250, {100: 1, 50: 3, 10: 0, 5: 0, 1: 0}),
        ([(5, 10), (5, 5), (4, 5), (5, 10)], 10, {100: 0, 50: 0, 10: 1, 5: 0, 1: 0}),
    ],
    ids=["example", "not-enough-change"],
)
def test_cashbox(hw_path, transactions, total, money):
    result = run_script(hw_path, "cashbox.py", **({} if transactions is None else {"transactions": transactions}))
    assert result["successful_sum"] == total
    assert result["cashbox"] == money


@pytest.mark.parametrize(
    ("checks", "hours", "working"),
    [
        (None, {"Анна": 8, "Борис": 9}, {"Виктор"}),
        (
            [("Мария", 8), ("Алексей", 9), ("Мария", 10), ("Мария", 11), ("Мария", 15)],
            {"Мария": 6},
            {"Алексей"},
        ),
    ],
    ids=["example", "several-periods"],
)
def test_checkpoint(hw_path, checks, hours, working):
    result = run_script(hw_path, "checkpoint.py", **({} if checks is None else {"checks": checks}))
    assert result["employees_working_hours"] == hours
    assert result["employees_still_working"] == working


@pytest.mark.parametrize(
    ("config", "expected"),
    [(None, True), ("server { routes: [(]) }", False), ("function(call[argument]", False)],
    ids=["example", "wrong-nesting", "unclosed-bracket"],
)
def test_config_validator(hw_path, config, expected):
    result = run_script(hw_path, "config_validator.py", **({} if config is None else {"config": config}))
    assert result["is_valid"] is expected


@pytest.mark.parametrize(
    ("path", "params", "expected"),
    [
        (None, None, "/tmp"),
        ("/", ["..", "a/b", "..", ".", "c"], "/a/c"),
        ("/home/user", ["docs", "/var/log", "../tmp"], "/var/tmp"),
    ],
    ids=["example", "root-and-relative", "absolute-path"],
)
def test_current_path(hw_path, path, params, expected):
    inputs = {} if path is None else {"current_path": path, "cd_params": params}
    result = run_script(hw_path, "current_path.py", **inputs)
    assert result["final_path"] == expected


@pytest.mark.parametrize(
    ("actions", "expected"),
    [(None, 3), (["start", "stop", "start", "start", "stop", "stop"], 2)],
    ids=["example", "reuse-room"],
)
def test_meeting_rooms(hw_path, actions, expected):
    result = run_script(hw_path, "meeting_rooms.py", **({} if actions is None else {"actions": actions}))
    assert result["required_rooms"] == expected


@pytest.mark.parametrize(
    ("inputs", "expected"),
    [
        ({}, {"Анна": [], "Борис": ["Git", "Django"], "Виктор": ["Основы Python"]}),
        (
            {
                "students_courses": {"Мария": {"Основы Python"}, "Алексей": set()},
                "course_requirements": {
                    "Основы Python": {"алгоритмы"},
                    "Git": {"командная строка", "файлы"},
                    "Django": {"Python", "ООП", "HTTP", "базы данных"},
                },
                "course_achievements": {
                    "Основы Python": {"Python", "ООП", "HTTP", "базы данных"},
                },
            },
            {"Мария": ["Git", "Django"], "Алексей": ["Основы Python", "Git"]},
        ),
    ],
    ids=["example", "threshold"],
)
def test_next_courses(hw_path, inputs, expected):
    result = run_script(hw_path, "next_courses.py", **inputs)
    assert result["recommendations"] == expected


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        (None, ["0", "2-4", "7", "10-11"]),
        ([1, 2, 3, 6, 9, 10, 11, 12], ["1-3", "6", "9-12"]),
        ([], []),
    ],
    ids=["example", "several-ranges", "empty"],
)
def test_range_folder(hw_path, numbers, expected):
    inputs = {} if numbers is None else {"numbers": numbers}
    result = run_script(hw_path, "range_folder.py", **inputs)
    assert result["folded"] == expected


@pytest.mark.parametrize(
    ("sales", "expected"),
    [
        (None, {"Анна": {"шоколад"}, "Борис": {"печенье", "рис"}, "Виктор": set(), "Галина": {"чай"}}),
        (
            [
                ("Анна", "кофе"),
                ("Анна", "чай"),
                ("Анна", "молоко"),
                ("Анна", "печенье"),
                ("Борис", "кофе"),
                ("Борис", "чай"),
                ("Борис", "молоко"),
                ("Борис", "шоколад"),
                ("Виктор", "кофе"),
                ("Виктор", "чай"),
                ("Виктор", "молоко"),
                ("Виктор", "хлеб"),
            ],
            {
                "Анна": {"шоколад", "хлеб"},
                "Борис": {"печенье", "хлеб"},
                "Виктор": {"печенье", "шоколад"},
            },
        ),
    ],
    ids=["example", "several-similar-users"],
)
def test_recommender(hw_path, sales, expected):
    result = run_script(hw_path, "recommender.py", **({} if sales is None else {"sales": sales}))
    assert result["recommendations"] == expected


@pytest.mark.parametrize(
    ("info", "courses", "above_average"),
    [
        (None, {"Git", "Python"}, ["Анна", "Виктор"]),
        (
            [
                ("Мария", "Математика", 10),
                ("Мария", "История", 10),
                ("Алексей", "Математика", 6),
                ("Алексей", "История", 8),
            ],
            {"Математика", "История"},
            ["Мария"],
        ),
    ],
    ids=["example", "other-grades"],
)
def test_students(hw_path, info, courses, above_average):
    result = run_script(hw_path, "students.py", **({} if info is None else {"students_info": info}))
    assert result["common_courses"] == courses
    assert result["students_above_average"] == above_average


@pytest.mark.parametrize(
    ("games", "expected"),
    [
        (None, "Сокол"),
        (
            [("Сокол", "Вымпел", 2, 0), ("Метеор", "Сокол", 1, 0), ("Метеор", "Вымпел", 3, 3)],
            "Метеор",
        ),
    ],
    ids=["example", "wins-and-draw"],
)
def test_tournament(hw_path, games, expected):
    result = run_script(hw_path, "tournament.py", **({} if games is None else {"games": games}))
    assert result["champion"] == expected
