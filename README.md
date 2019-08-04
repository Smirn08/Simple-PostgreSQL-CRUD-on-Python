# Simple PostgreSQL CRUD on Python


Написано на [python 3.6.8](https://www.python.org/) c использованием [psycopg2](http://initd.org/psycopg/docs/) для [PostgreSQL](https://www.postgresql.org/)

---
## Из чего состоит
### Описание сущностей:
Сущность Процесс. 
- Поля: id процесса, название, описание, флаг активности 

Сущность Параметр процесса: 
- Поля: название параметра, значение (текст) 

Сущность Условие запуска процесса.
- Поля: тип условия, значение (текст) 

Сущность Исполнитель процесса.
- Поля: id, название, описание (текст) 

Сущность Квота процесса.
- Поля: тип квоты, значение квоты (число) 


### Отношения: 

* Процесс - Параметр процесса - один ко многим
* Процесс - Условие запуска процесса - один ко многим
* Процесс - Исполнитель процесса - Многие к одному
* Процесс - Квота процесса - Один ко многим
---

## Как использовать?
### Для начала
Прописать connect и изменить имя своей базы данных можно в начале каждого файла `db_creator.py` и `load_data.py`
```
db_creator.py
```
Имеет команды:
- `create_db` : создание базы данных
- `create_tab` : создание пустых таблиц
- `clean` : очистка всех таблиц
- `del` : удаление всех таблиц
- `test_data` : загрузка тестовых данных в таблицы

### Создание собственного процесса:
```
load_data.py
```
Имеет команды:
- создание самого процесса
```
process --id <process_id> --name <process_name> --descr <process_description> --flag <flag [0,1]>
```
- создание параметров процесса
```
parameter --id <process_id> --p_name <process_param_name> --p_val <process_param_value>
```
- создание условий запуска процесса
```
condition --id <process_id> --c_type <condition_type> --c_val <condition_value>
```
- создание пользователя процесса
```
user --id <process_id> --u_id <user_id> --u_name <user_name> --u_descr <user_description>
```
- создание квоты процесса
```
qouta --id <process_id> --q_type <process_qouta_type> --q_val <process_qouta_val>
```

### Пример создания / изменения параметров:
```
db_creator.py create_db
db_creator.py create_tab
load_data.py process --id 1 --name First_pr --descr sample --flag 0 
load_data.py parameter --id 1 --p_name 1st_par --p_val 111
load_data.py condition --id 1 --c_type time --c_val 10:30
load_data.py user --id 1 --u_id 1337 --u_name kekandr --u_descr loled
load_data.py qouta --id 1 --q_type aaa --q_val 40
```
---
