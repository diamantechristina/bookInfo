from flask import Flask, render_template, request, redirect, flash
from dbhelper import *

app = Flask(__name__)
app.secret_key = "!@#@!#!"


@app.route("/delete/<isbn>", methods=["POST"])
def deleteBook(isbn: str) -> None:
    postprocess(f"DELETE FROM books WHERE isbn='{isbn}'")
    flash("Book deleted")
    return redirect("/")


@app.route("/addBook", methods=["POST"])
def addBook():
    # try:
    isbn = request.form["isbn"].strip()
    title = request.form.get("title")
    author = request.form.get("author")
    copyright = request.form.get("copyright").strip()
    edition = request.form.get("edition").strip()
    price = request.form.get("price").strip()
    qty = request.form.get("qty").strip()

    if (
        not isbn.isdigit()
        or not copyright.isdigit()
        or not edition.isdigit()
        or not price.isdigit()
        or not qty.isdigit()
    ):
        flash("ISBN, copyright, edition, price and qty must be numbers")
        return redirect("/")

    existing_book = getprocess(f"SELECT * FROM books WHERE isbn='{isbn}'")

    if existing_book:
        flash("Book already exists!", "error")
    else:
        postprocess(
            f"INSERT INTO books (isbn, title, author, copyright, edition, price, qty) VALUES('{isbn}', '{title}', '{author}', {copyright}, {edition}, {price}, {qty})"
        )
        flash("Book added successfully!", "error")

    return redirect("/")


@app.route("/update/<isbn>", methods=["POST"])
def updateBook(isbn: str) -> None:
    try:
        isbn = request.form["isbn"].strip()
        title = request.form.get("title")
        author = request.form.get("author")
        copyright = request.form.get("copyright").strip()
        edition = request.form.get("edition").strip()
        price = request.form.get("price").strip()
        qty = request.form.get("qty").strip()

        if (
            not copyright.isdigit()
            or not edition.isdigit()
            or not price.isdigit()
            or not qty.isdigit()
        ):
            flash("Copyright, edition, price and qty must be numbers", "error")
            return redirect("/")

        existing_book = getprocess(f"SELECT * FROM books WHERE isbn='{isbn}'")

        if existing_book:
            postprocess(
                f"UPDATE books SET title='{title}', author='{author}', copyright={copyright}, "
                f"edition='{edition}', price={price}, qty={qty} WHERE isbn='{isbn}'"
            )
            flash("Book updated successfully!", "success")

        return redirect("/")
    except Exception as e:
        flash(f"Fill in all the fields", "error")
        return redirect("/")


@app.route("/")
def index() -> None:
    books = getprocess(
        """SELECT isbn, UPPER(title) AS title, UPPER(author) AS author, copyright, CASE 
            WHEN SUBSTR(edition, -1) = '1' AND edition != '11' THEN CONCAT(edition, 'st')
            WHEN SUBSTR(edition, -1) = '2' AND edition != '12' THEN CONCAT(edition, 'nd')
            WHEN SUBSTR(edition, -1) = '3' AND edition != '13' THEN CONCAT(edition, 'rd')
            ELSE CONCAT(edition, 'th') 
        END AS edition, price, qty, (price*qty) as total FROM books"""
    )
    return render_template("index.html", books=books)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
