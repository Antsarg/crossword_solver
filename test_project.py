import pytest
from project import search_words,  load_list


@pytest.fixture
def unscored_list():
    return load_list("assets\\spreadthewordlist_unscored_high.txt")

def test_load_list():
    word_list = load_list("assets\\spreadthewordlist_unscored_high.txt")
    assert len(word_list) > 0
    assert "abdul" in word_list
    assert "anuglymind" not in word_list

def test_search_words(unscored_list: list):
    assert search_words("air???ne", unscored_list) == ["airborne", "airplane"]
    assert search_words("mar?io", unscored_list) == []
    assert "monitor" in search_words("m???t??", unscored_list)
    assert "terrain" in search_words("t??ra??", unscored_list)
    assert "score" not in search_words("st?r?", unscored_list)
    assert "darkroom" not in search_words("dar??", unscored_list)