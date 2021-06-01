from flask_testing import TestCase
from main import app
from flask import current_app, url_for

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# credential = credentials.ApplicationDefault()
# firebase_admin.initialize_app(credential, {'projectId':os.environ['GOOGLE_CLOUD_PROJECT']})

db = firestore.client()

class MainTest(TestCase):
    
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    
    def test_app_exists(self):
        self.assertIsNotNone(current_app)


    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])


    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello'))

    
    def test_hello_login_required(self):
        response = self.client.get(url_for('hello'))
        self.assertEqual(response.status_code, 302)


    def test_hello_post(self):
        #Login
        self.client.post(url_for('auth.login'), data=self.fake_log_form)
        fake_todo_form = {
            'description': 'fake_todo'
        }

        try:
            #Send todo
            response = self.client.post(url_for('hello'), data=fake_todo_form)
            self.assertRedirects(response, url_for('hello'))
        finally:
	    #Remove from db
            db._delete_todo(
                self.fake_log_form['username'], 
                fake_todo_form['description'], 
                caller=self    
            )


    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)
    

    def test_auth_login_get_200(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)


    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    
    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }

        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('index'))

        # response = self.client.get(url_for('hello'))        
        # self.assert200(response)


    def test_auth_signup_get(self):
        response = self.client.get(url_for('auth.signup'))

        self.assert200(response)
    

    def test_auth_signup_post(self):
        try:
            fake_form = {
                'username': 'test_user',
                'password': '123456'
            }
            response = self.client.post(url_for('auth.signup'), data=fake_form)
            self.assertRedirects(response, url_for('hello'))
        finally:
            #Remove added db
            db._delete_user(fake_form['username'], caller=self)