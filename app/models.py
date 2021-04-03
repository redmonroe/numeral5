from datetime import date, datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


# followers = db.Table(
#     'followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
# )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
 

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def avatar(self, size):
    #     digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    #     return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    #         digest, size)

    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)

    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    acct_name = db.Column(db.String)
    startbal = db.Column(db.Numeric)
    type = db.Column(db.String)
    status = db.Column(db.String) #either open or closed
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def accounts_to_dict(list_of_accounts):
        account_list = []
        for it in list_of_accounts:
            s = {}
            curbal, startbal = Transactions.get_current_balance(it.id)
            s['acct_name'] = it.acct_name
            s['id'] = it.id
            s['current_balance'] = curbal
            s['start_balance'] = it.startbal
            account_list.append(s)
        return account_list

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String)
    inorex = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        spacer = '**'
        return f'{self.name:-^40} {spacer:>2} {self.inorex:^20}'


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Numeric)
    payee_name = db.Column(db.String) # would become own column
    type = db.Column(db.String)
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    cat_id2 = db.Column(db.Integer, db.ForeignKey('categories.id'))
    cat_id3 = db.Column(db.Integer, db.ForeignKey('categories.id'))
    acct_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    amount2 = db.Column(db.Numeric)
    acct_id2 = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reconciled = db.Column(db.Boolean)
    agg_amount = db.Column(db.Numeric)

    def __repr__ (self):
        return f"transaction: {self.id} {self.reconciled}"

    def get_current_balance(id): # must include transfers (as opposed to transaction journals which don't)
        from decimal import Decimal
        results = []
        r = Transactions.query.filter(Transactions.acct_id2 ==
                                        id, Transactions.type != 'notposted').all()
        r2 = Transactions.query.filter(Transactions.acct_id ==
                                        id, Transactions.type != 'notposted').all()
        for item in r:
            results.append(item)
        for item in r2:
            results.append(item)

        bal_list = []
        # gets starting balance from account id
        starting_balance = Accounts.query.filter(Accounts.id == id).first()
        # print('ok', starting_balance.startbal)

        for item in results:
            if item.type == 'transfer' and item.acct_id2 == int(id):
                bal_list.append(item.amount * -1)
            elif (item.type == 'transfer') and (item.acct_id == int(id)):
                print('transfer amount:', item.amount)
                bal_list.append(item.amount)
            elif item.type == 'transactions':
                bal_list.append(item.amount)


        try:
            print('bal_list sum', sum(bal_list))
            curbal = Decimal(starting_balance.startbal) + sum(bal_list)
            print('curbal', curbal)
        except TypeError as e: 
            curbal = Decimal(starting_balance.startbal) + 0

        return curbal, starting_balance

class Reconciliation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    prior_end_balance = db.Column(db.Numeric)
    statement_end_bal = db.Column(db.Numeric)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    acct_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    finalized = db.Column(db.Boolean)
    txnjsn = db.Column(db.String)
    checkboxjsn = db.Column(db.String)

class Reports(object):
    @staticmethod
    def report_query(username, report_period=None, report_template=None, total=None):
        from sqlalchemy import extract, and_
      

        # this is ALWAYS part of queyr
        if report_period == 'year':
            period = date.today().year
        elif report_period == 'last month':
            period = date.today().month - 1
            report_period = 'month'
            print(period)
            # period = now.month-1 if now.month > 1 else 12
        elif report_period == 'month':
            period = date.today().month

        user = User.query.filter_by(username=username).first()

        queries = []

        if report_template == 'default':
            queries.append(Transactions.user_id == user.id)
            queries.append(extract(report_period, Transactions.date) == period)
        elif report_template == 'posted':
            queries.append(Transactions.user_id == user.id)
            queries.append(Transactions.type != 'notposted')
            queries.append(Transactions.type != 'transfers')
            queries.append(extract(report_period, Transactions.date) == period)

        print (report_template, queries)
        if total: 
            cat_list = Categories.query.filter(Categories.user_id == user.id).all()
            catid_dict = {i.id:[] for i in cat_list}

        # main iteration
        output_list_of_tuples = []
        for transaction in Transactions.query.filter(and_(*queries)):
            
            name = transaction
            other = 'add more info here'
            row = (name, other)
            output_list_of_tuples.append(row)


            if total:
                for k, v in catid_dict.items():                
                    if k == transaction.cat_id:
                        catid_dict[k].append(float(transaction.amount))

        if total: 
            cat_tuple = ()
            renamed_list = []
            output_list_of_tuples = []
            for key, value in catid_dict.items():
                category = Categories.query.get(key)
                cat_tuple = (category.name, value)
                renamed_list.append(cat_tuple)

            for item in renamed_list:
                name = item[0]
                total = sum(item[1])
                cat_tuple = (name, total)
                output_list_of_tuples.append(cat_tuple)

        # print(output_list_of_tuples)

        return output_list_of_tuples

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     language = db.Column(db.String(5))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)