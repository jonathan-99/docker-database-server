# docker-database-server
A dockerised, sqlite3 database with a front-end RESTapi written in python, deployed by ansible.

## Coverage.
> pip install coverage
> python -m coverage run -m unittest
> python -m coverage report
> python -m coverage html

## Pylint
>pip install pylint
File -> Settings -> Tools -> External Tools -> "add"
 - In "Name" put pylint
 - In "Program" put location of and pylint.exe
 - In "Paramaters" put $FilePath$
Tools -> External tools -> pylint

## Development Update
### update 22/08/23. 
> Coverage - "Total	714	314	0	56%"
> Pylint - "Your code has been rated at 5.35/10" - for testing.
> Pylint - "Your code has been rated at 5.11/10" for src.