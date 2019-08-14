::@echo off

:: It might be helpful to remove the inital build.
del _build /Q

:: Go out to the primary directory for api compliation
cd ..
sphinx-apidoc -e -f -o Documentation/_source/python_docstrings ./IfA_Smeargle

:: Go back into the doc directory and complile the html
cd Documentation
call make clean
call make html
call make latex

:: Go to the LaTeX and compile
call _build\latex\make.bat