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
        get_response = c.get('/register/')
        post_response_wrong = c.post('/register/', {
            'username': 'testUser',
            'password1': 'test1234',
            'password2': 'test1234',
        })
        post_response = c.post('/register/', {
            'email': 'test@test.com',
            'password1': 'testPass1234',
            'password2': 'testPass1234',
        })
        self.assertEqual(get_response.status_code, 200)
        self.assertNotEqual(post_response_wrong.status_code, 302)
        self.assertEqual(post_response.status_code, 302)
