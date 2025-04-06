

## Developer documentation

### How to install the project

```bash
python -m venv ../venvs/digup312
source ../venvs/digup312
python -m ensurepip --upgrade
python -m pip install setuptools --upgrade
python -m pip install -r requirements.txt

# To be able to run `digup` cli in the project
python -m pip install -e .
```


### How to public a new version

Increment the version in [pyproject.toml](pyproject.toml).

Delete the previous artefacts
```bash
rm dist/*
```

Build the project
```
python -m build
```

Upload the artefacts
```
python -m twine upload dist/*
```