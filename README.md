# Employee Management Application

## Descriere proiect
Această aplicație este realizată în Python folosind Flask și SQLAlchemy și permite gestionarea unei baze de date cu angajați.

Aplicația implementează operațiile CRUD:
- Create (adăugare angajat)
- Read (afișare angajați)
- Update (actualizare date angajat)
- Delete (ștergere angajat)

De asemenea, aplicația permite sortarea angajaților după:
- salariu
- departament
- senioritate

## Tehnologii utilizate
- Python
- Flask
- SQLAlchemy
- HTML
- CSS
- Jinja2

## Funcționalități
- Adăugare angajat
- Actualizare date angajat
- Ștergere angajat
- Afișare listă angajați
- Sortare date
- Validare date introduse
- Logging pentru anumite acțiuni și erori

## Structura proiectului
- `app.py` -> logica principală a aplicației Flask
- `templates/` -> fișiere HTML pentru interfața grafică
- `employees.db` -> baza de date SQLite

## Instalare și rulare

### Instalare dependințe
```bash
pip install flask
pip install flask_sqlalchemy

### Rulare aplicație

```bash
python app.py
```

Aplicația va rula la:

```text
http://127.0.0.1:5000
```
