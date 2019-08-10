@echo off

:: Go out to the mrimary directory for api compliation
cd ..
sphinx-apidoc -e -f -o Documentation/_source/python_docstrings ./

:: Go back into the doc directory and complile the html
cd Documentation
make clean && make html && make latex

:: Go to the LaTeX and compile
make latexpdf