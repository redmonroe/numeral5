import os
import click
from app.models import Accounts
from app import db



def register(app):
    @app.cli.group()
    def db_utilities():
        """just get a command without running a route"""
        pass

    @db_utilities.command()
    def print_test():
        print('hello world')

    @db_utilities.command()
    def duplicatecol():
        """duplicate a column"""
        """I don't know how to abstract this properly"""
        for item in Accounts.query.all():
            print(item)
            item.startbal_str = str(item.startbal)
            db.session.commit()
        db.session.close()

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')