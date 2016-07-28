from django.test import TestCase
from .models import User


# Create your tests here.
class CustomUserTest(TestCase):

    def test_manager_create(self):
        user = User.objects._create_user(None, 'test@test.com', 'password', False, False)
        self.assertIsNotNone(user)

        with self.assertRaises(ValueError):
            user = User.objects._create_user(None, None, 'password', False, False)

