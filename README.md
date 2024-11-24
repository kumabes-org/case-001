# case-001

## frontend
### Criando o projeto
```
mkdir frontend
cd frontend
npm install @angular/cli
./node_modules/.bin/ng --version
./node_modules/.bin/ng new frontend
```

## backend
### Ambiente Virtual
```
cd backend
pip install virtualenv --user
OR
alias virtualenv="/home/rkumabe/.local/bin/virtualenv"
virtualenv venv --python=python3.10
source venv/bin/activate
pip install -r requirements.txt
```
### Iniciar a aplicação local
```
DB_USERNAME="case-001" DB_PASSWORD="supersecret" DB_HOSTNAME="case-001" DB_NAME="localhost" python src/app.py
```

## database