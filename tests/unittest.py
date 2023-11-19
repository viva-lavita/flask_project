# import unittest
# from flask import Flask
# from flask_login import current_user
# import flask_testing
# from config import app, db
# from models import Note


# class TestNotes(flask_testing.TestCase):
#     def create_app(self):
#         app.config['TESTING'] = True
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#         return app

#     def setUp(self):
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()

#     def test_notes_authenticated_user(self):
#         with self.client:
#             # Create a user and login
#             self.client.post('/login', data=dict(
#                 username='testuser',
#                 password='testpassword'
#             ), follow_redirects=True)

#             # Create some notes for the authenticated user
#             note1 = Note(user_id=current_user.id, content='note1')
#             note2 = Note(user_id=current_user.id, content='note2')
#             db.session.add_all([note1, note2])
#             db.session.commit()

#             # Send a GET request to '/notes'
#             response = self.client.get('/notes')

#             # Assert that the response status code is 200
#             self.assertEqual(response.status_code, 200)

#             # Assert that the rendered template is 'notes.html'
#             self.assert_template_used('notes.html')

#             # Assert that the 'notes' variable in the template contains the created notes
#             self.assertIn(note1, response.context['notes'])
#             self.assertIn(note2, response.context['notes'])

#     def test_notes_unauthenticated_user(self):
#         with self.client:
#             # Send a GET request to '/notes'
#             response = self.client.get('/notes')

#             # Assert that the response status code is 200
#             self.assertEqual(response.status_code, 200)

#             # Assert that the rendered template is 'notes.html'
#             self.assert_template_used('notes.html')

#             # Assert that the 'notes' variable in the template is an empty list
#             self.assertEqual(response.context['notes'], [])


# if __name__ == '__main__':
#     unittest.main()