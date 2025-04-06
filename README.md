

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