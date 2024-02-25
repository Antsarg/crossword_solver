from project import search_words,  load_list

def test_load_list():
    global word_list
    word_list = load_list("assets\\spreadthewordlist_unscored_high.txt")
    assert len(word_list) > 0
    assert ("abdul" in word_list) == True
    assert ("anuglymind" in word_list) == False
