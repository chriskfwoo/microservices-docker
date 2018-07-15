import json
import unittest
from project.tests.base import BaseTestCase
from project import db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """ Tests for Users Service """


    def test_users(self):
        """ Ensure the /ping route behaves correctly """

        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    
    def test_add_user(self):
        """ Ensure a new user can be added to the database """

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'chris',
                    'email': 'chriswoo@gmail.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('chriswoo@gmail.com', data['message'])
            self.assertIn('succes', data['status'])


    def test_add_user_invalid_json(self):
        """ Ensure error is thrown if the JSON object is empty """

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    
    def test_add_user_invalid_json_keys(self):
        """ Ensure error is thrown if the JSON object does not have a username key """

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'chriswoo@gmail.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    
    def test_add_user_duplicate_email(self):
        """ Ensure error is thrown if the email already exists """

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'chriswoo',
                    'email': 'chriswoo@gmail.com'
                }),
                content_type='application/json',
            )

            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'chriswoo',
                    'email': 'chriswoo@gmail.com'
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])


    def test_single_user(self):
        """ Ensure get single user behaves correctly """

        user = add_user('chriswoo', 'chriswoo@gmail.com')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('chriswoo', data['data']['username'])
            self.assertIn('chriswoo@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    
    def test_single_user_no_id(self):
        """ Ensure error is thrown if an id is not provided """

        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    
    def test_single_user_incorrect_id(self):
        """ Ensure error is thrown if the id does not exist """

        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    
    def test_all_users(self):
        """ Ensure get all users behaves correctly """

        add_user('chriswoo', 'chriswoo@gmail.com')
        add_user('johndoe', 'johndoe@gmail.com')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('chriswoo', data['data']['users'][0]['username'])
            self.assertIn('chriswoo@gmail.com', data['data']['users'][0]['email'])
            self.assertIn('johndoe', data['data']['users'][1]['username'])
            self.assertIn('johndoe@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    
    def test_main_no_users(self):
        """ Ensure the main route behaves correctly when no users have been added to the database """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    
    def test_main_with_users(self):
        """ Ensure the main route behaves correctly when users have been added to the database """

        add_user('chriswoo', 'chriswoo@gmail.com')
        add_user('johndoe', 'johndoe@gmail.com')

        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'chriswoo', response.data)
            self.assertIn(b'johndoe', response.data)


    def test_main_add_user(self):
        """ Ensure a new user can be added to the database """

        add_user('chriswoo', 'chriswoo@gmail.com')
        add_user('johndoe', 'johndoe@gmail.com')

        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='chriswoo', email='chriswoo@gmail.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'chriswoo', response.data)


if __name__ == '__main__':
    unittest.main()