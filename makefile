MODULENAME = Uniscraper 

init:
	conda env create --prefix ./envs --file environment.yml

docs:
	pdoc3--force --html --output-dir ./docs $(MODULENAME)

lint:
	pylint $(MODULENAME) 

doclint:
	pydocstyle $(MODULENAME)

test:
	python downloadwords.py
	pytest -v $(MODULENAME) 

.PHONY: init docs lint test 
