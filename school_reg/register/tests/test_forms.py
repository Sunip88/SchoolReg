from django.test import TestCase
from register.forms import AddGradeForm, AddAdvertForm, AddClassAdvertForm, EditAdvertForm, EditClassAdvertForm, \
    AddNoticeForm, AnswerNoticeForm, EditNoticeForm, AddEventForm


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
