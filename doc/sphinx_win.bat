::@echo off

:: It might be helpful to remove the inital build.
rmdir build /S /Q

:: Go out to the primary directory for api compliation
cd ..
sphinx-apidoc -e -f -o doc/source/docstrings ./ifa_smeargle

:: Go back into the doc directory and complile the html
cd doc
call make clean
call make html
call make latex

:: Go to the LaTeX and compile
call build\latex\make.bat