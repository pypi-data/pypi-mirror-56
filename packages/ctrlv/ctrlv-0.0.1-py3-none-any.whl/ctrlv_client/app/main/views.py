from flask import (
    render_template,
    Blueprint,
    redirect,
    url_for,
    request,
    flash,
    current_app,
    session,
)
from flask_login import current_user, login_user
from ctrlv_client.app.models import User, Snippet
from ctrlv_client.app.main.forms import (
    LoginForm,
    MdeForm,
    DeleteForm,
    FilterForm
)
from ctrlv_client.app.helpers import (
    error_flasher,
    get_sanitized_html,
    truncate_html
)
from ctrlv_client.app import db, SITE_CONFIG_FILE
from sqlalchemy import desc, asc, or_
import os

main = Blueprint(
    'main',
    __name__,
    template_folder='templates/main',
    url_prefix='/'
)


@main.before_request
def before_request():
    # flask_login.login_required not used
    # dynamic reloading
    # https://flask-login.readthedocs.io/en/latest/#protecting-views
    if (
        not current_user.is_authenticated and
        os.path.isfile(SITE_CONFIG_FILE) and
        request.endpoint != 'main.login'
    ):
        return current_app.login_manager.unauthorized()


@main.route('/', methods=['GET', 'POST'])
def index():
    # Defaults
    # can also use dict.get()
    # this makes it more explicit
    snippet_preview_length = 250
    # Why separate dict sorts_available?
    # Cannot store objects directly in session
    # TypeError: <function asc at 0x7f3a33487a60> is not JSON serializable
    sorts_available = {
        'oldest': asc,
        'latest': desc
    }
    filter_params = {
        'limit': int(session.get('limit', 10)),
        'sort': sorts_available[session.get('sort', 'latest')],  # Latest
        'search': f'%{session.get("search", "")}%'  # Everything
    }
    # https://stackoverflow.com/questions/36157362/
    # setting-default-value-after-initialization-in-selectfield-flask-wtforms
    # Once an instance of the form is created,
    # the data is bound. Changing the default after that doesn't do anything.
    # Pass default data to the form constructor,
    # and it will be used if no form data was passed.
    filter_form = FilterForm(
        limit=session.get('limit', 1),
        sort=session.get('sort', 'latest')

    )

    # Filter done by user
    if filter_form.validate_on_submit():
        search = filter_form.search.data
        filter_params['search'] = f'%{search}%'
        # to remember in the form
        session['search'] = search
        limit = filter_form.limit.data
        filter_params['limit'] = int(limit)
        # to remember in the form
        session['limit'] = limit
        sort = filter_form.sort.data
        filter_params['sort'] = sorts_available[sort]
        session['sort'] = sort

    # remember search
    filter_form.search.data = filter_params['search'].replace('%', '')

    # Page number
    page = int(
        request.args.get('page', 1)
    )

    # Get snippets after pagination
    snippets = Snippet.query.filter(
        or_(
            Snippet.snippet_title.like(filter_params['search']),
            Snippet.snippet_text.like(filter_params['search'])
        )
    ).order_by(
        filter_params['sort'](Snippet.snippet_timestamp)

    ).paginate(
        page,
        filter_params['limit'],
        error_out=False
    )

    # modyfing the object directly causes issues
    snippet_holder = []
    for snippet in snippets.items:
        # convert to html
        # Jinja2 striptags is used in the template
        # Escape is turned on by default to prevent XSS
        # truncate(200) used to truncate text
        snippet_holder.append(
            {
                'id': snippet.snippet_id,
                'title': snippet.snippet_title,
                'text': truncate_html(
                        get_sanitized_html(
                            snippet.snippet_text
                        ), snippet_preview_length
                    )
            }
        )

    error_flasher(filter_form)

    return render_template(
        'main/index.html',
        snippet_list=snippet_holder,
        snippets=snippets,
        filter_form=filter_form
    )


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.username.data)
        if user.verify_password(form.password.data):
            login_user(user)
            nxt = request.args.get('next')
            # Verify that 'next' is available and relative
            # Also note:
            # The form action should be left blank
            # if it is given as url_for('login')
            # next parameter will not be available
            if nxt is None or not nxt.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nxt)
        else:
            flash('Invalid username or password', 'error')
    else:
        error_flasher(form)
    # No need for search_from in login
    return render_template('main/login.html', form=form)


@main.route('/new', methods=['GET', 'POST'])
def new():
    form = MdeForm()
    if form.validate_on_submit():
        new_snippet = Snippet(
            snippet_title=form.title.data,
            snippet_text=form.editor.data
        )
        db.session.add(new_snippet)
        db.session.commit()
        flash('Note added successfully!')
        return redirect(url_for('main.index'))
    else:
        error_flasher(form)
    # Reaches here if not a valid POST request
    search_form = FilterForm(
        limit=session.get('limit', 1),
        sort=session.get('sort', 'latest')
    )
    return render_template(
        'main/new.html',
        form=form,
        search_form=search_form
    )


@main.route('view/<int:id>', methods=['GET'])
def view(id):
    snippet = Snippet.query.get_or_404(id)
    # Above code raises 404 if query retuns none
    # so, it's safe to use below code without
    # if snippet:
    html_sanitized = get_sanitized_html(snippet.snippet_text)

    title = snippet.snippet_title
    # Delete form
    delete_form = DeleteForm(snippet_id=id)
    search_form = FilterForm(
        limit=session.get('limit', 1),
        sort=session.get('sort', 'latest')
    )
    return render_template(
        'main/view.html',
        title=title,
        content=html_sanitized,
        id=id,
        delete_form=delete_form,
        search_form=search_form
    )


@main.route('delete/<int:id>', methods=['POST'])
def delete(id):
    delete_form = DeleteForm(snippet_id=id)
    if delete_form.validate_on_submit():
        snippet = Snippet.query.filter_by(snippet_id=id).one()
        db.session.delete(snippet)
        db.session.commit()
        flash('Successfully deleted snippet')
        return redirect(url_for('main.index'))
    error_flasher(delete_form)
    return redirect(url_for('main.view', id=id))


@main.route('edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    snippet = Snippet.query.get_or_404(id)
    # https://wtforms.readthedocs.io/en/stable/crash_course.html#how-forms-get-data
    # If the field names were same as
    # db column names need to use only
    # form = MdeForm(obj=snippet)

    # https://stackoverflow.com/questions/23712986/
    # pre-populate-a-wtforms-in-flask-with-data-from-a-sqlalchemy-object
    # If your form fields don't match the database columns in your model
    # for whatever reason (they should), the form class takes kwargs:
    # **kwargs – If neither formdata or obj contains a value for a field,
    # the form will assign the value of a matching keyword argument
    # to the field, if provided.

    # Main Form
    form = MdeForm(
        obj=snippet,
        title=snippet.snippet_title,
        editor=snippet.snippet_text
    )

    if form.validate_on_submit():
        # https://wtforms.readthedocs.io/en/latest/forms.html#wtforms.form.Form.populate_obj
        # Populates the attributes of the passed obj
        # with data from the form’s fields.
        # If the filed names were same as db column names use only
        # form.populate_obj(snippet)

        # https://wtforms.readthedocs.io/en/stable/crash_course.html#editing-existing-objects
        # We’re also using the form’s populate_obj method to
        # re-populate the user object with the contents of the validated form.
        # This method is provided for convenience, or use when the field names
        # match the names on the object you’re providing with data.
        # Typically, you will want to assign the values manually.
        snippet.snippet_title = form.title.data
        snippet.snippet_text = form.editor.data
        db.session.commit()
        flash("Snippet edited successfully!")
        return redirect(
            url_for('main.view', id=id)
        )
    error_flasher(form)
    search_form = FilterForm(
        limit=session.get('limit', 1),
        sort=session.get('sort', 'latest')
    )
    return render_template(
        'main/edit.html',
        id=id,
        form=form,
        search_form=search_form
    )
