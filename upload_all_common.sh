rm -r dist/
python setup.py sdist build
python setup.py bdist_wheel --universal
twine upload -u dist/*