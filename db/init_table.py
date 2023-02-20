import click
from flask import current_app
from flask.cli import with_appcontext

from db.connector import get_db, close_db


def init_db():
    db = get_db()
    with current_app.open_resource(current_app.config["SCHEMA"]) as f:
        db.executescript(f.read().decode('utf8'))
    close_db()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
