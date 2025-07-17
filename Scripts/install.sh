pip install "$1"
pip freeze > requirements.txt
echo "$1 installed and requirements.txt updated."
