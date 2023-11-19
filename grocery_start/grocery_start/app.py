from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import requests

app = Flask(__name__)
app = Flask(__name__, static_folder="static")
Base = declarative_base()
app.config["SECRET_KEY"] = "98ea4f1872e6a8c3a4ceae1e31baefe7"


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

Session = sessionmaker(bind=engine)

EXCHANGE_RATE_API_BASE_URL = "https://open.er-api.com/v6/latest"


def convert_currency(amount, from_currency, to_currency):
    params = {"base": from_currency}
    response = requests.get(EXCHANGE_RATE_API_BASE_URL, params=params)

    if response.status_code == 200:
        exchange_rates = response.json()["rates"]
        if to_currency in exchange_rates:
            return amount * exchange_rates[to_currency]
        else:
            flash(f"Tipo de cambio '{to_currency}' no encontrado", "error")
            return None
    else:
        flash("ERROR AL OBENTER TIPO DE CAMBIO", "error")
        return None


@app.route("/")
def index():
    with Session() as session:
        items = session.query(GroceryItem).all()
        print(str((items[0])))
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
        with Session() as session:
            session.add(new_item)
            session.commit()
        return redirect(url_for("index"))
    return render_template("add_item.html")


@app.route("/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    with Session() as session:
        item_to_delete = session.query(GroceryItem).get(item_id)
        if item_to_delete:
            session.delete(item_to_delete)
            session.commit()
    return redirect(url_for("index"))


@app.route("/item", methods=["POST"])
def add_item_to_db():
    if request.method == "POST":
        sku = request.form["SKU"]
        name = request.form["Name"]
        description = request.form["Description"]
        price = float(request.form["Price"])
        quantity = int(request.form["Quantity"])
        expiration_date = datetime.strptime(
            request.form["Expiration_Date"], "%Y-%m-%d"
        ).date()
        new_item = GroceryItem(
            SKU=sku,
            Name=name,
            Description=description,
            Price=price,
            Quantity=quantity,
            Expiration_Date=expiration_date,
            converted_price=None,
            currency=None,
        )

        # Agregar datos a la base de datos
        with Session() as session:
            session.add(new_item)
            session.commit()
        return redirect(url_for("index"))


@app.route("/convert_all_items", methods=["POST"])
def convert_all_items():
    currency = request.form.get("currency")

    if not currency:
        flash("El tipo de cambio es necesario", "error")
        return redirect(url_for("index"))

    with Session() as session:
        items = session.query(GroceryItem).all()

        for item in items:
            converted_price = convert_currency(item.Price, "USD", currency)
            if converted_price is not None:
                flash(
                    f"Precio de {item.Name} convertido a {currency}: {converted_price}",
                    "success",
                )
                item.converted_price = converted_price
                item.currency = currency

        session.commit()  # Hace el commit a  cambios a la base de datos

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
