README.md:
	jupytext --from Rmd --to ipynb --output - README.Rmd \
		| jupyter nbconvert --stdin --to markdown --execute --output README.md
	
