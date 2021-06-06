# pg_utils.py
from datetime import datetime as dt
from config import Config
import os

# https://www.postgresql.org/docs/8.0/backup.html
# notes on backup and restore

def pg_dump_one():
    bu_time = dt.now()
    print(bu_time)
    os.system(f'pg_dump --dbname={Config.PG_DUMPS_URI} > "{Config.DB_BACKUPS}\loaderdump{bu_time.month}{bu_time.day}{bu_time.year}{bu_time.hour}.sql"')

def pg_restore_one(infile, testing=True):
    import subprocess

    DB_NAME = 'numeral5'  # your db name

    DB_USER = 'postgres' # you db user
    DB_HOST = "localhost"
    DB_PASSWORD = 'redmonroe'# your db password
    dump_success = 1
    print ('Backing up %s database ' % (DB_NAME))
    command_for_dumping = f'pg_dump --host={DB_HOST} ' \
                f'--dbname={DB_NAME} ' \
                f'--username={DB_USER} ' \
                f'--no-password ' \
                f'--file=backup.dmp '
    try:
        proc = subprocess.Popen(command, shell=True, env={
                    'PGPASSWORD': DB_PASSWORD
                    })
        proc.wait()

    except Exception as e:
            dump_success = 0
            print('Exception happened during dump %s' %(e))


    if dump_success:
        print('db dump successfull')
    print(' restoring to a new database database')

    """database to restore dump must be created with 
    the same user as of previous db (in my case user is 'postgres'). 
    i have #created a db called ReplicaDB. no need of tables inside. 
    restore process will #create tables with data.
    """

    backup_file = '/home/Downloads/BlogTemplate/BlogTemplate/backup.dmp' 
    """give absolute path of your dump file. This script will create the backup.dmp in the same directory from which u are running the script """



    if not dump_success:
        print('dump unsucessfull. retsore not possible')
    else:
        try:
            process = subprocess.Popen(
                            ['pg_restore',
                            '--no-owner',
                            '--dbname=postgresql://{}:{}@{}:{}/{}'.format('postgres',#db user
                                                                        'sarath1996', #db password
                                                                        'localhost',  #db host
                                                                        '5432', 'ReplicaDB'), #db port ,#db name
                            '-v',
                            backup_file],
                            stdout=subprocess.PIPE
                        )
            output = process.communicate()[0]

        except Exception as e:
            print('Exception during restore %e' %(e) )
        # restore from psql; see db & psql
