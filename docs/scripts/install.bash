cp .env.example .env &&
pipenv install &&
psql -u postgres -e "CREATE DATABASE example" &&
pipenv run init &&
pipenv run migrate &&
pipenv run upgrade &&
pipenv run start &&
python3 welcome.py