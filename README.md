# SkyFly Backend

sudo apt install python3-pip

pip install -r requirements.txt

save in ~/.bashrc
export PYTHONPATH="${PYTHONPATH}:/home/[username]/"

python3 api/main.py

## Format Python VSCode

Black Formatter
isort

Settings > settings.json

Add:
"[python]": {
"editor.formatOnSave": true,
"editor.defaultFormatter": "ms-python.black-formatter",
"editor.codeActionsOnSave": {
"source.organizeImports": true
}
},
"isort.args": ["--profile", "black"]

Upgrade vscode:
sudo apt update
sudo apt install code

## Later on Remove this Section

observer
