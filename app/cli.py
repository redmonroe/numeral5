import os
import click
from datetime import datetime as dt

from config import Config

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
        from app.models import Accounts, Reconciliation
        from app import db
        for item in Accounts.query.all():
            item.startbal_str = str(item.startbal)

            print(item.startbal_str)
            db.session.commit()
            
        db.session.close()



        # for item in Reconciliation.query.all():
        #     print(item)
        #     item.statement_end_bal_str = str(item.statement_end_bal)
        #     db.session.commit()
        # db.session.close()

    @db_utilities.command()
    def dumpdb():
        def pg_dump_one():
            bu_time = dt.now()
            print(bu_time)
            os.system(f'pg_dump --dbname={Config.PG_DUMPS_URI} > "{Config.DB_BACKUPS}\lnew_loaderdump{bu_time.month}{bu_time.day}{bu_time.year}{bu_time.hour}.sql"')

        pg_dump_one()

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