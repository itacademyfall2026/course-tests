import filecmp
import tempfile

import pytest

from homeworks.homeworks_03.editor import main as editor_main
from homeworks.homeworks_03.shopping_list import main as shopping_list_main




@pytest.fixture
def hw_path(base_hw_path):
    return base_hw_path / "homeworks_03"


@pytest.mark.parametrize("number", ("1", "2"))
def test_editor(hw_path, number):
    data_dir = hw_path / "data" / "editor"
    sample_csv = data_dir / "samples" / f"{number}.csv"
    expected_txt = data_dir / "expected" / f"{number}.txt"

    with tempfile.NamedTemporaryFile(delete_on_close=False) as result_file:
        result_file.close()
        editor_main(sample_csv, result_file.name)

        assert filecmp.cmp(expected_txt, result_file, shallow=False)


@pytest.mark.parametrize("number", ("1", "2"))
def test_shopping_list(hw_path, number):
    data_dir = hw_path / "data" / "shopping_list"
    recipes_csv = data_dir / "samples" / number / "recipes.csv"
    ingredients_csv = data_dir / "samples" / number / "ingredients.csv"
    menu_csv = data_dir / "samples" / number / "menu.csv"
    expected_txt = data_dir / "expected" / f"{number}.csv"

    with tempfile.NamedTemporaryFile(delete_on_close=False) as result_file:
        result_file.close()
        shopping_list_main(
            recipes_csv,
            ingredients_csv,
            menu_csv,
            result_file.name
        )

        assert filecmp.cmp(expected_txt, result_file, shallow=False)
