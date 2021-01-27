from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User


class AccountCreationForm(FlaskForm):
    acct_name = StringField('account name', validators=[DataRequired()])
    startbal = DecimalField('starting balance', validators=[InputRequired()])
    type = StringField('asset or liability?', validators=[DataRequired()])
    status = StringField('open or closed?', validators=[DataRequired()])
    submit = SubmitField('create account')


class EditAccountForm(AccountCreationForm):
    submit = SubmitField('submit account changes')


class CategoryCreationForm(FlaskForm):
    name = StringField('category name', validators=[DataRequired()])
    inorex = StringField('income or expense account?', validators=[DataRequired()])
    submit = SubmitField('create category')

class EditCategoryForm(CategoryCreationForm):
    submit = SubmitField('submit category changes')

class TransactionCreationForm(FlaskForm):
    date = DateField('date', validators=[DataRequired()])
    type = SelectField('type? transaction by default', choices=[('transactions', 'transactions'), ('split', 'split'), ('transfer', 'transfer'), ('notposted', 'notposted')])

    amount = DecimalField('amount (- for expense)', validators=[DataRequired()])
    payee_name = StringField('payee name')
    acct_id = SelectField('distribution account?', validators=[DataRequired()])
    acct_id2 = SelectField('transfer account?')
    cat_id = SelectField('category?')
    submit = SubmitField('add transaction to register')

class EditTransactionForm(TransactionCreationForm):
    submit = SubmitField('submit category changes')


class ReconciliationForm(FlaskForm):
    start_date = DateField('statement start date', validators=[DataRequired()])
    end_date = DateField('statement end date', validators=[DataRequired()])
    prior_end_balance = DecimalField('prior ending balance?', validators=[DataRequired()])
    statement_end_bal = DecimalField('statement ending balance?', validators=[DataRequired()])
    submit = SubmitField('start reconciling')

'''
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    '''