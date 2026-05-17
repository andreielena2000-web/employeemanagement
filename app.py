from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
db = SQLAlchemy(app)


class Employee(db.Model):
    cnp = db.Column(db.String(13), primary_key=True)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)
    varsta = db.Column(db.Integer, nullable=False)
    salariu = db.Column(db.Integer, nullable=False)
    departament = db.Column(db.String(50), nullable=False)
    senioritate = db.Column(db.String(20), nullable=False)



@app.route('/')
def home() -> str:

    '''
    Functia home():
        - afiseaza toti angajatii din baza de date
        - permite sortarea dupa salariu, departament sau senioritate
    '''
    

    sort = request.args.get("sort")

    if sort == "salary":
        employees = db.session.query(Employee).order_by(Employee.salariu).all()

    elif sort == "department":
        employees = db.session.query(Employee).order_by(Employee.departament).all()

    elif sort == "seniority":
        employees = db.session.query(Employee).order_by(Employee.senioritate).all()

    else:
        employees = db.session.query(Employee).all()

    return render_template('home_sql_alchemy.html', employees=employees)

@app.route('/add', methods=["GET", "POST"])
def add() -> str:

    '''
        Functia add(): adauga un nou angajat in baza de date
            
    '''

    if request.method == "POST":
        cnp = request.form.get('cnp')

        if not (cnp.isdigit() and len(cnp) == 13):
            print("CNP invalid.")
            return render_template("add_sql_alchemy.html", error="CNP invalid")
        existing_employee = db.session.query(Employee).get(cnp)

        if existing_employee:
            return render_template("add_sql_alchemy.html", error="Există deja un angajat cu acest CNP.")
        
        nume = request.form.get('nume')

        if not nume.isalpha():
            return render_template("add_sql_alchemy.html", error="Nu introduceți cifre sau mai mult de un nume în acest câmp.")
        
        prenume = request.form.get('prenume')

        if not prenume.replace(" ", "").replace("-", "").isalpha():
            return render_template("add_sql_alchemy.html", error="Prenumele trebuie să conțină numai litere.")

        varsta = int(request.form.get('varsta'))
        salariu = int(request.form.get('salariu'))
        departament = request.form.get('departament').lower()
        senioritate = request.form.get('senioritate')
        new_employee = Employee(cnp=cnp, nume=nume, prenume=prenume, varsta=varsta, salariu=salariu, departament=departament, senioritate=senioritate)
        db.session.add(new_employee)
        db.session.commit()
        logging.info("Angajat adăugat")
        return redirect(url_for('home'))

    return render_template('add_sql_alchemy.html')


@app.route('/update', methods=["GET", "POST"])
def update() -> str:

    '''
        Functia update():
        - modifica datele unui angajat existent
        - permite actualizarea unui camp selectate de utilizator
    '''

    if request.method == "POST":
        cnp = request.form.get("cnp")
        field = request.form.get("field")
        value = request.form.get("value")

        employee = db.session.query(Employee).get(cnp)

        if employee:
            if field == "nume":
                if not value.isalpha():
                    return render_template("update_sql_alchemy.html", error="Nu introduceți cifre sau mai mult de un nume în acest câmp.")
                employee.nume = value
                logging.info("nume actualizat")

            elif field == "prenume":
                if not value.replace(" ", "").replace("-", "").isalpha():
                    return render_template("update_sql_alchemy.html", error="Prenumele trebuie să conțină numai litere.")
                employee.prenume = value
                logging.info("prenume actualizat")

            elif field == "varsta":
                try:
                    value = int(value)
                    if value >= 18:
                        employee.varsta = value
                        logging.info("vârstă actualizată")
                    else:
                        logging.warning("Vârstă sub 18 ani.")
                except ValueError:
                    logging.warning("Input vârstă nu este un număr.")

            elif field == "salariu":
                try:
                    value = int(value)
                    if value >= 4050:
                        employee.salariu = value
                        logging.info("salariu actualizat")
                    else:
                        logging.warning("Salariu < 4050")
                except ValueError:
                    logging.warning("Input salariu nu este un număr.")
                    return render_template("update_sql_alchemy.html", error="Introduceți un număr valid")

            elif field == "departament":
                employee.departament = value.lower()
                logging.info("departament actualizat")

            elif field == "senioritate":
                value = value.lower()
                if value in ["junior", "mid", "senior"]:
                    employee.senioritate = value
                    logging.info("senioritate actualizată")
                else:
                    logging.warning("senioritate invalidă")
                    return render_template("update_sql_alchemy.html", error="senioritate invalidă")

            db.session.commit()
        else:
            logging.warning("CNP_update nu există în baza de date")
            return render_template("update_sql_alchemy.html", error="Angajatul nu există sau cnp invalid")

        return redirect(url_for("home"))

    return render_template("update_sql_alchemy.html")


@app.route('/delete', methods=["GET", "POST"])
def delete() -> str:

    '''
    Functia delete():
        - sterge un angajat din baza de date pe baza CNP-ului
    '''

    if request.method == "POST":
        cnp = request.form.get('cnp')

        employee = db.session.query(Employee).get(cnp)

        if employee:
            db.session.delete(employee)
            db.session.commit()
        else:
            logging.warning("CNP_delete nu există în baza de date")
            return render_template("update_sql_alchemy.html", error="Angajatul nu există sau cnp invalid"),

        return redirect(url_for('home'))

    return render_template('delete_sql_alchemy.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
