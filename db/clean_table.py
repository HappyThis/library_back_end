import click
from flask import current_app
from flask.cli import with_appcontext

from db.connector import close_db, get_db


def clean_db():
    db = get_db()
    with current_app.open_resource(current_app.config["CLEAN"]) as f:
        db.executescript(f.read().decode('utf8'))
    close_db()


@click.command('clean-db')
@with_appcontext
def clean_db_command():
    clean_db()
    click.echo('Clean the database.')
