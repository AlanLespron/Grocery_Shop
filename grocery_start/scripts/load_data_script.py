from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
from datetime import datetime
from sqlalchemy.orm import Session

session = Session()

app = Flask(__name__)
Base = declarative_base()


class GroceryItem(Base):
    __tablename__ = "grocery_items"
    id = Column(Integer, primary_key=True)
    SKU = Column(String)
    Name = Column(String)
    Description = Column(String)
    Price = Column(Float)
    Quantity = Column(Integer)
    Expiration_Date = Column(Date)
    converted_price = Column(Float)
    currency = Column(String)


DATABASE_URL = "postgresql://postgres:117007@localhost/postgres"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)


@app.route("/")
def index():
    with Session() as session:
        items = session.query(GroceryItem).all()
    return render_template("index.html", items=items)


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        sku = request.form["sku"]
        name = request.form["name"]
        new_item = GroceryItem(
            SKU=sku,
            Name=name,
        )
        with app.app_context():
            db_session = Session()
            db_session.add(new_item)
            db_session.commit()
        return redirect(url_for("index"))
    return render_template("add_item.html")


@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    with app.app_context():
        db_session = Session()
        item_to_delete = db_session.query(GroceryItem).get(item_id)
        if item_to_delete:
            db_session.delete(item_to_delete)
            db_session.commit()
    return redirect(url_for("index"))


if __name__ == "_main_":
    app.run(debug=True)


def load_data_to_database(filename):
    Session = sessionmaker(bind=engine)

    with Session() as session:
        with open(filename, "r") as f:
            csv_reader = csv.DictReader(f)
            try:
                for row in csv_reader:
                    grocery_item = GroceryItem(
                        SKU=row["SKU"],
                        Name=row["Name"],
                        Description=row["Description"],
                        Price=float(row["Price"]),
                        Quantity=int(row["Quantity"]),
                        Expiration_Date=datetime.strptime(
                            row["Expiration_Date"], "%Y-%m-%d"
                        ),
                        converted_price=None,
                        currency=None,
                    )
                    session.add(grocery_item)
                session.commit()
                print("Datos cargados exitosamente.")
            except Exception as e:
                print(f"Error: {e}")
                session.rollback()
                print("Se produjo un error y se revirtió la transacción.")


# Llamar a la función para cargar los datos desde el archivo CSV
load_data_to_database("sample_grocery.csv")
