import pytest

def test_set_phrase():
    phrase = input("Set a phrase")
    assert len(phrase) < 15, f"Phrase > 15 sym"