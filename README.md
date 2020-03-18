# Описание
Сайт который читает список пар кодов из (csv) файла и по запросу первого кода выдает второй.

# Демо сайт

https://doublecode.herokuapp.com/


# Installation

```
git clone https://github.com/spbelect/doublecode.git
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Local deploy

Создать файл `env-local` со ссылкой на csv вида:

```
CSV_PAIRS_URL=https://gist.githubusercontent.com/Fak3/976b78e1a97bbd78a20dfc5bd295254e/raw/example.csv 
```

Запустить

```
python ./doublecode.py
```
