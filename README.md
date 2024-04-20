# SkyFly Backend

## Run project locally

1. Install python packages

```bash
sudo apt install python3-pip python3
pip install --user pipenv
```

2. Set python path

   Save the python path variable in the ~/.bashrc file for convenience.
   Replace [username] with your linux user. To see it just use this command:

```bash
echo $USER
```

Then set the variable:

- Open .bashrc file for editing

```bash
nano ~/.bashc
```

- Copy and paste this line at the top of the file

```bash
export PYTHONPATH="${PYTHONPATH}:/home/[username]/"
```

- Press ctrl+X, then Y, then enter. And save file

```bash
source ~/.bashrc
```

Or just do it from your command line every time you open terminal

```bash
export PYTHONPATH="${PYTHONPATH}:/home/[username]/"
```

3. Clone the repository

```bash
git clone git@github.com:margoch24/skyfly-backend.git && cd skyfly-backend
```

4. Install dependencies

```bash
pipenv install
```

5. Create .env file (from .env.example)

6. Run project:

```bash
pipenv run start
```

## Setup mysql database

### Development / Production

0. Enter mysql:

```bash
mysql -u root -p
```

1. Create mysql database:

```bash
CREATE DATABASE skyfly;
```

2. Create new mysql user with a password requirement

```bash
CREATE USER 'skyfly'@'localhost';
ALTER USER 'skyfly'@'localhost' IDENTIFIED WITH mysql_native_password BY '[your password here]';
```

3. grant privileges to this user for database 'skyfly'

```bash
GRANT ALL PRIVILEGES ON skyfly. * TO 'skylfy'@'localhost';
FLUSH PRIVILEGES;
```

4. exit mysql

```bash
exit;
```

### Test

0. Enter mysql:

```bash
mysql -u root -p
```

1. Create mysql database:

```bash
CREATE DATABASE test_skyfly;
```

2. Create new mysql user without a password requirement

```bash
CREATE USER 'test-skyfly'@'localhost';
ALTER USER 'test-skyfly'@'localhost' IDENTIFIED WITH mysql_native_password BY '';
```

3. grant privileges to this user for database 'test_skyfly'

```bash
   GRANT ALL PRIVILEGES ON test_skyfly. * TO 'test-skylfy'@'localhost';
   FLUSH PRIVILEGES;
```

4. exit mysql

```bash
exit;
```

## Testing

### Run all tests

```bash
pipenv run test
```

### Run single test

1. add `_only` to the end of the method name of the test you want to test.
   *def test_successful(self) ---> def test_successful_only(self)*

2. run single test:

```bash
pipenv run test-only
```

### Create tests

It is important to start all the names of the files you want to test with `test_`.

## Format Python VSCode

1. Install vscode extensions

- Black Formatter
- isort

2. Go to Settings (ctrl+Comma) > settings.json (top right corner "Open Settings (JSON)")

Add:

```json
"[python]": {
   "editor.formatOnSave": true,
   "editor.defaultFormatter": "ms-python.black-formatter",
   "editor.codeActionsOnSave": {
      "source.organizeImports": true
   }
},
"isort.args": ["--profile", "black"]
```

3. Upgrade vscode if changes have no effect:

```bash
sudo apt update
sudo apt install code
```
