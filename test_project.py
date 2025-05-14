from project import choose, set_entry, get_subjects, UserShenanigans
import pytest


def test_set_entry():
    assert set_entry('foo') == 'foo'
    assert set_entry('1,2,3') == '1~~~2~~~3'
    assert set_entry('a ,    b,  c     ') == "a~~~b~~~c"
    assert set_entry("aAa, b Bb, C C C ") == "aaa~~~b bb~~~c c c"
    with pytest.raises(AttributeError):
        set_entry(3) == '3'

def test_get_subjects():
    assert get_subjects(['foo_bar.csv']) == ["Foo Bar"]
    assert get_subjects(['foo_bar_2.txt','foo_bar.csv','EXAMPLE.csv']) == ["Foo Bar","Example"]

def test_choose(monkeypatch):
    inputs = [
        'Y',
        ' N ',
        iter(['y','Y']),
        iter(['n','n','n','N']),
        iter(['a','a','a','a']),
        iter(['b','b','b','b','b','b','b'])
    ]
    monkeypatch.setattr('builtins.input', lambda _: inputs[0])
    assert choose("input:", "Y", "N") == 'Y'
    monkeypatch.setattr('builtins.input', lambda _: inputs[1])
    assert choose("input:", "Y", "N") == 'N'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs[2]))
    assert choose("input:", "Y", "N") == 'Y'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs[3]))
    assert choose("input:", "Y", "N") == 'N'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs[4]))
    with pytest.raises(UserShenanigans):
        assert choose("input:", "Y", "N")
    monkeypatch.setattr('builtins.input', lambda _: next(inputs[5]))
    with pytest.raises(UserShenanigans):
        assert choose("input:", "Y", "N")