import random

from flask_login import login_required, current_user

from book.book_url import book


@book.route("/show_some_book/<num>", methods=["GET"])
@login_required
def show_some_book(num):
    try:
        num = int(num)
        from model.models import Book
        from es.my_es import es
        tot_book = es.count()['count']
        choice = random.sample(range(1, tot_book + 1), num)
        show_books = []
        for i in range(len(choice)):
            found_book = get_book_by_id(choice[i])
            show_books.append(found_book['book'])
    except Exception as e:
        return {"error": e.__str__(), "books": None}
    return {"error": None, "books": show_books}


@book.route("/get_book_by_id/<book_id>", methods=["GET"])
@login_required
def get_book_by_id(book_id):
    try:
        from es.my_es import es
        result = es.get_doc(book_id)['_source']
    except Exception as e:
        return {"error": e.__str__(), "book": None}
    return {"error": None, "book": result}


@book.route("/search_book/<key_word>", methods=["GET"])
@login_required
def search_book(key_word):
    try:
        result = []
        from es.my_es import es
        es_result = es.search(key_word)
        hits = es_result['hits']
        for hit in hits['hits']:
            result.append(hit["_source"])
        return {"error": None, "result": result}
    except Exception as e:
        return {"error": e.__str__(), "result": None}


@book.route("/query_borrow_by_user", methods=["GET"])
@login_required
def query_borrow_by_user():
    try:
        from model.models import Borrow
        borrows = Borrow.query.filter_by(user_id=current_user.get_id()).all()
        borrows_result = []
        for borrow in borrows:
            borrows_result.append([borrow.id, borrow.book_id, int(borrow.create_time.timestamp())])
        return {"error": None, "borrows": borrows_result}
    except Exception as e:
        return {"error": e.__str__(), "borrows": None}
