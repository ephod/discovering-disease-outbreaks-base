# Discovering Disease Outbreaks Starting Repository

Starter repository for Manning PBC: Discovering and Tracking Disease Outbreaks with Data Science and Python

## Setup

This project requires Python 3.7 installed with the [anaconda distribution](https://www.anaconda.com/distribution/).

To install the required libraries in a new virtual environment, run `conda env create -f environment.yml` from the project root 
directory. This will install the  libraries into a virtual env that can be activated with `conda activate discovering-disease-outbreaks`. 

The data is located at `data/headlines.txt`. Run `jupyter notebook` to start a Jupyter Notebook and get coding!

### Update Conda's environment

The following YAML file: `environment.yml` contains a predetermined env name.

```yaml
name: discovering-disease-outbreaks
# ...
```

```bash
conda env update -f environment.yml
```

If you want to update another environment based on the env file.

```bash
conda env update --name myenv -f environment.yml
```
