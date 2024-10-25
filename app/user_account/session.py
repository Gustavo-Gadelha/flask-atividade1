from flask import session


def create_session(user):
    session['user_id'] = user.id
    session['user_name'] = user.username
    session['authenticated'] = True


def teardown_session():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('authenticated', None)


def has_session():
    return session_id() is not None and session_name() is not None and session_authenticated()


def session_id():
    return session.get('user_id')


def session_name():
    return session.get('user_name')


def session_authenticated():
    return session.get('authenticated')
