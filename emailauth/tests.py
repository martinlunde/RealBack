from django.test import Client, TestCase
from emailauth import forms

c = Client()


class FormTests(TestCase):

    def test_creation_form(self):
        form_data = {'email': 'test@test.com', 'password1': 'test1234', 'password2': 'test1234'}
        form = forms.UserCreationForm(form_data)

        # Testing if form is valid, and that the fields are working.
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {'email': 'test@test.com', 'password1': 'test1234', 'password2': 'test1234'}
        form = forms.UserCreationForm(form_data)

        # Testing if form is valid, and that the fields are working.
        self.assertTrue(form.is_valid())

        user = form.save()
        # Testing if save function is returning properly
        self.assertEqual(str(user), 'test@test.com')

    def test_not_identically_passwords(self):
        form_data = {'email': 'test@test.com', 'password1': '1234test', 'password2': 'test1234'}
        form = forms.UserCreationForm(form_data)

        # Testing if form is invalid when passwords are not matching.
        self.assertFalse(form.is_valid())

    def test_register_by_post(self):
        # Testing register trough post-request
        self.assertEqual(c.post('/register/', {'username': 'test@test.com',
                                               'password1': 'test1234',
                                               'password2': 'test1234'}
                                ).status_code, 200)
