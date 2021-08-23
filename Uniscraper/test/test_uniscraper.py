from Uniscraper.Uniscraper import uniscraper
import pytest

def test_uniscraper():
    url = "https://www.msu.edu/"
    webpage = uniscraper(url)
    webtext = webpage.text
    assert "Spartans" in webtext
