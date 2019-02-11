from django.test import TestCase
from register.forms import AddGradeForm, AddAdvertForm, AddClassAdvertForm, EditAdvertForm, EditClassAdvertForm, \
    AddNoticeForm, AnswerNoticeForm, EditNoticeForm, AddEventForm
from users.forms import UserTeacherRegisterForm, ParentRegisterForm, UserUpdateForm, ProfileUpdateForm, \
    UserParentStudentRegisterForm, StudentRegisterForm
'''
making tests for exercise
'''


class AddGradeFormTest(TestCase):
    def test_category_field_label(self):
        form = AddGradeForm()
        self.assertTrue(form.fields['category'].label is None or form.fields['category'].label == 'kategoria')
        self.assertTrue(form.fields['grade'].label is None or form.fields['grade'].label == 'ocena')


class AddAdvertFormTest(TestCase):
    def test_fields_label(self):
        form = AddAdvertForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'tytuł')
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'treść')

    def test_fields_help_text(self):
        form = AddAdvertForm()
        self.assertEqual(form.fields['title'].help_text, 'Podaj tytuł ogłoszenia')
        self.assertEqual(form.fields['text'].help_text, 'Podaj treść ogłoszenia')


class AddClassAdvertFormTest(TestCase):
    def test_fields_label(self):
        form = AddClassAdvertForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'tytuł')
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'treść')

    def test_fields_help_text(self):
        form = AddClassAdvertForm()
        self.assertEqual(form.fields['title'].help_text, 'Podaj tytuł ogłoszenia klasowego')
        self.assertEqual(form.fields['text'].help_text, 'Podaj treść ogłoszenia klasowego')


class EditAdvertFormTest(TestCase):
    def test_fields_label(self):
        form = EditAdvertForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'tytuł')
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'treść')
        self.assertTrue(form.fields['deleted'].label is None or form.fields['deleted'].label == 'oznaczyć jako usunięte')

    def test_fields_help_text(self):
        form = EditAdvertForm()
        self.assertEqual(form.fields['title'].help_text, 'Zmień tytuł ogłoszenia')
        self.assertEqual(form.fields['text'].help_text, 'Zmień treść ogłoszenia')


class EditClassAdvertFormTest(TestCase):
    def test_fields_label(self):
        form = EditClassAdvertForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'tytuł')
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'treść')
        self.assertTrue(form.fields['deleted'].label is None or form.fields['deleted'].label == 'oznaczyć jako usunięte')

    def test_fields_help_text(self):
        form = EditClassAdvertForm()
        self.assertEqual(form.fields['title'].help_text, 'Zmień tytuł ogłoszenia klasowego')
        self.assertEqual(form.fields['text'].help_text, 'Zmień treść ogłoszenia klasowego')


class AddNoticeFormTest(TestCase):
    def test_fields_label(self):
        form = AddNoticeForm()
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'treść')

    def test_fields_help_text(self):
        form = AddNoticeForm()
        self.assertEqual(form.fields['text'].help_text, 'Podaj treść uwagi')


class AnswerNoticeFormTest(TestCase):
    def test_fields_label(self):
        form = AnswerNoticeForm()
        self.assertTrue(form.fields['accepted'].label is None or form.fields['accepted'].label == 'przyjęte do wiadomości')
        self.assertTrue(form.fields['re_text'].label is None or form.fields['re_text'].label == 'treść')

    def test_fields_help_text(self):
        form = AnswerNoticeForm()
        self.assertEqual(form.fields['re_text'].help_text, 'Podaj treść komentarza')


class EditNoticeFormTest(TestCase):
    def test_fields_label(self):
        form = EditNoticeForm()
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'treść')
        self.assertTrue(form.fields['deleted'].label is None or form.fields['deleted'].label == 'oznaczyć jako usunięte')

    def test_fields_help_text(self):
        form = EditNoticeForm()
        self.assertEqual(form.fields['text'].help_text, 'Zmień treść uwagi')


class AddEventFormTest(TestCase):
    def test_fields_label(self):
        form = AddEventForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'tytuł')
        self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'opis')
        self.assertTrue(form.fields['date_of_event'].label is None or form.fields['date_of_event'].label == 'termin wykonania')

    def test_fields_help_text(self):
        form = AddEventForm()
        self.assertEqual(form.fields['title'].help_text, 'Podaj tytuł wydarzenia')
        self.assertEqual(form.fields['text'].help_text, 'Podaj treść wydarzenia')


class UserTeacherRegisterFormTest(TestCase):
    def test_fields_label(self):
        form = UserTeacherRegisterForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'login')
        self.assertTrue(form.fields['first_name'].label is None or form.fields['first_name'].label == 'imię')
        self.assertTrue(form.fields['last_name'].label is None or form.fields['last_name'].label == 'nazwisko')
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'email')
        self.assertTrue(form.fields['password1'].label is None or form.fields['password1'].label == 'Password')
        self.assertTrue(form.fields['password2'].label is None or form.fields['password2'].label == 'Password confirmation')

    def test_fields_help_text(self):
        form = UserTeacherRegisterForm()
        self.assertEqual(form.fields['username'].help_text, 'Podaj nazwę użytkownika')
        self.assertEqual(form.fields['first_name'].help_text, 'Podaj imię użytkownika')
        self.assertEqual(form.fields['last_name'].help_text, 'Podaj nazwisko użytkownika')
        self.assertEqual(form.fields['email'].help_text, 'Podaj email użytkownika')


class ParentRegisterFormTest(TestCase):
    def test_fields_label(self):
        form = ParentRegisterForm()
        self.assertTrue(form.fields['students'].label is None or form.fields['students'].label == 'dzieci')


class UserUpdateFormTest(TestCase):
    def test_fields_label(self):
        form = UserUpdateForm()
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'email')

    def test_fields_help_text(self):
        form = UserUpdateForm()
        self.assertEqual(form.fields['email'].help_text, 'Podaj nowy email')


class ProfileUpdateFormTest(TestCase):
    def test_fields_label(self):
        form = ProfileUpdateForm()
        self.assertTrue(form.fields['image'].label is None or form.fields['image'].label == 'zdjęcie')
        self.assertTrue(form.fields['phone'].label is None or form.fields['phone'].label == 'telefon')

    def test_fields_help_text(self):
        form = ProfileUpdateForm()
        self.assertEqual(form.fields['image'].help_text, 'Podaj nowe zdjęcie')
        self.assertEqual(form.fields['phone'].help_text, 'Podaj nowy telefon')


class UserParentStudentRegisterFormTest(TestCase):
    def test_fields_label(self):
        form = UserParentStudentRegisterForm()
        self.assertTrue(form.fields['first_name'].label is None or form.fields['first_name'].label == 'imię')
        self.assertTrue(form.fields['last_name'].label is None or form.fields['last_name'].label == 'nazwisko')

    def test_fields_help_text(self):
        form = UserParentStudentRegisterForm()
        self.assertEqual(form.fields['first_name'].help_text, 'Podaj imię użytkownika')
        self.assertEqual(form.fields['last_name'].help_text, 'Podaj nazwisko użytkownika')


class StudentRegisterFormTest(TestCase):
    def test_fields_label(self):
        form = StudentRegisterForm()
        self.assertTrue(form.fields['year_of_birth'].label is None or form.fields['year_of_birth'].label == 'rok urodzenia')
        self.assertTrue(form.fields['classes'].label is None or form.fields['classes'].label == 'klasa')

    def test_fields_help_text(self):
        form = StudentRegisterForm()
        self.assertEqual(form.fields['year_of_birth'].help_text, 'Podaj rok urodzenia użytkownika')
