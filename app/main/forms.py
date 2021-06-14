from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, SelectField, DateField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Length, InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class AccountCreationForm(FlaskForm):
    acct_name = StringField('account name', validators=[DataRequired()])
    startbal_str = StringField('starting balance', validators=[InputRequired()])
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
    date = DateField('date', format='%Y-%m-%d')
    # date = DateField('date', validators=[DataRequired()])
    type = SelectField('type? transaction by default', choices=[('transactions', 'transactions'), ('split', 'split'), ('transfer', 'transfer'), ('notposted', 'notposted')])
    amount = DecimalField('amount (- for expense)', validators=[DataRequired()])
    payee_name = SelectField('payee name')
    acct_id = SelectField('distribution account?', validators=[DataRequired()])
    acct_id2 = SelectField('transfer account?')
    cat_id = SelectField('category?')
    submit = SubmitField('add transaction to register')

class EditTransactionForm(TransactionCreationForm):
    submit = SubmitField('submit transaction changes')

class ReconciliationForm(FlaskForm):
    start_date = DateField('statement start date', validators=[DataRequired()])
    end_date = DateField('statement end date', validators=[DataRequired()])
    prior_end_balance = DecimalField('prior ending balance?', validators=[DataRequired()])
    statement_end_bal = DecimalField('statement ending balance?', validators=[DataRequired()])
    submit = SubmitField('start reconciling')

class EditReconciliationForm(ReconciliationForm):
    submit = SubmitField('submit adjustment')

class ReportSelectForm(FlaskForm):
    report_period = SelectField('report period', choices=[('year', 'year'), ('month', 'month'), ('last month', 'last month'), ('custom', 'custom')])
    report_template = SelectField('report template', choices=[('default', 'get all in period'), ('posted', 'posted only')])
    total_by_cat = SelectField('total by category', choices=[(True, 'yes'), (False, 'no')])
    # if report_period == 'custom':
    start_date = DateField('start')
    end_date = DateField('end')
    submit = SubmitField('generate report')

class ReportSelectForm(FlaskForm):
    report_period = SelectField('report period', choices=[('year', 'year'), ('month', 'month'), ('last month', 'last month'), ('custom', 'custom')])
    report_template = SelectField('report template', choices=[('default', 'get all in period'), ('posted', 'posted only')])
    total_by_cat = SelectField('total by category', choices=[(True, 'yes'), (False, 'no')])
    # if report_period == 'custom':
    start_date = DateField('start')
    end_date = DateField('end')
    submit = SubmitField('generate report')

class VendorCreationForm(FlaskForm):
    vendor_name = StringField('vendor name')
    submit = SubmitField('create new vendor')

class EditVendorForm(VendorCreationForm):
    pass
