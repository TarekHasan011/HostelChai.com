import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django

django.setup()

from django.db import connection
from django.conf import settings
import math
from PIL import Image

from . import database, exceptions, utilities

cursor = connection.cursor()


class User:

    def __init__(self):
        pass

    def load(self, user_id):
        command = f'select * from user where id like "{user_id}"'
        cursor.execute(command)

        data = cursor.fetchall()[0]

        self.id = data[0]
        self.name = data[1]
        self.username = data[2]
        self.password = data[3]
        self.profile_picture = data[4]
        self.dob = data[5]
        self.nid = data[6]
        self.birth_certificate = data[7]
        self.gender = data[8]
        self.phone_number = data[9]
        self.email = data[10]
        self.permanent_address = data[11]
        self.verified = data[12]
        self.user_type = data[13]

    def create(self, user_type, data, files):

        command = f'select count(*) from user where user_type={user_type}'
        cursor.execute(command)

        user_type_count = cursor.fetchall()[0][0]
        user_type_string = ''

        if user_type == 0:
            user_type_string = 'S'
        elif user_type == 1:
            user_type_string = 'H'
        elif user_type == 9:
            user_type_string = 'A'

        self.user_type = user_type
        self.id = f'{user_type_string}-{user_type_count + 1}'
        self.name = data['name']
        self.username = data['username']
        self.password = data['password']
        self.dob = data['dob']
        self.gender = data['gender']
        self.phone_number = data['phone_number']
        self.email = data['email']
        self.permanent_address = data['permanent_address']

        self.profile_picture = f'{self.id}_profile_picture.png'
        self.nid = f'{self.id}_nid.png'
        self.birth_certificate = f'{self.id}_birth_certificate.png'

        self.files = {
            'profile_picture': Image.open(files['profile_picture']),
            'nid': Image.open(files['nid']),
            'birth_certificate': Image.open(files['birth_certificate']),
        }

        self.verified = 0

    def save(self):

        command = f'select count(*) from user where id like "{self.id}"'
        cursor.execute(command)
        user_count = cursor.fetchall()[0][0]

        if user_count == 0:

            self.files['profile_picture'].save(f'{settings.MEDIA_ROOT}/{self.profile_picture}')
            self.files['nid'].save(f'{settings.MEDIA_ROOT}/{self.nid}')
            self.files['birth_certificate'].save(f'{settings.MEDIA_ROOT}/{self.birth_certificate}')

            command = (
                f'insert into user values (' +
                f'"{self.id}", ' +
                f'"{self.name}", ' +
                f'"{self.username}", ' +
                f'"{self.password}", ' +
                f'"{self.profile_picture}", ' +
                f'"{self.dob}", ' +
                f'"{self.nid}", ' +
                f'"{self.birth_certificate}", ' +
                f'"{self.gender}", ' +
                f'"{self.phone_number}", ' +
                f'"{self.email}", ' +
                f'"{self.permanent_address}", ' +
                f'{self.verified}, ' +
                f'{self.user_type}' +
                f')'
            )
            cursor.execute(command)
        else:

            command = (
                f'update user set ' +
                # f'id="{self.id}", ' +
                f'name="{self.name}", ' +
                f'username="{self.username}", ' +
                f'password="{self.password}", ' +
                f'profile_picture="{self.profile_picture}", ' +
                f'dob="{self.dob}", ' +
                f'nid="{self.nid}", ' +
                f'birth_certificate="{self.birth_certificate}", ' +
                f'gender="{self.gender}", ' +
                f'phone_number="{self.phone_number}", ' +
                f'email="{self.email}", ' +
                f'permanent_address="{self.permanent_address}", ' +
                f'verified={self.verified}, ' +
                f'user_type={self.user_type} ' +
                f'where id like "{self.id}"'
            )

            cursor.execute(command)


class HostelOwner(User):

    def __init__(self):
        User.__init__(self)

    def load_hostel_owner(self, user_id):
        User.load(self, user_id)

        command = f'select * from hostel_owner where user_id like "{user_id}"'
        cursor.execute(command)

        data = cursor.fetchall()[0]

        self.user_id = self.id
        self.occupation = data[1]
        self.due = data[2]
        self.active = data[3]

    def create_hostel_owner(self, data, files):

        User.create(self, 1, {
            'name': data['name'],
            'username': data['username'],
            'password': data['password'],
            'dob': data['dob'],
            'gender': data['gender'],
            'email': data['email'],
            'phone_number': data['phone_number'],
            'permanent_address': data['permanent_address'],
        }, {
            'profile_picture': files['profile_picture'],
            'nid': files['nid'],
            'birth_certificate': files['birth_certificate'],
        })

        self.user_id = self.id
        self.occupation = data['occupation']
        self.due = 0
        self.active = 0

    def save_hostel_owner(self):
        User.save(self)

        command = f'select count(*) from hostel_owner where user_id like "{self.id}"'
        cursor.execute(command)

        hostel_owner_count = cursor.fetchall()[0][0]

        if hostel_owner_count == 0:
            command = f'insert into hostel_owner values ("{self.user_id}", "{self.occupation}", {self.due}, {self.verified})'
            cursor.execute(command)
        else:
            command = (
                f'update hostel_owner set ' +
                f'occupation="{self.occupation}", ' +
                f'due={self.due}, ' +
                f'active={self.verified} ' +
                f'where user_id like "{self.user_id}"'
            )
            cursor.execute(command)


class Student(User):

    def __init__(self):
        User.__init__(self)

    def load_student(self, user_id):
        User.load(self, user_id)

        command = f'select * from student where user_id like "{user_id}"'
        cursor.execute(command)

        data = cursor.fetchall()[0]

        self.user_id = self.id
        self.institution = data[1]
        self.degree = data[2]
        self.student_id = data[3]
        self.current_hostel_id = data[4]

    def create_student(self, data, files):

        User.create(self, 0, {
            'name': data['name'],
            'username': data['username'],
            'password': data['password'],
            'dob': data['dob'],
            'gender': data['gender'],
            'email': data['email'],
            'phone_number': data['phone_number'],
            'permanent_address': data['permanent_address'],
        }, {
            'profile_picture': files['profile_picture'],
            'nid': files['nid'],
            'birth_certificate': files['birth_certificate'],
        })

        self.user_id = self.id
        self.institution = data['institution']
        self.degree = data['degree']
        self.student_id = data['student_id']
        self.current_hostel_id = 'null'

    def save_student(self):
        User.save(self)

        command = f'select count(*) from student where user_id like "{self.id}"'
        cursor.execute(command)

        student_count = cursor.fetchall()[0][0]

        if student_count == 0:
            command = (
                    f'insert into student(user_id, institution, degree, student_id) values ( ' +
                    f'"{self.user_id}", ' +
                    f'"{self.institution}", ' +
                    f'"{self.degree}", ' +
                    f'"{self.student_id}" ' +
                    f')'
            )
            cursor.execute(command)
        else:
            command = (
                    f'update student set ' +
                    f'user_id="{self.user_id}", ' +
                    f'institution="{self.institution}", ' +
                    f'degree="{self.degree}", ' +
                    f'student_id="{self.student_id}", ' +
                    f'current_hostel_id="{self.current_hostel_id}" ' +
                    f'where user_id like "{self.user_id}"'
            )
            cursor.execute(command)


class Hostel:

    def __init__(self):
        pass

    def load(self, hostel_id):
        command = f'select * from hostel where hostel_id like "{hostel_id}"'
        cursor.execute(command)

        try:
            hostel = cursor.fetchall()[0]
        except IndexError:
            raise exceptions.HostelNotFoundException

        self.hostel_id = hostel_id
        self.hostel_owner_id = hostel[1]
        self.hostel_name = hostel[2]
        self.thana = hostel[3]
        self.road_number = hostel[4]
        self.house_number = hostel[5]
        self.postal_code = hostel[6]
        self.electricity_bill = hostel[7]
        self.hostel_document = hostel[8]
        self.photo = hostel[9]
        self.verified = hostel[10]
        self.active = hostel[11]

        self.rating = -1

        hostel_ratings = database.load_hostel_ratings()

        avg_by = 0
        self.rating = 0

        for rating in hostel_ratings:
            if rating.hostel_id == self.hostel_id:
                avg_by += 1
                self.rating += rating.rating

        if avg_by == 0:
            self.rating = -1
        else:
            self.rating = round(self.rating/avg_by, 1)

        self.reviews = []

    def create(self, data, files):

        command = f'SELECT COUNT(*) FROM hostel'
        cursor.execute(command)

        self.hostel_id = f'HOS-{str(cursor.fetchall()[0][0] + 1)}'
        self.hostel_owner_id = data['hostel_owner_id']
        self.hostel_name = data['hostel_name']
        self.thana = data['thana']
        self.road_number = data['road_number']
        self.house_number = data['house_number']
        self.postal_code = data['postal_code']
        self.electricity_bill = f'{self.hostel_owner_id}_{self.hostel_id}_electricity_bill.png'
        self.hostel_document = f'{self.hostel_owner_id}_{self.hostel_id}_hostel_document.png'
        self.photo = f'{self.hostel_owner_id}_{self.hostel_id}_photo.png'
        self.verified = 0
        self.active = 0

        self.rating = -1
        self.reviews = []

        self.files = {
            'electricity_bill': Image.open(files['electricity_bill']),
            'hostel_document': Image.open(files['hostel_document']),
            'photo': Image.open(files['photo']),
        }

    def save(self):
        command = f'select count(*) from hostel where hostel_id like "{self.hostel_id}"'
        cursor.execute(command)
        hostel_count = cursor.fetchall()[0][0]

        if hostel_count == 0:

            self.files['electricity_bill'].save(f'{settings.MEDIA_ROOT}/{self.electricity_bill}')
            self.files['hostel_document'].save(f'{settings.MEDIA_ROOT}/{self.hostel_document}')
            self.files['photo'].save(f'{settings.MEDIA_ROOT}/{self.photo}')

            command = f'INSERT INTO hostel VALUES("{self.hostel_id}", "{self.hostel_owner_id}", "{self.hostel_name}", "{self.thana}", "{self.road_number}", "{self.house_number}", "{self.postal_code}", "{self.electricity_bill}", "{self.hostel_document}", "{self.photo}", {self.verified}, {self.active})'
        else:
            command = f'UPDATE hostel SET hostel_name="{self.hostel_name}", thana="{self.thana}", road_number="{self.road_number}", house_number="{self.house_number}", postal_code="{self.postal_code}", electricity_bill="{self.electricity_bill}", hostel_document="{self.hostel_document}", photo="{self.photo}", verified={self.verified}, active={self.active} WHERE hostel_id="{self.hostel_id}"'

        cursor.execute(command)


class Advertise:

    def __init__(self):
        pass

    def load(self, ads_id):
        cmd = f'SELECT * FROM advertise WHERE ads_id like "{ads_id}"'
        cursor.execute(cmd)

        ads = cursor.fetchall()[0]

        self.ads_id = ads_id
        self.hostel_id = ads[1]
        self.room_description = ads[3]
        self.meal_description = ads[4]
        self.facilities_description = ads[5]
        self.preferred_institutions = InstitutionPreference(self.ads_id)
        self.preferred_institutions.load()
        self.rent = ads[6]
        self.rules = ads[7]
        self.conditions = ads[8]
        self.per_room_seats = ads[9]
        self.total_seats = ads[10]
        self.room_photo = ads[11]
        self.approved = ads[12]
        self.active = ads[13]

    def create(self, data, files):
        cmd = f'SELECT COUNT(*) FROM advertise'
        cursor.execute(cmd)

        self.ads_id = f'ADS-{cursor.fetchall()[0][0] + 1}'
        self.hostel_id = data['hostel_id']
        self.room_description = data['room_description']
        self.meal_description = data['meal_description']
        self.facilities_description = data['facilities_description']

        self.preferred_institutions = InstitutionPreference(self.ads_id)
        self.preferred_institutions.add_institution(data['preferred_institutions'])

        self.rent = data['rent']
        self.rules = data['rules']
        self.conditions = data['conditions']
        self.per_room_seats = data['per_room_seats']
        self.total_seats = data['total_seats']
        self.room_photo = f'{self.ads_id}_room_photo.png'
        self.room_photo_2 = f'{self.ads_id}_room_photo_2.png'
        self.room_photo_3 = f'{self.ads_id}_room_photo_3.png'
        self.approved = 0
        self.active = 0

        self.files = {
            'room_photo': Image.open(files['room_photo']),
            'room_photo_2': Image.open(files['room_photo_2']),
            'room_photo_3': Image.open(files['room_photo_3']),
        }

    def save(self):
        cmd = f'SELECT COUNT(*) FROM advertise WHERE ads_id like "{self.ads_id}"'
        cursor.execute(cmd)

        ads_count = cursor.fetchall()[0][0]

        if ads_count == 0:
            self.files['room_photo'].save(f'{settings.MEDIA_ROOT}/{self.room_photo}')
            self.files['room_photo_2'].save(f'{settings.MEDIA_ROOT}/{self.room_photo_2}')
            self.files['room_photo_3'].save(f'{settings.MEDIA_ROOT}/{self.room_photo_3}')

            cmd = f'INSERT INTO advertise(ads_id,hostel_id,room_description,meal_description,facilities_description,rent,rules,conditions,per_room_seats,total_seats,room_photo,approved,active) VALUES("{self.ads_id}","{self.hostel_id}","{self.room_description}","{self.meal_description}","{self.facilities_description}","{self.rent}","{self.rules}","{self.conditions}","{self.per_room_seats}","{self.total_seats}","{self.room_photo}","{self.approved}","{self.active}")'
        else:
            cmd = f'UPDATE advertise SET hostel_id="{self.hostel_id}", room_description="{self.room_description}", meal_description="{self.meal_description}", facilities_description="{self.facilities_description}", rent="{self.rent}", rules="{self.rules}", conditions="{self.conditions}", per_room_seats="{self.per_room_seats}", total_seats="{self.total_seats}", room_photo="{self.room_photo}", approved="{self.approved}", active="{self.active}" WHERE ads_id="{self.ads_id}"'

        print(f'INS: {self.preferred_institutions.institutions}')
        self.preferred_institutions.save()

        cursor.execute(cmd)


class InstitutionPreference:

    def __init__(self, ads_id):
        self.ads_id = ads_id
        self.institutions = []

    def load(self):

        command = f'select institution_name from preferred_institutions where ads_id like "{self.ads_id}"'
        cursor.execute(command)

        self.institutions = [ins[0] for ins in cursor.fetchall()]

    def add_institution(self, institution_names):

        if len(self.institutions) > 0 and self.institutions[0] == '<No-preference>':
            self.institutions = []

        for institution_name in institution_names:
            self.institutions.append(institution_name)

    def save(self):

        command = f'delete from preferred_institutions where ads_id like "{self.ads_id}"'
        cursor.execute(command)

        command = 'insert into preferred_institutions values '
        for i in range(len(self.institutions)):
            command += f'("{self.ads_id}", "{self.institutions[i]}")'
            if i == len(self.institutions) - 1:
                command += ' '
            else:
                command += ', '

        cursor.execute(command)


class AdsFeed:

    def __init__(self, criteria_dict):

        all_ads = database.load_advertisements()

        self.ads_for_feed = []

        for ad in all_ads:
            if ad.approved == 1 and ad.active == 1:
                self.ads_for_feed.append(ad)

        self.criteria = criteria_dict

        self.__apply_location_filter()
        self.__apply_institution_filter()
        self.__apply_budget_filter()

    def __apply_location_filter(self):

        if self.criteria['location'] != 'Any':

            new_ads_for_feed = []

            for ad in self.ads_for_feed:
                i = ad.hostel_id
                hostel = Hostel()
                hostel.load(i)
                if self.criteria['location'] == hostel.thana:
                    new_ads_for_feed.append(ad)

            self.ads_for_feed = new_ads_for_feed

    def __apply_institution_filter(self):

        if self.criteria['institute'] != 'Any':

            new_ads_for_feed = []

            for ad in self.ads_for_feed:
                if self.criteria['institute'] in ad.preferred_institutions.institutions:
                    new_ads_for_feed.append(ad)

            self.ads_for_feed = new_ads_for_feed

    def __apply_budget_filter(self):

        new_ads_for_feed = []

        for ad in self.ads_for_feed:
            if self.criteria['budget']['from'] <= ad.rent <= self.criteria['budget']['to']:
                new_ads_for_feed.append(ad)

        self.ads_for_feed = new_ads_for_feed

    def get_feed_data_for(self, page_number):

        criteria_dict = {
            'thanas': [[thana, 'selected' if thana == self.criteria['location'] else ''] for thana in utilities.all_thana()],
            'institutes': [[institute, 'selected' if institute == self.criteria['institute'] else ''] for institute in utilities.all_institutes()],
            'budget_from': self.criteria['budget']['from'],
            'budget_to': self.criteria['budget']['to'],
            'url_location': self.criteria['location'],
            'url_institute': self.criteria['institute'],
            'url_budget_from': self.criteria['budget']['from'],
            'url_budget_to': self.criteria['budget']['to'],
        }

        criteria_dict['thanas'] = [['Any', '']] + criteria_dict['thanas']
        criteria_dict['institutes'][0] = ['Any', '']

        if page_number == 0:
            page_number = 1

        if len(self.ads_for_feed) == 0:
            return utilities.add_dictionary(criteria_dict, {
                'previous_page': 1,
                'current_page': 1,
                'next_page': 1,
                'pages': [[1, 'active']],
            })

        total_pages = math.ceil(len(self.ads_for_feed)/12)
        number_of_ads_at_last_page = len(self.ads_for_feed) % 12 if len(self.ads_for_feed) % 12 != 0 else 0 if len(self.ads_for_feed) == 0 else 12

        if page_number > total_pages:
            page_number = total_pages

        ads_to_show_start_idx = (page_number - 1) * 12

        ads_to_show_end_idx = ads_to_show_start_idx
        if page_number == total_pages:
            ads_to_show_end_idx += number_of_ads_at_last_page
        else:
            ads_to_show_end_idx += 12

        ads = [[], [], []]

        # [ads_id, hostel_name, rating, thana, ins_pref, rent]

        for i in range(len(self.ads_for_feed))[ads_to_show_start_idx:ads_to_show_end_idx]:

            hostel = Hostel()
            hostel.load(self.ads_for_feed[i].hostel_id)

            ads[math.floor((i-ads_to_show_start_idx)/4)].append([
                self.ads_for_feed[i].ads_id,
                hostel.hostel_name,
                hostel.rating if hostel.rating != -1 else 'UNRATED',
                hostel.thana,
                self.ads_for_feed[i].preferred_institutions.institutions[0],
                self.ads_for_feed[i].rent,
            ])

        pages = [[p, ''] for p in range(total_pages + 1)]
        pages[page_number][1] = 'active'

        return utilities.add_dictionary(criteria_dict, {
            'previous_page': page_number if page_number == 1 else page_number - 1,
            'current_page': page_number,
            'next_page': page_number if page_number == total_pages else page_number + 1,
            'pages': pages[1:],
            'ads': ads,
        })


class Complaint:

    def __init__(self):
        pass

    def load(self, complaint_id):
        command = f'SELECT * FROM complaint_box where complaint_id like "{complaint_id}"'
        cursor.execute(command)

        complaint = cursor.fetchall()[0]

        self.complaint_id = complaint_id
        self.user_id = complaint[1]
        self.subject = complaint[2]
        self.complaint = complaint[3]
        self.photo = complaint[4]
        self.resolved = complaint[5]

    def create(self, data, files):
        command = 'SELECT COUNT(*) FROM complaint_box'
        cursor.execute(command)

        self.complaint_id = f'COM-{cursor.fetchall()[0][0] + 1}'
        self.user_id = data['user_id']
        self.subject = data['subject']
        self.complaint = data['complaint']
        self.photo = f'{self.user_id}_{self.complaint_id}_evidence.png'
        self.resolved = 0

        self.files = {
            'photo': Image.open(files['photo'])
        }

    def save(self):
        command = f'SELECT COUNT(*) FROM complaint_box WHERE complaint_id like "{self.complaint_id}"'
        cursor.execute(command)
        complaint_count = cursor.fetchall()[0][0]

        if complaint_count == 0:
            self.files['photo'].save(f'{settings.MEDIA_ROOT}/{self.photo}')
            command = f'INSERT INTO complaint_box VALUES ("{self.complaint_id}","{self.user_id}","{self.subject}","{self.complaint}","{self.photo}",{self.resolved})'
        else:
            command = f'UPDATE complaint_box SET user_id = "{self.user_id}", subject = "{self.subject}", complaint = "{self.complaint}", photo = "{self.photo}", resolved = {self.resolved} WHERE complaint_id like "{self.complaint_id}"'
        cursor.execute(command)


class Transaction:

    def __init__(self):
        pass

    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass


class ReceivedTransaction(Transaction):

    def __init__(self):
        Transaction.__init__(self)
        pass

    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass


class PaymentRequest(Transaction):

    def __init__(self):
        Transaction.__init__(self)
        pass

    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass


class HostelRating:

    def __init__(self):
        pass

    def load(self, s_u_id, h_id):
        command = f"SELECT * FROM rating_hostel WHERE (student_user_id,hostel_id) = ('{s_u_id}','{h_id}')"
        cursor.execute(command)

        self.student_user_id = s_u_id
        self.hostel_id = h_id
        self.rating = cursor.fetchall()[0][2]

    def create(self, data):
        self.student_user_id = data['student_id']
        self.hostel_id = data['hostel_id']
        self.rating = data['rating']

    def save(self):
        command = f"DELETE FROM rating_hostel WHERE (student_user_id, hostel_id) = ('{self.student_user_id}','{self.hostel_id}')"
        cursor.execute(command)
        command = f"INSERT INTO rating_hostel VALUES ('{self.student_user_id}','{self.hostel_id}',{self.rating})"
        cursor.execute(command)


class StudentRating:

    def __init__(self):
        pass


class HostelReview:

    def __init__(self):
        pass

    def load(self, s_id, h_id):
        command = f"SELECT * FROM review WHERE (hostel_id, student_id) = ('{h_id}','{s_id}')"
        cursor.execute(command)

        self.student_id = s_id
        self.hostel_id = h_id
        self.review = cursor.fetchall()[0][2]

    def create(self,data):
        self.student_id = data['student_id']
        self.hostel_id = data['hostel_id']
        self.review = data['review']

    def save(self):
        command = f"DELETE FROM review WHERE (student_id,hostel_id) = ('{self.student_id}','{self.hostel_id}')"
        cursor.execute(command)
        command = f"INSERT INTO review VALUES ('{self.hostel_id}','{self.student_id}','{self.review}')"
        cursor.execute(command)

