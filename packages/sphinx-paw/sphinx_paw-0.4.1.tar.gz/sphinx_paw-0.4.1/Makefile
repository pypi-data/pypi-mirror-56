PROJECT_KEY		= sphinx_paw
SOURCEDIR     	= ./src/${PROJECT_KEY}
MSG_CATALOG		= ./src/${PROJECT_KEY}/locales/
MSG_TEMPLATE	= ${MSG_CATALOG}${PROJECT_KEY}.pot


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  locale-extract   		to extract localized strings from source code"
	@echo "  locale-update    		to update existed locales to have all localized strings"
	@echo "  locale-add <locale>    to add additional locale"

locale-extract:
	@echo
	@echo "Extracting localization strings from $(SOURCEDIR)"
	pybabel extract --output=${MSG_TEMPLATE} ${SOURCEDIR}/
	@echo
	@echo "Done"

locale-update:
	@echo
	@echo "Extracting localization strings from $(SOURCEDIR)"
	pybabel update --input-file=${MSG_TEMPLATE} --domain=${PROJECT_KEY} --output-dir=${MSG_CATALOG}
	@echo
	@echo "Done"

locale-add:
	@echo
	@echo "Extracting localization strings from $(SOURCEDIR)"
	pybabel init --input-file=${MSG_TEMPLATE} --domain=${PROJECT_KEY} --output-dir=${MSG_CATALOG} --locale=$(locale)
	@echo
	@echo "Done"

locale-compile:
	@echo
	@echo "Compile localization strings *.mo files"
	pybabel compile --directory=${MSG_CATALOG} --domain=${PROJECT_KEY}

publish_test:
	@echo
	@echo "Check twine installed"
	@pip install twine
	@echo "Create sdist"
	@python setup.py sdist
	@echo "Check package description"
	@twine check dist/*
	@echo "Uploading to test.pypi.org"
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish: publish_test
	@echo "Uploading to pypi.org"
	@twine upload dist/*

patch:
	@echo
	@echo "Bumping version m.v.Patch number"
	bumpversion --verbose patch

minor:
	@echo
	@echo "Bumping version m.Version.p number"
	bumpversion --verbose minor

major:
	@echo
	@echo "Bumping version Major.v.p number"
	bumpversion --verbose major
