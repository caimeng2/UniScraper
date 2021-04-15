from Uniscraper.Uniscraper import uniscraper
import pytest

def test_uniscraper():
    url = "https://msu.edu/"
    webpage = uniscraper(url)
    text = webpage.text
    assert "Spartans" in text
