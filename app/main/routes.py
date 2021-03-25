from datetime import datetime
from decimal import Decimal
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
# from guess_language import guess_language
from app import db
from app.main.forms import AccountCreationForm, EditAccountForm, EditCategoryForm, CategoryCreationForm, TransactionCreationForm, EditTransactionForm, ReconciliationForm, EditReconciliationForm, EmptyForm, ReportSelectForm
from app.models import User, Accounts, Categories, Transactions, Reconciliation, Reports
# from app.translate import translate
from app.main import bp


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

    for item in r:
        print(item)
    # flash('congratulations, you deleted an account')
    # post/redirect/get pattern
    return render_template('main/transactions.html', username=username, items=r)

@bp.route('/create_transaction/<username>/<lastpage>/', methods=['GET', 'POST'])
@login_required
def create_transaction(username, id=None, lastpage=None):
    #username, #account_id
    
    print(lastpage)
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
        new_transaction = Transactions()
        new_transaction.user_id = user.id
        new_transaction.date = form.date.data
        new_transaction.type = form.type.data
        new_transaction.amount = form.amount.data
        new_transaction.payee_name = form.payee_name.data
        new_transaction.acct_id = form.acct_id.data
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
        return redirect(url_for('main.register', username=username, id=form.acct_id.data, page=lastpage))

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

    flash('congratulations, you deleted a transaction')
    return redirect(url_for('main.register', username=username, id=acct))

@bp.route('/edit_transaction/<username>/<id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(username, id):
    
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
    #     # post/redirect/get pattern
        return redirect(url_for('main.transactions', username=username))

    return render_template('main/edit_transaction.html', form=form)

@bp.route('/register/<username>/<id>', methods=['GET', 'POST'])
@login_required
def register(username, id):
    from sqlalchemy import or_, and_
    
    user = User.query.filter_by(username=username).first()

    page = request.args.get('page', 1, type=int)

    transactions_and_transfers_native = Transactions.acct_id == id

    transfers_foreign = and_(Transactions.type == 'transfer', Transactions.acct_id2 == id)

    filter_args = [transactions_and_transfers_native, transfers_foreign]

    or_filter = or_(*filter_args)

    results = Transactions.query.filter(or_filter) 

    results = results.order_by(Transactions.date.asc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)

    
        
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

    #TODO: add last reconciled date

    user = User.query.filter_by(username=username).first()
    r = Accounts.query.filter(Accounts.user_id == user.id).all()

    account_list = Accounts.accounts_to_dict(r)
    
    return render_template('main/view_reconciliations_by_account.html', items=account_list)

@bp.route('/delete_reconciliation/<username>/<id>/<acct_id>', methods=['GET', 'POST'])
@login_required
def delete_reconciliation(username, id, acct_id):

    user = User.query.filter_by(username=username).first()

    r = Reconciliation.query.get(id)

    db.session.delete(r)
    db.session.commit()
    db.session.close()

    return redirect(url_for('main.view_reconciliations', username=username, id=acct_id))

@bp.route('/start_reconciliation/<username>/<id>', methods=['GET', 'POST'])
@login_required
def start_reconciliation(username, id):
    user = User.query.filter_by(username=username).first()

    # if no previous reconciliation then use startbal
    # r = Reconciliation.query.filter(Reconciliation.acct_id == id).order_by(Reconciliation.date.desc()).first()

    # if r == None:
    form = ReconciliationForm()
    if form.validate_on_submit():
        new_reconciliation = Reconciliation()
        new_reconciliation.create_date = datetime.utcnow()
        new_reconciliation.user_id = user.id
        new_reconciliation.start_date = form.start_date.data
        new_reconciliation.end_date = form.end_date.data
        new_reconciliation.prior_end_balance = form.prior_end_balance.data
        new_reconciliation.statement_end_bal = form.statement_end_bal.data
        new_reconciliation.acct_id = id
    
        db.session.add(new_reconciliation)
        db.session.commit()
        db.session.close()
        flash('congratulations, you started reconciling . . .')
        return redirect(url_for('main.reconcile', username=username, acct_id=id))
    return render_template('main/start_reconciliation.html', username=username, form=form, acct_id=id)

@bp.route('/adjust_reconciliation/<username>/<rec_id>', methods=['GET', 'POST'])
@login_required
def adjust_reconciliation(username, rec_id):

    user = User.query.filter_by(username=username).first()

    reconciliation = Reconciliation.query.get(rec_id)

    form = EditReconciliationForm(obj=reconciliation)
    if form.validate_on_submit():
        reconciliation.create_date = datetime.utcnow()
        reconciliation.user_id = user.id
        reconciliation.start_date = form.start_date.data
        reconciliation.end_date = form.end_date.data
        reconciliation.prior_end_balance = form.prior_end_balance.data
        reconciliation.statement_end_bal = form.statement_end_bal.data
        reconciliation.acct_id = id

    return render_template('main/adjust_reconciliation.html', form=form)
    #this comes from view rec by account

@bp.route('/reconcile/<username>/<acct_id>', methods=['GET', 'POST'])
@login_required
def reconcile(username, acct_id):
    #ingredients
        # transactions by account
        # between start and end dates


    most_recent_reconciliation = Reconciliation.query.order_by(Reconciliation.create_date.desc()).first()

    from sqlalchemy import or_, and_
    
    user = User.query.filter_by(username=username).first()

    page = request.args.get('page', 1, type=int)

    ## this can be reduced along with searches in 

    transactions_and_transfers_native = Transactions.acct_id == acct_id

    transfers_foreign = and_(Transactions.type == 'transfer', Transactions.acct_id2 == acct_id)

    reconciliation_dates = and_(Transactions.date >= most_recent_reconciliation.start_date, Transactions.date <= most_recent_reconciliation.end_date) # start & end dates come from query for most recent reconciliation

    filter_args = [transactions_and_transfers_native, transfers_foreign]

    or_filter = or_(*filter_args)

    results = Transactions.query.filter(or_filter) 

    results = Transactions.query.filter(reconciliation_dates)

    results = results.order_by(Transactions.date.asc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
        
    curbal, startbal = Transactions.get_current_balance(acct_id)

    prior_end_bal = most_recent_reconciliation.statement_end_bal
   
    
    next_url = url_for('main.reconcile', username=username, id=id,
                       page=results.next_num) if results.has_next else None
    prev_url = url_for('main.reconcile', username=username, id=id,
                       page=results.prev_num) if results.has_prev else None


    return render_template('main/reconcile.html', username=username, items=results.items, startbal=startbal, curbal=curbal, next_url=next_url, prev_url=prev_url, prior_end_bal=prior_end_bal)


@bp.route('/_reconciled')
@login_required
def reconciled():
    amount_list = []
    difference_list = []

    amount = request.args.get('amount', 0, type=str)
    difference = request.args.get('difference', 0, type=str)    
   
    amount_list.append(float(amount))
    difference_list.append(float(amount))
    amount = sum(amount_list)
    difference = sum(difference_list)
    print(amount)
    print('difference:', difference)
    return jsonify(result=amount)


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
        total = form.total_by_cat.data

        output_list_of_tuples = Reports.report_query(username=username, report_template=report_template, report_period=report_period, total=total) 

        flash('lily-livered sumbitch')

        return render_template('main/reports_summary.html', username=username, form=form, transactions=output_list_of_tuples, report_period=report_period)

    return render_template('main/reports_summary.html', username=username, form=form)


# '''

# start_bal = s.query(Accounts).filter(
#         Accounts.id == account_to_reconcile).first()

# starting_balance = Decimal(start_bal.startbal)

# start = prior_month_end_bal
# print('---' * 30)
# for item in stuff_check:
#     """if matching account is is acct_id then use amount, else use amount2"""
#     if item.acct_id == account_to_reconcile:
#         run_bal = start + item.amount
#         print(item, run_bal)
#         start = run_bal
#     elif item.acct_id2 == account_to_reconcile:
#         run_bal = start + item.amount2
#         print(item, run_bal)
#         start = run_bal


# discrepancy = 0        
# acct_end_bal = start
# discrepancy = acct_end_bal - statement_end_bal

# print(f'\nCurrent difference {discrepancy}.')

# print(f'\nShowing items from account {account_to_reconcile} from {strt_dt} to {end_dt}.\n')

# throwaway view to run a function within context of app

@bp.route('/import')
def import_thing():

    filename = 'category_list_for_load_category_function.csv'
    with open(filename, 'rt') as f:
        username = 'joe'
        header = next(f)
        cats = []
        for line in f:
            print(line)
            c = Categories()
            nl = line.split(',')
            c.name = nl[1]
            c.inorex = nl[2].strip()
            c.user_id = 1
            # db.session.add(c)
            db.session.commit()
    return redirect(url_for('main.index'))




'''
@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot follow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('You are following %(username)s!', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('User %(username)s not found.', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('You cannot unfollow yourself!'))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('You are not following %(username)s.', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})
'''
