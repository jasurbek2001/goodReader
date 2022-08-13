from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data = {
                "username":"jasurbek001",
                "first_name":"Jasurbek",
                "last_name":"Suyunov",
                "email":"js@gmail.com",
                "password":"somepassword"
            }
        )
        user = CustomUser.objects.get(username="jasurbek001")

        self.assertEqual(user.first_name,"Jasurbek")
        self.assertEqual(user.last_name, "Suyunov")
        self.assertEqual(user.email,"js@gmail.com")
        self.assertNotEqual(user.password,"somepassword")
        self.assertTrue(user.check_password("somepassword"))


    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data = {
                "first_name":"Jasurbek",
                "email":"js@gmail.com"
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response,"form","username","This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")


    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "jasurbek001",
                "first_name": "Jasurbek",
                "last_name": "Suyunov",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")


    def test_unique_username(self):
        user = CustomUser.objects.create(username="jasurbek",first_name="Jasurbek")
        user.set_password("somepassword")
        user.save()
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "jasurbek",
                "first_name": "Jasurbek",
                "last_name": "Suyunov",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count,1)
        self.assertFormError(response,"form","username","A user with that username already exists.")



class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="jasurbek", first_name="Jasurbek")
        self.db_user.set_password("somepassword")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username":"jasurbek",
                "password":"somepassword"
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credintial(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong_username",
                "password": "somepassword"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


        self.client.post(
            reverse("users:login"),
            data={
                "username": "jasurbek",
                "password": "wrong_password"
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username = 'jasurbek', password = "somepassword")
        self.client.get(reverse("users:logout"))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(username="jasurbek", first_name="Jasurbek",last_name="Suyunov",email="sj@gmail.com")
        user.set_password("somepassword")
        user.save()
        self.client.login(username="jasurbek",password="somepassword")
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(username="jasurbek", first_name="Jasurbek", last_name="Suyunov", email="sj@gmail.com")
        user.set_password("somepassword")
        user.save()
        self.client.login(username="jasurbek", password="somepassword")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username":"jasurbek",
                "first_name":"Jasurbek",
                "last_name":"Suyunov_one",
                "email":"jasurbek@gmail.com"
            }
        )
        # user = User.objects.get(pk = user.pk)
        user.refresh_from_db()

        self.assertEqual(user.last_name,"Suyunov_one")
        self.assertEqual(user.email, "jasurbek@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))