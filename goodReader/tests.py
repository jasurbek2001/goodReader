# from django.test import TestCase
# from django.urls import reverse
#
# from books.models import Book, BookRewiev
# from users.models import CustomUser
#
#
# class HomePageTestCase(TestCase):
#     def test_paginated_list1(self):
#         book_m = Book.objects.create(title="Book", description="description_z", isbn="11111112")
#         user_m = CustomUser.objects.create(
#             username="jasurbek",
#             first_name="Jasurbek",
#             last_name="Suyunov",
#             email="sj@gmail.com"
#         )
#         user_m.set_password("somepassword")
#         user_m.save()
#         review1 = BookRewiev.objects.create(book=book_m, user=user_m, stars_given=3, comment="Very good book")
#         review2 = BookRewiev.objects.create(book=book_m, user=user_m, stars_given=4, comment="Useful book")
#         review3 = BookRewiev.objects.create(book=book_m, user=user_m, stars_given=5, comment="Nice book")
#
#         response = self.client.get(reverse("home_page") + "?page_size=1")
#
#         self.assertContains(response, review3.comment)
#         self.assertContains(response, review2.comment)
#         self.assertNotContains(response, review1.comment)