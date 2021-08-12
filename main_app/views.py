from my_modules import page_works, exceptions, classes, database, utilities
from django.shortcuts import render
from django.db import connection
from pathlib import Path
import datetime
import math
import os

cursor = connection.cursor()

base_dir = Path('__file__').resolve().parent.parent
text_files_dir = os.path.join(base_dir, 'text_files')
temp_files_dir = os.path.join(base_dir, 'temp_files')


def test_page(request):

    data_dict = {
        'page_name': 'test_page',
    }

    user_dict = page_works.get_active_user(request)

    try:
        data_dict['user_id'] = user_dict['user_id']
        data_dict['name'] = user_dict['name']
        data_dict['user_type'] = user_dict['user_type']
        data_dict['login_status'] = 'true'
    except KeyError:
        data_dict['login_status'] = 'false'

    data_dict['image'] = 'H-1_HOS-4_electbill.png'

    data_dict['days'] = range(32)[1:]
    data_dict['months'] = 'January,February,March,April,May,June,July,August,September,October,November,December'.split(',')
    data_dict['years'] = range(2022)[1990:]

    return render(request, 'main_app/test_page.html', context=data_dict)


def setup_admin_page(request):
    return render(request, 'main_app/setup_admin_page.html', context={})


def setup_admin(request):

    name = request.POST.get('name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    address = request.POST.get('address')

    command = f'select count(*) from user where id like "A%"'
    cursor.execute(command)
    user_id = f'A-{cursor.fetchall()[0][0] + 1}'

    command = f'insert into user values ("{user_id}", "{name}", "{username}", "{password}", "null", CURRENT_DATE , "null", "null", "{gender}", "{phone}", "{email}", "{address}", 1, 9)'
    cursor.execute(command)

    return login_page(request)


def error_404(request, exception=''):

    try:
        page_works.request_verify(request, True)

        user_dict = page_works.get_active_user(request)

        data_dict = {
            'name': user_dict['name'],
            'logged_in_username': user_dict['username'],
            'user_type': user_dict['user_type'],
            'page_name': '404_page',
            'login_status': 'true',
        }

    except exceptions.LoginRequiredException:
        pass

    return render(request, 'main_app/404_page.html', context=data_dict)


def error_500(request, template_name='500.html'):

    data_dict = {}

    try:
        page_works.request_verify(request, True)

        user_dict = page_works.get_active_user(request)

        data_dict = {
            'name': user_dict['name'],
            'logged_in_username': user_dict['username'],
            'user_type': user_dict['user_type'],
            'page_name': '404_page',
            'login_status': 'true',
        }
    except exceptions.LoginRequiredException:
        pass

    return render(request, template_name, context=data_dict)


def requests_loader_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'admin_hostel_loader_page',
        'login_status': 'true',
    }

    command = 'select id from user where verified=0'
    cursor.execute(command)
    users = [user[0] for user in cursor.fetchall()]

    command = 'select hostel_id from hostel where verified=0'
    cursor.execute(command)
    hostels = [hostel[0] for hostel in cursor.fetchall()]

    command = 'select ads_id from advertise where approved=0'
    cursor.execute(command)
    ads = [ad[0] for ad in cursor.fetchall()]

    data_dict['users'] = users
    data_dict['hostels'] = hostels
    data_dict['ads'] = ads

    return render(request, 'main_app/requests_loader_page.html', context=data_dict)


def requests_loader(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    req_type = request.POST.get('req_type')

    if req_type == 'hostels':
        return hostel_approval_page(request)
    elif req_type == 'ads':
        return ad_approval_page(request)
    elif req_type == 'users':
        return user_approval_page(request)
    else:
        return home_page(request)


def ad_approval_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    ads_id = request.POST.get('ads_id')

    if not ads_id:
        return requests_loader_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'admin_home_page',
        'login_status': 'true',
        'ads_id': ads_id,
    }

    return render(request, 'main_app/ad_approval_page.html', context=data_dict)


def approve_ad(request, ads_id):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    ad = classes.Advertise()
    ad.load(ads_id)
    ad.approved = 1
    ad.active = 1
    ad.save()

    return requests_loader_page(request)


def hostel_approval_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    hostel_id = request.POST.get('hostel_id')

    if hostel_id:

        hostel = classes.Hostel()
        hostel.load(hostel_id)

        command = f'select name, phone_number from user where id like "{hostel.hostel_owner_id}"'
        cursor.execute(command)

        hostel_owner_name, phone_number = cursor.fetchall()[0]

        user_dict = page_works.get_active_user(request)

        data_dict = {
            'user_id': user_dict['user_id'],
            'name': user_dict['name'],
            'logged_in_username': user_dict['username'],
            'user_type': user_dict['user_type'],
            'page_name': 'admin_home_page',
            'login_status': 'true',
            'hostel_name': hostel.hostel_name,
            'hostel_owner_name': hostel_owner_name,
            'phone_number': phone_number,
            'hostel_id': hostel.hostel_id,
            'hostel_house_number': hostel.house_number,
            'hostel_road_number': hostel.road_number,
            'hostel_thana': hostel.thana,
            'hostel_postal_code': hostel.postal_code,
            'hostel_photo': hostel.photo,
            'hostel_electricity_bill': hostel.electricity_bill,
            'hostel_document': hostel.hostel_document,
        }

        return render(request, 'main_app/hostel_approval_page.html', context=data_dict)
    else:
        return requests_loader_page(request)


def approve_hostel(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    hostel_id = request.POST.get('hostel_id')
    command = f'update hostel set verified=1, active=1 where hostel_id like "{hostel_id}"'
    cursor.execute(command)

    return requests_loader_page(request)


def user_approval_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    user_id = request.POST.get('user_id')

    if user_id:

        data_dict = {
            'user_id': user_dict['user_id'],
            'name': user_dict['name'],
            'logged_in_username': user_dict['username'],
            'user_type': user_dict['user_type'],
            'page_name': 'admin_home_page',
            'login_status': 'true',

            'user_id_': user_id,
            'user_type_': 0 if user_id.split('-')[0] == 'S' else 1,
        }

        return render(request, 'main_app/user_approval_page.html', context=data_dict)

    else:
        return requests_loader_page(request)


def approve_user(request, user_id, user_type):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    if user_type == 0:
        student = classes.Student()
        student.load_student(user_id)
        student.verified = 1
        student.active = 1
        student.save_student()
    else:
        hostel_owner = classes.HostelOwner()
        hostel_owner.load_hostel_owner(user_id)
        hostel_owner.verified = 1
        hostel_owner.active = 1
        hostel_owner.save_hostel_owner()

    return requests_loader_page(request)


def registration_page(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    data_dict = {
        'page_name': 'registration_page',
        'login_status': 'false',
        'institutions': utilities.all_institutes()[1:],
    }

    return render(request, 'main_app/registration_page.html', context=data_dict)


def student_registration(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    student = classes.Student()

    student.create_student({
        'name':  request.POST.get('s_name'),
        'username': request.POST.get('s_username'),
        'password': request.POST.get('s_password'),
        'dob': request.POST.get('s_dob'),
        'gender': request.POST.get('s_gender'),
        'email': request.POST.get('s_email'),
        'phone_number': request.POST.get('s_phone_number'),
        'permanent_address': request.POST.get('s_permanent_address'),
        'institution': request.POST.get('institution'),
        'degree': request.POST.get('degree'),
        'student_id': request.POST.get('student_id')
    }, {
        'profile_picture': request.FILES['s_profile_picture'],
        'nid': request.FILES['s_nid'],
        'birth_certificate': request.FILES['s_birth_certificate'],
    })

    student.save_student()

    return login_page(request)


def hostel_owner_registration(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    hostel_owner = classes.HostelOwner()

    hostel_owner.create_hostel_owner({
        'name':  request.POST.get('h_name'),
        'username': request.POST.get('h_username'),
        'password': request.POST.get('h_password'),
        'dob': request.POST.get('h_dob'),
        'gender': request.POST.get('h_gender'),
        'email': request.POST.get('h_email'),
        'phone_number': request.POST.get('h_phone_number'),
        'occupation': request.POST.get('occupation'),
        'permanent_address': request.POST.get('h_permanent_address'),
    }, {
        'profile_picture': request.FILES['h_profile_picture'],
        'nid': request.FILES['h_nid'],
        'birth_certificate': request.FILES['h_birth_certificate'],
    })

    hostel_owner.save_hostel_owner()

    return login_page(request)


def login_page(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    data_dict = {
        'page_name': 'login_page',
        'login_status': 'false',
    }

    return render(request, 'main_app/login_page.html', context=data_dict)


def login(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    if request.method == 'GET':
        return login_page(request)

    username = request.POST.get('username')
    get_password = request.POST.get('password')
    user = "null"

    command = f"select id, password from user where username like '{username}'"
    cursor.execute(command)

    try:
        user_id, password = cursor.fetchall()[0]
    except IndexError:
        return login_page(request)

    user = user_id.split('-')[0]

    if user == 'null':
        return login_page(request)

    password_verified = False

    if password == get_password:
        password_verified = True

    c_user = classes.User()
    c_user.load(user_id)

    if password_verified and c_user.verified == 1:

        command = (
            "SELECT name FROM user " +
            "WHERE username LIKE '{}'".format(username)
        )
        cursor.execute(command)

        name = cursor.fetchall()[0][0]

        command = (
            "INSERT INTO logged_in_users (userid, expires) " +
            "VALUES ('{}', DATE_ADD(NOW(), INTERVAL 3 DAY))".format(user_id)
        )
        cursor.execute(command)

        command = (
            "SELECT MAX(session_id) FROM logged_in_users"
        )
        cursor.execute(command)

        session_id = int(cursor.fetchall()[0][0])

        cookie_content = "{}_{}".format(session_id, username)

        cookie_expires = datetime.datetime.now() + datetime.timedelta(hours=66)
        cookie_expires = cookie_expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

        data_dict = {
            'user_id': user_id,
            'name': name,
            'logged_in_username': username,
            'user_type': user,
            'login_status': 'true',
        }

        if user == 'S':
            data_dict['page_name'] = 'student_home_page'
            response = render(request, 'main_app/student_home_page.html', context=data_dict)
        elif user == 'H':
            data_dict['page_name'] = 'hostel_owner_home_page'
            response = render(request, 'main_app/hostel_owner_home_page.html', context=data_dict)
        elif user == 'A':
            data_dict['page_name'] = 'admin_home_page'
            response = render(request, 'main_app/admin_home_page.html', context=data_dict)
        else:
            return logout(request)

        response.set_cookie('_login_session', cookie_content, expires=cookie_expires)

        return response
    else:
        data_dict = {
            'username': username,
            'page_name': 'login_page',
            'login_status': 'false',
        }
        return render(request, 'main_app/login_page.html', context=data_dict)


def logout(request):
    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    session_id = user_dict['session_id']

    command = (
        "DELETE FROM logged_in_users WHERE session_id={}".format(session_id)
    )
    cursor.execute(command)

    return login_page(request)


def landing_page(request):
    data_dict = {
        'page_name': 'landing_page',
        'login_status': 'false',
        'thanas': utilities.all_thana()
    }

    data_dict['thanas'][0] = 'Any'

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return render(request, 'main_app/landing_page.html', context=data_dict)


def home_page(request):
    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    if user_dict['user_type'] == 'S':
        return student_home_page(request)
    elif user_dict['user_type'] == 'H':
        return hostel_owner_home_page(request)
    elif user_dict['user_type'] == 'A':
        return admin_home_page(request)
    else:
        return logout(request)


def admin_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'admin_home_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/admin_home_page.html', context=data_dict)


def student_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'S')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'student_home_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/student_home_page.html', context=data_dict)


def hostel_owner_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'H')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'hostel_owner_home_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/hostel_owner_home_page.html', context=data_dict)


def profile_page(request, user, user_id):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    if user == 0:
        return student_profile_page(request, user_id)
    elif user == 1:
        return hostel_owner_profile_page(request, user_id)
    elif user == 9:
        return admin_profile_page(request, user_id)


def admin_profile_page(request, user_id):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'admin_profile_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/admin_profile_page.html', context=data_dict)


def student_profile_page(request, user_id):

    try:
        page_works.user_verify(request, 'S')
    except exceptions.UserRequirementException:
        return home_page(request)

    student = classes.Student()
    student.load_student(user_id)
    hostel = classes.Hostel()
    hostel_dict = {}

    try:
        hostel.load(student.current_hostel_id)

        hostel_owner = classes.HostelOwner()
        hostel_owner.load_hostel_owner(hostel.hostel_owner_id)

        hostel_dict = {
            'hostel_found': 'true',
            'hostel_photo': hostel.photo,
            'hostel_id': hostel.hostel_id,
            'hostel_name': hostel.hostel_name,
            'hostel_rating': hostel.rating if hostel.rating != -1 else 'UNRATED',
            'hostel_location': hostel.thana,
            'hostel_contact': hostel_owner.phone_number,
        }

    except exceptions.HostelNotFoundException:
        hostel_dict = {'hostel_found': 'false'}

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'student_profile_page',
        'login_status': 'true',
    }

    data_dict = utilities.add_dictionary(data_dict, hostel_dict)

    return render(request, 'main_app/student_profile_page.html', context=data_dict)


def hostel_owner_profile_page(request, user_id):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'H')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'hostel_owner_profile_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/hostel_owner_profile_page.html', context=data_dict)


def add_hostel_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'H')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'hostel_owner_home_page',
        'login_status': 'true',
        'thanas': utilities.all_thana()
    }

    return render(request, 'main_app/add_hostel_page.html', context=data_dict)


def add_hostel(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'H')
    except exceptions.UserRequirementException:
        return home_page(request)

    hostel_owner_id = page_works.get_active_user(request)['user_id']
    name = request.POST.get('name')
    thana = request.POST.get('thana')
    postal_code = request.POST.get('postal_code')
    house_no = request.POST.get('house_no')
    road_no = request.POST.get('road_no')

    new_hostel = classes.Hostel()
    new_hostel.create({
            'hostel_owner_id': hostel_owner_id,
            'hostel_name': name,
            'thana': thana,
            'road_number': road_no,
            'house_number': house_no,
            'postal_code': postal_code,
        }, {
            'electricity_bill': request.FILES['electricity_bill'],
            'hostel_document': request.FILES['other_valid_doc'],
            'photo': request.FILES['image'],
        }
    )

    new_hostel.save()

    return hostel_owner_home_page(request)


def process_hostel_review_and_rating(request, user_id, hostel_id):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'S')
    except exceptions.UserRequirementException:
        return home_page(request)

    rating = request.POST.get('rate')
    review = request.POST.get('review')

    data = {
        'student_id': user_id,
        'hostel_id': hostel_id,
        'rating': rating,
        'review': review,
    }
    new_hostel_rating = classes.HostelRating()
    new_hostel_rating.create(data)
    new_hostel_rating.save()

    new_hostel_review = classes.HostelReview()
    new_hostel_review.create(data)
    new_hostel_review.save()

    return student_profile_page(request, user_id)


def ad_posting_page(request):
    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'H')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    hostels = database.load_hostels()

    hostel_id_name = []

    for hostel in hostels:
        if hostel.hostel_owner_id == user_dict['user_id'] and hostel.verified == 1:
            hostel_id_name.append(f'{hostel.hostel_id} {hostel.hostel_name}')

    ins_names = utilities.all_institutes()

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'ad_posting_page',
        'login_status': 'true',
        'hostels': hostel_id_name,
        'ins_names': ins_names,
    }

    return render(request, 'main_app/ad_posting_page.html', context=data_dict)


def ad_posting(request):
    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'H')
    except exceptions.UserRequirementException:
        return home_page(request)

    hostel = request.POST.get('hostel').split()[0]
    total_seats = request.POST.get('total_seats')
    per_room_seats = request.POST.get('per_room_seats')
    rent = request.POST.get('rent')
    room_description = request.POST.get('room_description')
    meal_description = request.POST.get('meal_description')
    facility_description = request.POST.get('facility_description')
    preferred_institutions = [request.POST.get('preferred_institution')]
    rules = request.POST.get('rules')
    conditions = request.POST.get('conditions')

    new_advertise = classes.Advertise()
    new_advertise.create({
            'hostel_id': hostel,
            'room_description': room_description,
            'meal_description': meal_description,
            'facilities_description': facility_description,
            'preferred_institutions': preferred_institutions,
            'rent': rent,
            'rules': rules,
            'conditions': conditions,
            'per_room_seats': per_room_seats,
            'total_seats': total_seats,
        }, {
            'room_photo': request.FILES['room_photo_1'],
            'room_photo_2': request.FILES['room_photo_2'],
            'room_photo_3': request.FILES['room_photo_3'],
        }
    )

    new_advertise.save()

    return home_page(request)


def ads_feed_page(request, page_number, location, institute, budget_from, budget_to):

    login_status = 'true'

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        login_status = 'false'

    data_dict = {}

    if login_status == 'true':

        user_dict = page_works.get_active_user(request)
        data_dict = {
            'user_id': user_dict['user_id'],
            'name': user_dict['name'],
            'logged_in_username': user_dict['username'],
            'user_type': user_dict['user_type'],
            'page_name': 'ad_feed_page',
            'login_status': 'true',
        }

    else:
        data_dict = {
            'page_name': 'ads_feed_page',
            'login_status': 'false',
        }

    criteria_dict = {}

    if page_number == 0 and location == 'null':

        location = 'Any' if not request.POST.get('location') else request.POST.get('location')
        institute = 'Any' if not request.POST.get('institute') else request.POST.get('institute')
        budget_from = request.POST.get('budget_from')
        budget_to = request.POST.get('budget_to')

        try:
            budget_from = int(budget_from)
        except:
            budget_from = 0

        if request.POST.get('budget_to') != 'inf':
            try:
                budget_to = int(budget_to)
            except:
                budget_to = 'inf'

    criteria_dict = {
        'location': location,
        'institute': institute,
        'budget': {
            'from': int(budget_from),
            'to': math.inf if budget_to == 'inf' else int(budget_to),
        },
    }

    data_dict = utilities.add_dictionary(data_dict, classes.AdsFeed(criteria_dict).get_feed_data_for(page_number))

    return render(request, 'main_app/ads_feed_page.html', context=data_dict)


def complaint_box_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'complaint_box_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/complaint_box_page.html', context=data_dict)


def complaint_box(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_id = page_works.get_active_user(request)['user_id']
    subject = request.POST.get('subject')
    complaint = request.POST.get('details')

    new_complaint = classes.Complaint()

    new_complaint.create(
        {
            'user_id': user_id,
            'subject': subject,
            'complaint': complaint,
        },
        {
            'photo': request.FILES['photo'],
        }
    )
    new_complaint.save()

    return home_page(request)


def complaint_checker_page(request, complaint_id='null'):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'user_id': user_dict['user_id'],
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'complaint_checker_page',
        'login_status': 'true',
        'all_resolved': 'false',
    }

    current_complaint = {
        'loaded_complaint_id': complaint_id,
    }

    complaints = database.load_complaints()

    complaint_id_sub = []

    unresolved = 0

    for complaint in complaints:
        if complaint.resolved == 0:
            unresolved += 1

            complaint_id_sub.append([complaint.complaint_id, complaint.subject])

            if complaint_id != 'null' and complaint.complaint_id == complaint_id:

                user = classes.User()
                user.load(complaint.user_id)

                utilities.add_dictionary(current_complaint, {
                    'loaded_complaint_subject': complaint.subject,
                    'loaded_complaint_description': complaint.complaint,
                    'loaded_complaint_attachment': complaint.photo,
                    'loaded_user_id_name': f'{user.id} {user.name}',
                    'loaded_user_contact': [user.phone_number, user.email],
                })

    if unresolved == 0:
        data_dict['all_resolved'] = 'true'
        return render(request, 'main_app/complaint_checker_page.html', context=data_dict)

    data_dict['complaints'] = complaint_id_sub

    data_dict = utilities.add_dictionary(data_dict, current_complaint)

    return render(request, 'main_app/complaint_checker_page.html', context=data_dict)


def resolve_complaint(request, complaint_id):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    if complaint_id != 'null':
        complaint = classes.Complaint()
        complaint.load(complaint_id)
        complaint.resolved = 1
        complaint.save()

    return complaint_checker_page(request)
