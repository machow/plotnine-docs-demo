setup:
	rm -rf plotnine-examples
	git clone https://github.com/has2k1/plotnine-examples.git

docs-build:
	DOC_GENERATION=1 python -m quartodoc build
	quarto render
