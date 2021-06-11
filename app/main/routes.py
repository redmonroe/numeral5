import json
from datetime import datetime, timedelta
from decimal import Decimal

from app import db
from app.main import bp
from app.main.forms import (AccountCreationForm, CategoryCreationForm,
                            EditAccountForm, EditCategoryForm,
                            EditReconciliationForm, EditTransactionForm,
                            EmptyForm, ReconciliationForm, ReportSelectForm,
                            TransactionCreationForm, VendorCreationForm)
from app.models import (Accounts, Categories, Reconciliation, Reports,
                        Transactions, User, Vendors, route_utilities)
from flask import (current_app, flash, g, jsonify, redirect, render_template,
                   request, url_for)
from flask_babel import _, get_locale
from flask_login import current_user, login_required
from sqlalchemy import and_, or_


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/<username>/', methods=['GET', 'POST'])

def index(username=None):
    print(username)
    string = 'hello world this is numeral4 & 5.  I am born December 10, 2020.'
    return render_template('main/index.html', title='sign in', string=string)

'''
account functions
'''

@bp.route('/accounts/<username>/')
@login_required
def accounts(username):
    user = User.query.filter_by(username=username).first()

    r = Accounts.query.filter(Accounts.user_id == user.id).all()

    account_list = Accounts.accounts_to_dict(r)

    return render_template('main/view_account.html', items=account_list)

@bp.route('/create_account/<username>/', methods=['GET', 'POST'])
@login_required
def create_account(username):

    user = User.query.filter_by(username=username).first()

    r = Accounts.query.filter(Accounts.user_id == user.id).all()

    form = AccountCreationForm()
    if form.validate_on_submit():
        new_account = Accounts()
        new_account.acct_name = form.acct_name.data
        new_account.startbal = form.startbal.data
        new_account.type = form.type.data
        new_account.status = form.status.data
        new_account.user_id = user.id
        db.session.add(new_account)
        db.session.commit()
        flash('congratulations, you created a new account')
        return redirect(url_for('main.create_account', username=username))
    return render_template('main/create_account.html', form=form)


@bp.route('/delete_account/<username>', methods=['GET', 'POST'])
@login_required
def delete_account(username):

    user = User.query.filter_by(username=username).first()

    r = Accounts.query.filter(Accounts.user_id == user.id).all()

    # return redirect(url_for('delete_account', username=username)) #post/redirect/get pattern
    return render_template('main/delete_account.html', items=r)

@bp.route('/deleted/<username>/<id>', methods=['GET', 'POST'])
@login_required
def deleted(username, id):

    user = User.query.filter_by(username=username).first()

    r = Accounts.query.get(id)

    db.session.delete(r)
    db.session.commit()

    flash('congratulations, you deleted an account')
    # post/redirect/get pattern
    return redirect(url_for('main.accounts', username=username))

@bp.route('/edit_account/<username>/<id>', methods=['GET', 'POST'])
@login_required
def edit_account(username, id):

    user = User.query.filter_by(username=username).first()

    r = Accounts.query.filter(Accounts.user_id == user.id).all()

    account = Accounts.query.get(id)

    form = EditAccountForm(obj=account)
    if form.validate_on_submit():
        account.acct_name = form.acct_name.data
        account.startbal = form.startbal.data
        account.type = form.type.data
        account.status = form.status.data
        account.user_id = user.id
        db.session.commit()
        db.session.close()
        flash('congratulations, you created a new account')
        # post/redirect/get pattern
        return redirect(url_for('main.accounts', username=username))
    return render_template('main/edit_account.html', form=form)

'''
categories functions
'''

@bp.route('/categories/<username>')
@login_required
def categories(username):

    user = User.query.filter_by(username=username).first()

    r = Categories.query.filter(Categories.user_id == user.id).all()

    return render_template('main/view_categories.html', items=r)


@bp.route('/create_category/<username>/', methods=['GET', 'POST'])
@login_required
def create_category(username):

    user = User.query.filter_by(username=username).first()

    r = Categories.query.filter(Categories.user_id == user.id).all()

    form = CategoryCreationForm()
    if form.validate_on_submit():
        new_cat = Categories()
        new_cat.id = None
        new_cat.name = form.name.data
        new_cat.inorex = form.inorex.data
        new_cat.user_id = user.id
        db.session.add(new_cat)
        db.session.commit()
        db.session.close()
        flash('congratulations, you created a new category')
        # post/redirect/get pattern
        return redirect(url_for('main.categories', username=username))

    return render_template('main/create_categories.html', form=form)


@bp.route('/edit_category/<username>/<id>', methods=['GET', 'POST'])
@login_required
def edit_category(username, id):
    
    user = User.query.filter_by(username=username).first()

    r = Categories.query.filter(Categories.user_id == user.id).all()

    categories = Categories.query.get(id)

    form = EditCategoryForm(obj=categories)
    if form.validate_on_submit():

        categories.name = form.name.data
        categories.inorex = form.inorex.data
        categories.user_id = user.id
        db.session.commit()
        db.session.close()
        flash('congratulations, you edited this category')
        # post/redirect/get pattern
        return redirect(url_for('categories', username=username))

    return render_template('main/edit_categories.html', form=form)


@bp.route('/delete_category/<username>', methods=['GET', 'POST'])
@login_required
def delete_category(username):

    user = User.query.filter_by(username=username).first()

    r = Categories.query.filter(Categories.user_id == user.id).all()

    return render_template('main/delete_categories.html', items=r)


@bp.route('/deletedcat/<username>/<id>', methods=['GET', 'POST'])
@login_required
def deletedcat(username, id):

    user = User.query.filter_by(username=username).first()

    r = Categories.query.get(id)

    db.session.delete(r)
    db.session.commit()
    db.session.close()

    flash('congratulations, you deleted an account')
    # post/redirect/get pattern
    return redirect(url_for('main.categories', username=username))

'''
transactions
'''
@bp.route('/transactions/<username>', methods=['GET', 'POST'])
@login_required
def transactions(username):
    '''get this working first > break out by account'''

    user = User.query.filter_by(username=username).first()

    r = Transactions.query.filter(Transactions.user_id == user.id).all()

    return render_template('main/transactions.html', username=username, items=r)

@bp.route('/create_transaction/<username>/<lastpage>/', methods=['GET', 'POST'])
@login_required
def create_transaction(username, id=None, lastpage=None):
    #username, #account_id
    
    print('ct:', lastpage)
    user = User.query.filter_by(username=username).first()

    # ''' code to create dynamics account list for form'''
    account_choice = Accounts.query.filter(
        Accounts.user_id == user.id).all()

    account_list = [(item.id, item.acct_name) for item in account_choice]

    # ''' code to create dynamic category list for form'''
    category_choice = Categories.query.filter(
        Categories.user_id == user.id).all()

    cat_list = [(item.id, item.name) for item in category_choice]

    # ''' code to create dynamic vendor list
    vendor_choice = Vendors.query.filter(Vendors.user_id == user.id).all()

    vendor_list = [(item.vendor_name) for item in vendor_choice]

    form = TransactionCreationForm()
    form.acct_id.choices = account_list
    form.acct_id2.choices = account_list
    form.cat_id.choices = cat_list
    form.payee_name.choices = vendor_list
    if form.validate_on_submit():
        print('create txn after submit')
        new_transaction = Transactions()
        new_transaction.user_id = user.id
        new_transaction.date = form.date.data
        new_transaction.type = form.type.data
        new_transaction.amount = form.amount.data
        new_transaction.payee_name = form.payee_name.data
        new_transaction.acct_id = form.acct_id.data
        new_transaction.reconciled = False
        if new_transaction.type == 'transfer':
            new_transaction.acct_id2 = form.acct_id2.data
        else:
            new_transaction.acct_id2 = None
        new_transaction.cat_id = form.cat_id.data     
        db.session.add(new_transaction)
        db.session.commit()
        db.session.close()
        flash('congratulations, you created a new transaction')
    
        return redirect(url_for('main.register', username=username, id=form.acct_id.data, lastpage=lastpage))
        # acct_id=new_transaction.acct_id, 

    return render_template('main/create_transactions.html', form=form, lastpage=lastpage)

@bp.route('/create_and_new/<username>/<lastpage>/', methods=['GET', 'POST'])
@login_required
def create_and_new(username, id=None, lastpage=None):
    #username, #account_id

    print('c&n:', lastpage)
    user = User.query.filter_by(username=username).first()

    # ''' code to create dynamics account list for form'''
    account_choice = Accounts.query.filter(
        Accounts.user_id == user.id).all()

    account_list = [(item.id, item.acct_name) for item in account_choice]

    # ''' code to create dynamic category list for form'''
    category_choice = Categories.query.filter(
        Categories.user_id == user.id).all()

    cat_list = [(item.id, item.name) for item in category_choice]

    # r = Categories.query.filter(Categories.user_id == user.id).all()

    form = TransactionCreationForm()
    form.acct_id.choices = account_list
    form.acct_id2.choices = account_list
    form.cat_id.choices = cat_list
    if form.validate_on_submit():
        print('create new after submit')
        new_transaction = Transactions()
        new_transaction.user_id = user.id
        new_transaction.date = form.date.data
        new_transaction.type = form.type.data
        new_transaction.amount = form.amount.data
        new_transaction.payee_name = form.payee_name.data
        new_transaction.acct_id = form.acct_id.data
        new_transaction.reconciled = False
        if new_transaction.type == 'transfer':
            new_transaction.acct_id2 = form.acct_id2.data
        else:
            new_transaction.acct_id2 = None
        new_transaction.cat_id = form.cat_id.data
        db.session.add(new_transaction)
        db.session.commit()
        db.session.close()
        flash('congratulations, you created a new transaction')
        # post/redirect/get pattern
        return redirect(url_for('main.create_transaction', username=username, id=form.acct_id.data, lastpage=lastpage))

    return render_template('main/create_transactions.html', form=form)


@bp.route('/delete_transaction/<username>', methods=['GET', 'POST'])
@login_required
def delete_transaction(username):

    user = User.query.filter_by(username=username).first()

    r = Transactions.query.filter(Transactions.user_id == user.id).all()

    return render_template('main/delete_transaction.html', items=r)

@bp.route('/deletedtxn/<username>/<id>', methods=['GET', 'POST'])
@bp.route('/deletedtxn/<username>/<id>/<acct>', methods=['GET', 'POST'])
@login_required
def deletedtxn(username, id, acct):

    user = User.query.filter_by(username=username).first()

    r = Transactions.query.get(id)

    db.session.delete(r)
    db.session.commit()
    db.session.close()
    return redirect(route_utilities.my_redirect_url())


@bp.route('/edit_transaction/<username>/<id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(username, id):


    print('ct:', lastpage)
    user = User.query.filter_by(username=username).first()

    r = Transactions.query.filter(Transactions.user_id == user.id).all()

    transaction = Transactions.query.get(id)

    account_choice = Accounts.query.filter(Accounts.user_id == user.id).all()

    account_list = [(item.id, item.acct_name) for item in account_choice]

    # ''' code to create dynamic category list for form'''
    category_choice = Categories.query.filter(
        Categories.user_id == user.id).all()

    cat_list = [(item.id, item.name) for item in category_choice]

    form = EditTransactionForm(obj=transaction)
    form.acct_id.choices = account_list
    form.acct_id2.choices = account_list
    form.cat_id.choices = cat_list

    if form.validate_on_submit():

        transaction.user_id = user.id
        transaction.date = form.date.data
        transaction.type = form.type.data
        transaction.amount = form.amount.data
        transaction.payee_name = form.payee_name.data
        transaction.acct_id = form.acct_id.data
        if transaction.type == 'transfer':
            transaction.acct_id2 = form.acct_id2.data
        else:
            transaction.acct_id2 = None
        transaction.cat_id = form.cat_id.data

        db.session.commit()
        db.session.close()
        flash('congratulations, you edited this transaction')

        # return redirect(route_utilities.my_redirect_url(referrer))
        return redirect(url_for('main.register', username=username, id=form.acct_id.data))

    return render_template('main/edit_transaction.html', form=form)


@bp.route('/edit_transaction_reconciliation/<username>/<id>', methods=['GET', 'POST'])
@login_required
def edit_transaction_reconciliation(username, id):

    
    user = User.query.filter_by(username=username).first()

    r = Transactions.query.filter(Transactions.user_id == user.id).all()

    transaction = Transactions.query.get(id)

    account_choice = Accounts.query.filter(Accounts.user_id == user.id).all()

    account_list = [(item.id, item.acct_name) for item in account_choice]

    # ''' code to create dynamic category list for form'''
    category_choice = Categories.query.filter(
        Categories.user_id == user.id).all()

    cat_list = [(item.id, item.name) for item in category_choice]

    form = EditTransactionForm(obj=transaction)
    form.acct_id.choices = account_list
    form.acct_id2.choices = account_list
    form.cat_id.choices = cat_list   

    if form.validate_on_submit():
    # continue_reconcile(username, rec_id)

        reconciliation = Reconciliation.query.filter(Reconciliation.finalized == None).first()
        print(reconciliation, reconciliation.id)
        rec_id = reconciliation.id
    
        transaction.user_id = user.id
        transaction.date = form.date.data
        transaction.type = form.type.data
        transaction.amount = form.amount.data
        transaction.payee_name = form.payee_name.data
        transaction.acct_id = form.acct_id.data
        if transaction.type == 'transfer':
            transaction.acct_id2 = form.acct_id2.data
        else:
            transaction.acct_id2 = None
        transaction.cat_id = form.cat_id.data 

        db.session.commit()
        db.session.close()
        flash('congratulations, you edited this transaction')

        return redirect(url_for('main.continue_reconcile', username=username, rec_id=rec_id))

    return render_template('main/edit_transaction.html', form=form)

@bp.route('/register/<username>/<id>', methods=['GET', 'POST'])
@login_required
def register(username, id): 
    from sqlalchemy import and_, or_
    
    user = User.query.filter_by(username=username).first()

    page = request.args.get('page', 1, type=int)

    transactions_and_transfers_native = Transactions.acct_id == id

    transfers_foreign = and_(Transactions.type == 'transfer', Transactions.acct_id2 == id)

    filter_args = [transactions_and_transfers_native, transfers_foreign]

    or_filter = or_(*filter_args)

    results = Transactions.query.filter(or_filter).join(Categories, Transactions.cat_id==Categories.id)\
        .add_columns(Categories.name, Transactions.date, Transactions.payee_name, Transactions.amount, Transactions.reconciled, Transactions.type, Transactions.amount2, Transactions.id, Transactions.acct_id)


    results = results.order_by(Transactions.date.asc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)    
    
    for item in results.items:
        print(item)
        
    curbal, startbal = Transactions.get_current_balance(id)

    first_url = url_for('main.register', username=username, id=id,
                        page=1) if results.has_next else None
    final_url = url_for('main.register', username=username, id=id,
                        page=results.pages) if results.has_next else None

    next_url = url_for('main.register', username=username, id=id,
                       page=results.next_num) if results.has_next else None
    prev_url = url_for('main.register', username=username, id=id,
                       page=results.prev_num) if results.has_prev else None


    return render_template('main/register.html', username=username, items=results.items, startbal=startbal, curbal=curbal, next_url=next_url, prev_url=prev_url, lastpage=page, first_url=first_url, final_url=final_url)


'''
reconciliations
'''

@bp.route('/view_reconciliations/<username>/<id>', methods=['GET', 'POST'])
@login_required
def view_reconciliations(username, id):
    user = User.query.filter_by(username=username).first()
    r = Reconciliation.query.filter(Reconciliation.acct_id == id).order_by(Reconciliation.create_date.desc()).all()
    return render_template('main/view_reconciliations.html', items=r, id=id)

@bp.route('/view_reconciliations_by_account/<username>/', methods=['GET', 'POST'])
@login_required
def view_reconciliations_by_account(username):

    user = User.query.filter_by(username=username).first()
    r = Accounts.query.filter(Accounts.user_id == user.id).all()

    account_list = Accounts.accounts_to_dict(r)
    
    return render_template('main/view_reconciliations_by_account.html', items=account_list)

@bp.route('/delete_reconciliation/<username>/<id>/<acct_id>', methods=['GET', 'POST'])
@login_required
def delete_reconciliation(username, id, acct_id):

    user = User.query.filter_by(username=username).first()

    #on delete, release all txn from Reconciled = True
    r = Reconciliation.query.get(id)


    ## should show warning if trying to delete finalized == True
    if r.finalized == True:
        reconciled_is_true_list = json.loads(r.txnjsn)
        
        for item in reconciled_is_true_list:
            txn = Transactions.query.get(item)
            txn.reconciled = False
            db.session.commit()

    db.session.delete(r)
    db.session.commit()
    db.session.close()

    return redirect(url_for('main.view_reconciliations', username=username, id=acct_id))

@bp.route('/start_reconciliation/<username>/<acct_id>', methods=['GET', 'POST'])
@login_required
def start_reconciliation(username, acct_id):
    user = User.query.filter_by(username=username).first()

    result = Reconciliation.query.filter(Reconciliation.acct_id == acct_id).order_by(Reconciliation.end_date.desc()).first()

    if result == None: #this branch is for first reconciliation in the account
        # if no previous reconciliation then use Account.startbal
        account = Accounts.query.get(acct_id)
        form = ReconciliationForm(prior_ending_balance=account.startbal)
    elif result.finalized == None: # this branch is for if continuing last reconciliation if 
        target_rec = Reconciliation.query.get(result.id)  # picks up with selected rec_id

        user = User.query.filter_by(username=username).first()

        page = request.args.get('page', 1, type=int)

        rec = Reconciliation()

        username, results, startbal, curbal, prior_end_bal, rec_id, acct_id = rec.reconciliation_wrapper(
            target_rec=target_rec,                                                            username=username, acct_id=None, page=page, style='continue')

        return render_template('main/reconcile.html', username=username, items=results.items, startbal=startbal, curbal=curbal,  prior_end_bal=prior_end_bal, acct_id=acct_id, rec_id=rec_id)

    else:
        # this branch is for starting a new reconciliation & pre-filling the columns
        #add one day to last end date
        legacy_end_date = result.end_date
        adjusted_start_date = legacy_end_date + timedelta(1)
        form = ReconciliationForm(start_date=adjusted_start_date, prior_end_balance=result.statement_end_bal)


    if form.validate_on_submit():
        new_reconciliation = Reconciliation()
        new_reconciliation.create_date = datetime.utcnow()
        new_reconciliation.user_id = user.id
        new_reconciliation.start_date = form.start_date.data
        new_reconciliation.end_date = form.end_date.data
        new_reconciliation.prior_end_balance = form.prior_end_balance.data
        new_reconciliation.statement_end_bal = form.statement_end_bal.data
        new_reconciliation.acct_id = acct_id
        new_reconciliation.is_first = False
    
        db.session.add(new_reconciliation)
        db.session.commit()
        db.session.close()
        return redirect(url_for('main.reconcile', username=username, acct_id=acct_id))
    return render_template('main/start_reconciliation.html', username=username, form=form, acct_id=acct_id)

@bp.route('/adjust_reconciliation/<username>/<rec_id>', methods=['GET', 'POST'])
@login_required
def adjust_reconciliation(username, rec_id):

    user = User.query.filter_by(username=username).first()

    reconciliation = Reconciliation.query.get(rec_id)

    form = EditReconciliationForm(obj=reconciliation)
    if form.validate_on_submit():
        # reconciliation.create_date = datetime.utcnow()
        reconciliation.start_date = form.start_date.data
        reconciliation.end_date = form.end_date.data
        reconciliation.user_id = user.id
        reconciliation.prior_end_balance = form.prior_end_balance.data
        reconciliation.statement_end_bal = form.statement_end_bal.data
        # reconciliation.acct_id = id

        db.session.commit()
        db.session.close()

        return redirect(url_for('main.view_reconciliations_by_account', username=username))

    return render_template('main/adjust_reconciliation.html', form=form)

@bp.route('/reconcile/<username>/<acct_id>', methods=['GET', 'POST'])
@login_required
def reconcile(username, acct_id):

    # this is a little brittle
    target_rec = Reconciliation.query.order_by(Reconciliation.create_date.desc()).first()

    print(target_rec.id)
    page = request.args.get('page', 1, type=int)

    rec = Reconciliation()

    username, results, startbal, curbal, prior_end_bal, rec_id, acct_id = rec.reconciliation_wrapper(target_rec=target_rec,
        username=username, acct_id=acct_id, page=page)

    print(target_rec.prior_end_balance, startbal.startbal, prior_end_bal)

    return render_template('main/reconcile.html', username=username, items=results.items, startbal=target_rec.prior_end_balance, curbal=curbal,  prior_end_bal=prior_end_bal, acct_id=acct_id, rec_id=rec_id)

@bp.route('/continue_reconcile/<username>/<rec_id>', methods=['GET', 'POST'])
@login_required
def continue_reconcile(username, rec_id):
    print(f'continue reconciliation {rec_id}')
    target_rec = Reconciliation.query.get(rec_id) #picks up with selected rec_id
    
    user = User.query.filter_by(username=username).first()

    page = request.args.get('page', 1, type=int)

    rec = Reconciliation()

    username, results, startbal, curbal, prior_end_bal, rec_id, acct_id = rec.reconciliation_wrapper(target_rec=target_rec,                                                            username=username, acct_id=None, page=page, style='continue')

    return render_template('main/reconcile.html', username=username, items=results.items, startbal=target_rec.prior_end_balance, curbal=curbal,  prior_end_bal=prior_end_bal, acct_id=acct_id, rec_id=rec_id)

@bp.route('/_reconciled_button')
@login_required
def reconciled_button():
    print('RECONCILED BUTTON')
    amount = request.args.get('amount', 0, type=str)

    ids = request.args
    str_id_list = ids.getlist('idArray[]')
    id_list = [int(item) for item in str_id_list]

    id_str_for_db = json.dumps(id_list)

    reconciliation_id = request.args.get('recId', 0, type=str)

    # gets the transactions from id list and marks them as reconciled=True
    for idd in id_list:
        txn = Transactions.query.get(idd)
        txn.reconciled = True #should be True in production

        db.session.commit()
        print(txn)

    current_reconciliation = Reconciliation.query.get(reconciliation_id)

    #finalized the reconciliation
    current_reconciliation.finalized = True
    # stores the reconciliation id list so when we delete reconciliation, the transactions will be released 
    current_reconciliation.txnjsn = id_str_for_db
    print('cur txn:', current_reconciliation.txnjsn)
    current_reconciliation.count = len(id_list)
    db.session.commit()
    return jsonify(result=None)


@bp.route('/reset_reconciliations', methods=['GET', 'POST'])
def reset_reconciliations():
    txns = Transactions.query.all()
    for txn in txns:
        print(txn)
        txn.reconciled = False
        db.session.commit()

@bp.route('/_persist_checkboxes')
@login_required
def persist_checkboxes():
    print('persist checkboxes')
    checkbox_values = request.args
    print(checkbox_values)
    checkbox_str_for_db = json.dumps(checkbox_values)
    print('json dumps CHECKBOXES:', checkbox_str_for_db, type(checkbox_str_for_db))

    reconciliation_id = request.args.get('recId', 0, type=str)

    current_reconciliation = Reconciliation.query.get(reconciliation_id)

    current_reconciliation.checkboxjsn = checkbox_str_for_db
    # db.session.commit()
    # str_checkbox_list = checkbox_values.getlist('checkboxObject{}')
    # print(str_checkbox_list)
    # checkbox_list = [int(item) for item in str_checkbox_list]


    # checkbox_values = request.args
    # str_id_list = ids.getlist('idArray[]')
    # id_list = [int(item) for item in str_id_list]

    # id_str_for_db = json.dumps(id_list)
    # print('json dumps:', id_str_for_db, type(id_str_for_db))



    # amount_list.append(float(amount))
    # amount = sum(amount_list)
    # print('rec id:', reconciliation_id)
    # print('reconciled amount:', amount)
    # print('id list:', id_list)
    # print('message:', message)
    # data = {"this": "is", "just": "a test"}
    # return jsonify(result=amount)
    return jsonify(result=0)


'''
end reconciliation
'''
# action = "/forward/"

@bp.route('/index/<username>/popup', methods=['GET', 'POST'])
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)

@bp.route('/reports/<username>/', methods=['GET', 'POST'])
@login_required
def reports(username):
    form = ReportSelectForm()
    if form.validate_on_submit():
        report_period = form.report_period.data
        report_template = form.report_template.data
        if report_period == 'custom':
            start_date = form.start_date.data
            end_date = form.end_date.data

        total = form.total_by_cat.data

        output_list_of_tuples = Reports.report_query(username=username, start_date=start_date,end_date=end_date, report_template=report_template, report_period=report_period, total=total) 

        flash('lily-livered sumbitch')

        return render_template('main/reports_summary.html', username=username, form=form, transactions=output_list_of_tuples, report_period=report_period)

    return render_template('main/reports_summary.html', username=username, form=form)

@bp.route('/import')
def import_thing():

    payee_name_list = []
    for item in Transactions.query.all():
        print(item.payee_name)
        payee_name_list.append(item.payee_name)

    new_set = set()
    new_set = set(payee_name_list)

    for item in new_set:
        vend = Vendors()
        vend.vendor_name = item
        db.session.add(vend)
        db.session.commit()
    
    db.session.close()

    return 'ok'

'''vendors'''
@bp.route('/vendors/<username>', methods=['GET', 'POST'])
@login_required
def vendors(username):
    user = User.query.filter_by(username=username).first()

    r = Vendors.query.filter(Vendors.user_id == user.id).all()

    return render_template('main/vendors.html', username=username, items=r)

@bp.route('/create_vendor/<username>/', methods=['GET', 'POST'])
@login_required
def create_vendor(username):

    user = User.query.filter_by(username=username).first()

    r = Vendors.query.filter(Vendors.user_id == user.id).all()

    form = VendorCreationForm()
    if form.validate_on_submit():
        new_vendor = Vendors()
        new_vendor.vendor_name = form.vendor_name.data
        new_vendor.user_id = user.id
        db.session.add(new_vendor)
        db.session.commit()
        flash('congratulations, you created a new vendor')
        return redirect(url_for('main.vendors', username=username))
    return render_template('main/create_vendor.html', form=form)

@bp.route('/delete_vendor/<username>/<vendor_id>', methods=['GET', 'POST'])
@login_required
def delete_vendor(username, vendor_id):

    user = User.query.filter_by(username=username).first()

    r = Vendors.query.get(vendor_id)
    print(r)
    db.session.delete(r)
    db.session.commit()
    flash('congratulations, you deleted a vendor')
    return redirect(url_for('main.vendors', username=username))

'''
@bp.route('/deleted/<username>/<id>', methods=['GET', 'POST'])
@login_required
def deleted(username, id):

    user = User.query.filter_by(username=username).first()

    r = Accounts.query.get(id)

    db.session.delete(r)
    db.session.commit()

    # post/redirect/get pattern
    return redirect(url_for('main.accounts', username=username))

@bp.route('/edit_account/<username>/<id>', methods=['GET', 'POST'])
@login_required
def edit_ac
'''









'''db management'''
@bp.route('/createdb')
def createdb():
    db.create_all()
    return 'creating dbs from models'


@bp.route('/dumpdb')
def dumpdb():
    import os
    from datetime import datetime as dt

    from config import Config

    def pg_dump_one():
        bu_time = dt.now()
        print(bu_time)
        os.system(f'pg_dump --dbname={Config.PG_DUMPS_URI} > "{Config.DB_BACKUPS}\lnew_loaderdump{bu_time.month}{bu_time.day}{bu_time.year}{bu_time.hour}.sql"')

    pg_dump_one()
    return 'dumping db to db_backups'
