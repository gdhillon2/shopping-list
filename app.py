from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class MyItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, default=1)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route("/", methods=["POST","GET"])
def index():
    # add item
    if request.method == "POST":
        current_item = request.form["content"]
        current_amount = request.form["amount"]
        print(str(current_item))
        new_item = MyItem(content=current_item, amount=current_amount)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # see all current items
    else:
        items = MyItem.query.order_by(MyItem.created).all()
        return render_template('index.html', items=items)

@app.route("/delete/<int:id>")
def delete(id:int):
    item_to_delete = MyItem.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR:{e}")
        return f"ERROR:{e}"


@app.route("/update/<int:id>", methods=["POST","GET"])
def edit(id:int):
    item = MyItem.query.get_or_404(id)
    if request.method == "POST":
        item.content = request.form["content"]
        item.amount = request.form["amount"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template("update.html", item=item)


if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
