NAMESPACE=dmmmd
SHELL := /bin/bash

tmpinstall:
	# This fails because mktmpenv is not on path. Just for reference.
	# mktmpenv -n
	pip install chamelboots --extra-index-url=https://test.pypi.org/simple/

build:
	python setup.py sdist bdist_wheel

check:
	twine check ./dist/*

testupload:
	twine upload --repository-url https://test.pypi.org/legacy/ ./dist/* --verbose

upload:
	twine upload dist/*

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
	rm -fr docs/_build/

distclean: clean
	rm -fr *.egg *.egg-info/ dist/ build/

coverage:
	
	/home/dmmmd/.virtualenvs/seven-notebooks/bin/watchmedo shell-command \
		--patterns="*.py" \
		--command='clear && pytest --cov --cov-report=term-missing -vv tests && coverage html' \
		-w -W \
		--recursive ./tests/

pytest:
	/home/dmmmd/.virtualenvs/seven-notebooks/bin/watchmedo shell-command \
		--patterns="*.py" \
		--command='clear && pytest -sx $${watch_src_path}' \
		-w -W \
		--recursive ./tests/

tox:
	/home/dmmmd/.virtualenvs/seven-notebooks/bin/watchmedo shell-command \
		--patterns="*.py" \
		--command='clear && tox -p auto' \
		-w -W \
		--recursive ./tests/

browser-sync:
	browser-sync \
		start \
		--server ./htmlcov \
		--port 3000 \
		--files "**/*" \
		--host $$(hostname)  \
		--no-open \
		--no-ui \
		--https \
		--key ~/.jupyter/mykey.key \
		--cert ~/.jupyter/mycert.pem 

ctags:
	ctags -R \
		--exclude=.git \
		--exclude=node_modules \
		--exclude=tests \
		--exclude=.tox \
		--exclude=dist .

