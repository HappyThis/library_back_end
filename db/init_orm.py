import time

import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

import model.models


def import_book_from_file(data_file="db/book_data"):
    books = []
    with open(data_file, encoding="utf-8") as file:
        for line in file:
            book_data_p1 = line[:-1].split(",")[:12]
            # for i in range(len(book_data_p1)):
            #     print(i, book_data_p1[i])
            book_data_p2 = line[:-1].split(",'")
            book_data_p2 = book_data_p2[len(book_data_p2) - 6:]
            # print(book_data_p2[len(book_data_p2) - 6:])
            book_name = book_data_p1[1].strip()
            book_name = book_name[1:-1].strip()
            author = book_data_p1[2].strip()
            author = author[1:-1].strip()
            publisher = book_data_p1[3].strip()
            publisher = publisher[1:-1].strip()
            translator = book_data_p1[4].strip()
            if translator == "NULL\'":
                translator = None
            else:
                translator = translator[1:-1].strip()
            isbn = book_data_p1[7].strip()
            isbn = isbn[1:-1].strip()
            if isbn[0] != "9":
                continue
            abstract = book_data_p2[0].strip()
            abstract = abstract[:-1].strip()
            author_introduction = book_data_p2[1].strip()
            author_introduction = author_introduction[:-1].strip()
            catalog = book_data_p2[3].strip()
            catalog = catalog[:-1].strip()
            picture = book_data_p2[4].strip()
            picture = picture[:-1].strip()
            value = [book_name, author, publisher, translator, isbn, abstract, author_introduction, catalog, picture]
            books.append(value)
        return books


def orm_db():
    from db.orm_db import sqlite_db
    sqlite_db.drop_all()
    sqlite_db.create_all()
    # 插入初始数据
    # 插入用户
    for i in range(3):
        user = model.models.User(id="202012378" + str(i), username="萝卜" + str(i),
                                 password=generate_password_hash("123456"))
        sqlite_db.session.add(user)
    # 插入层次
    for i in range(3):
        layer = model.models.Layer(layer_name=str(i) + "_layer")
        sqlite_db.session.add(layer)
    sqlite_db.session.commit()
    # 对于每个层次插入区
    layers = model.models.Layer.query.all()
    for layer in layers:
        for j in range(3):
            part = model.models.Part(layer_id=layer.id, part_name=chr(ord("A") + j) + "_part")
            sqlite_db.session.add(part)
    sqlite_db.session.commit()
    # 对于每个区插入桌子
    parts = model.models.Part.query.all()
    for part in parts:
        for j in range(1, 11):
            desk = model.models.Desk(part_id=part.id, desk_name=str(j) + "_desk")
            sqlite_db.session.add(desk)
    sqlite_db.session.commit()
    # 对于桌子，插入椅子
    desks = model.models.Desk.query.all()
    for desk in desks:
        for j in range(1, 6):
            stool = model.models.Stool(desk_id=desk.id, stool_name=str(j) + "_stool")
            sqlite_db.session.add(stool)
    sqlite_db.session.commit()
    books = import_book_from_file()
    # 插入书
    for book in books:
        insert_book = model.models.Book(book_name=book[0], author=book[1], publisher=book[2], translator=book[3],
                                        isbn=book[4], abstract=book[5], author_introduction=book[6], catalog=book[7],
                                        picture=book[8])
        sqlite_db.session.add(insert_book)

    sqlite_db.session.commit()
    # 书籍数据导入es
    books = model.models.Book.query.all()
    from es.my_es import es

    es.delete_index()
    for book in books:
        book_data = {
            "id": book.id,
            "book_name": book.book_name,
            "author": book.author,
            "author_introduction": book.author_introduction,
            "abstract": book.author,
            "catalog": book.catalog,
            "isbn": book.isbn,
            "translator": book.translator,
            "publisher": book.publisher,
            "picture": book.picture
        }
        es.insert_one(doc=book_data)


@click.command('orm-db')
@with_appcontext
def orm_db_command():
    """Clear the existing data and create new tables."""
    orm_db()
    click.echo('Initialized the database.')
