import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()


from django.db import connection
from my_modules import exceptions
from argon2 import PasswordHasher
import datetime


cursor = connection.cursor()
hasher = PasswordHasher()


def get_session_id(request):
    cookie_content = request.COOKIES.get('_login_session')

    try:
        session_id = cookie_content.split('_')[0]
    except:
        session_id = -1

    return session_id


def request_verify(request, login_required):

    session_id = get_session_id(request)

    command = (
        "SELECT COUNT(userid) " +
        "FROM logged_in_users " +
        "WHERE session_id={}".format(session_id)
    )
    cursor.execute(command)
    count = int(cursor.fetchall()[0][0])

    if login_required and count == 0:
        raise exceptions.LoginRequiredException
    elif not login_required and count > 0:
        raise exceptions.LogoutRequiredException
    else:
        return True


def user_verify(request, required_user):
    active_user_type = get_active_user(request)['user_type']

    if required_user != active_user_type:
        raise exceptions.UserRequirementException

    return True


def get_active_user(request):

    session_id = get_session_id(request)

    command = (
        "SELECT userid " +
        "FROM logged_in_users " +
        "WHERE session_id={}".format(session_id)
    )
    cursor.execute(command)
    try:
        query_target = cursor.fetchall()[0][0]
    except IndexError:
        return {}

    command = f"SELECT name, username, id FROM user WHERE id LIKE '{query_target}'"
    cursor.execute(command)

    name, username, userid = cursor.fetchall()[0]

    user_data = {
        'user_id': userid,
        'username': username,
        'user_type': query_target.split('-')[0],
        'name': name,
        'session_id': session_id,
    }

    command = f"DELETE FROM logged_in_users WHERE expires<NOW() AND userid LIKE '{query_target}'"
    cursor.execute(command)

    return user_data


def extend_session(request, response):
    session_id = get_session_id(request)
    user_data = get_active_user(request)

    command = (
        "DELETE FROM logged_in_user " +
        "WHERE session_id={}".format(session_id)
    )
    cursor.execute(command)

    command = (
        "INSERT INTO logged_in_user (userid, expires) " +
        "VALUES ('{}', DATE_ADD(NOW(), INTERVAL 3 DAY))".format(user_data['userid'])
    )
    cursor.execute(command)

    command = (
        "SELECT MAX(session_id) FROM logged_in_user"
    )
    cursor.execute(command)

    session_id = int(cursor.fetchall()[0][0])

    cookie_content = "{}_{}".format(session_id, user_data['username'])

    cookie_expires = datetime.datetime.now() + datetime.timedelta(hours=66)
    cookie_expires = cookie_expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie('_login_session', cookie_content, expires=cookie_expires)

    return response
