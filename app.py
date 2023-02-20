from flask import Flask


def create_app(cfg_file):
    app = Flask(__name__)
    app.config.from_pyfile(cfg_file)
    from db.connector import close_db
    app.teardown_appcontext(close_db)
    from db.init_table import init_db_command
    app.cli.add_command(init_db_command)
    from db.clean_table import clean_db_command
    app.cli.add_command(clean_db_command)
    return app


library_app = create_app("configure.py")

if __name__ == '__main__':
    library_app.run()
