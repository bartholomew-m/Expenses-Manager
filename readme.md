# Manger wydatków - Expenses Manager

## Setup projektu

### Baza danych

W pliku **settings.py** => **DATABASES['default']** ustaw dane połączenia do istniejącej pustej bazy danych postgres.  

### Środowisko

Utwórz wirtualne środowisko python i zainstaluj zależności. 

```shell
python -m venv env
env\Scripts\activate & pip install -r requirements.txt
```

### Aktywacja środowiska

```shell
env\Scripts\activate
```

### Migracje

Wywołaj migracje na bazie danych  

```shell
(env) > python manage.py migrate
```

### Dodaj konto admina

Wywołaj komendę  

```shell
(env) > python manage.py createsuperuser
```

## Uruchom projekt deweloperski

Wywołaj komendę   

```shell
(env) > python manage.py runserver
```

### Panel admina znajduje się pod adresem: http://127.0.0.1:8000/admin/  
(Pamiętaj aby w adminie dodać przykładowe **Tag**'i oraz kategorie **ExpenseCategory**)

### Aplikacja znajduje się pod adresem: http://127.0.0.1:8000/expenses-manager/home/  
