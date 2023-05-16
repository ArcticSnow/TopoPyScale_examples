# TopoPyScale_examples
Set of examples on which to run [TopoPyScale](https://github.com/ArcticSnow/TopoPyScale)

The example `ex1_norway_finse` contains two Jupyter Notebooks available on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ArcticSnow/TopoPyScale_examples/main?labpath=https%3A%2F%2Fgithub.com%2FArcticSnow%2FTopoPyScale_examples%2Fblob%2Fmain%2Fex1_norway_finse%2Fex1_norway.ipynb)


**WARNINGS**
1. You need a Python VE setup with TopoPyScale installed
2. `cdsapi` credentials must be ready
3. These script will download the climate data from Copernicus ERA5 repository

Contributors:

- Simon Filhol
- Joel Fiddes


## Usage with TopoPyScale

1. Clone the repository
2. modify the `project_dir` in `config.yml` to fit your path
3. Run the pipeline within your relevant virtual environment
```
python pipeline.py
```

Now you may wait for the climate data to download. Downscaling will follow.


## Example 1: Finse in Norway

Folder `ex1_norway_finse`


## Example 2: Retezat Mountain Range in Romania

Folder `ex2_romania_retezat`

## Example 3: Davos in Switzerland

Folder `ex3_switzerland_davos`


## Adding an example site

Add a folder with a DEM and a complete `config.yml` file. To not overload the Github repo with data add in the `.gitignore` file lines to exclude the climate data and outputs such as:

```txt
ex2_romania_retezat/inputs/climate/* 
ex2_romania_retezat/outputs/*

ex1_norway_finse/inputs/climate/*
ex1_norway_finse/outputs/*
```

Be mindful of the size of the input DEM. Github limits to file above 50 Mb.

