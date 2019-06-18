import unittest
import json
from run import create_app
from Model import db


class UsersTest(unittest.TestCase):
    """
    Users Test Case
    """

    def setUp(self):
        """
        Test Setup
        """
        self.app = create_app("config")
        self.client = self.app.test_client
        self.user = {
            'user_name': 'user_test',
            'password': 'password'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_login(self):
        """ User Login Tests """
        res = self.client().post(
            '/api/registration',
            headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/api/login',
            headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('access_token'))
        self.assertEqual(res.status_code, 200)

    def test_user_login_invalid_password(self):
        """ User Login Tests with invalid credentials """
        user1 = {
            'password': 'password1',
            'user_name': 'user_test',
        }
        res = self.client().post(
            '/api/registration',
            headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/api/login',
            headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('access_token'))
        self.assertEqual(json_data.get('message'), 'Wrong credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_login_invalid_user_name(self):
        """ User Login Tests with invalid credentials """
        user1 = {
            'password': 'password',
            'user_name': 'test_user',
        }
        res = self.client().post(
            '/api/registration',
            headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/api/login',
            headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('access_token'))
        self.assertEqual(json_data.get('message'),
            'User {} doesn\'t  exist'.format(user1.get('user_name')))
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
