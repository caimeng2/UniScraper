# <center> UniScraper </center>

## Description

Uniscraper is a universal scraper that collects text from multiple types of webpages. Currently it supports html (including dynamic webpages that use javascript), online pdfs, word documents, presentation slides, and spreadsheets.

## Installation instructions

Clone the git repo:

    git clone https://github.com/caimeng2/UniScraper.git
    
Set up a conda environment by running the following command:

    conda env create --prefix ./envs --file environment.yml

    conda activate ./envs

## Dependency

`bs4` `webdriver_manager` `pandas` `selenium` `nltk` `requests` `python-docx` `python-pptx`  `pdfminer`

## Example usage

Please run `example.ipynb` to see example usage.
