# TopoPyScale_examples
Set of examples on which to run [TopoPyScale](https://github.com/ArcticSnow/TopoPyScale)

Contributors:

- Simon Filhol, October 2021



## Usage with TopoPyScale

1. Clone the repository
2. modify the `project_dir` in `config-ini` to fit your path
3. Run TopoPyScale



## Example 1: Finse in Norway

Folder `ex1_norway_finse`



## Example 2: Retezat Mountain Range in Romania

Folder `ex2_romania_retezat`



## Adding an example site

Add a folder with a DEM and a complete `config.ini` file. To not overload the Github repo with data add in the `.gitignore` file lines to exclude the climate data and outputs such as:

```txt
ex2_romania_retezat/inputs/forcings/* 
ex2_romania_retezat/outputs/*

ex1_norway_finse/inputs/forcings/*
ex1_norway_finse/outputs/*
```

Be mindful of the size of the input DEM. Github limits to file above 50 Mb.

