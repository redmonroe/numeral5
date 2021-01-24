from datetime import datetime
from decimal import Decimal
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
# from guess_language import guess_language
from app import db
from app.main.forms import AccountCreationForm, EditAccountForm, EditCategoryForm, CategoryCreationForm, TransactionCreationForm, EditTransactionForm
from app.models import User, Accounts, Categories, Transactions
# from app.translate import translate
from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
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

    return render_template('main/view_account.html', items=r)

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
        return redirect(url_for('categories', username=username))

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

@bp.route('/create_transaction/<username>/', methods=['GET', 'POST'])
@login_required
def create_transaction(username):
    #username, #account_id

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
        return redirect(url_for('main.register', username=username, id=form.acct_id.data))

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
    print(id)

    r = Transactions.query.get(id)

    db.session.delete(r)
    db.session.commit()
    db.session.close()

    flash('congratulations, you deleted a transaction')
    # post/redirect/get pattern
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
    from sqlalchemy import or_
    
    user = User.query.filter_by(username=username).first()

    # results = []
    page = request.args.get('page', 1, type=int)

    results = Transactions.query.filter(or_(Transactions.user_id == user.id, Transactions.acct_id == id)).order_by(Transactions.date.asc()).paginate(page, current_app.config['ITEMS_PER_PAGE'], False)

    curbal, startbal = Transactions.get_current_balance(id)

    next_url = url_for('main.register', username=username, id=id,
                       page=results.next_num) if results.has_next else None
    prev_url = url_for('main.register', username=username, id=id,
                       page=results.prev_num) if results.has_prev else None


    return render_template('main/register.html', username=username, items=results.items, startbal=startbal, curbal=curbal, next_url=next_url, prev_url=prev_url)




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
@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

'''

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