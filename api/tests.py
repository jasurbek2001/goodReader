from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookRewiev
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="jasurbek", first_name="Jasurbek")
        self.user.set_password("somepassword")
        self.user.save()
        self.client.login(username = "jasurbek", password = "somepassword")

    def test_book_review_detail(self):
        book = Book.objects.create(title="Book", description="description_z", isbn="11111112")
        br = BookRewiev.objects.create(book=book, user=self.user, stars_given=3, comment="Very good book")

        response = self.client.get(reverse('api:review-detail', kwargs={'id':br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'],br.id)
        self.assertEqual(response.data['stars_given'], 3)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], br.book_id)
        self.assertEqual(response.data['book']['title'], 'Book')
        self.assertEqual(response.data['book']['description'], 'description_z')
        self.assertEqual(response.data['book']['isbn'], '11111112')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], 'Jasurbek')
        self.assertEqual(response.data['user']['username'], 'jasurbek')

    def test_delete_review(self):
        book = Book.objects.create(title="Book", description="description_z", isbn="11111112")
        br = BookRewiev.objects.create(book=book, user=self.user, stars_given=3, comment="Very good book")

        response = self.client.delete(reverse('api:review-detail', kwargs={'id':br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookRewiev.objects.filter(id = br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="Book", description="description_z", isbn="11111112")
        br = BookRewiev.objects.create(book=book, user=self.user, stars_given=3, comment="Very good book")

        response = self.client.patch(reverse('api:review-detail', kwargs={'id':br.id}), data={'stars_given':4})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)

    # def test_put_review(self):
    #     book = Book.objects.create(title="Book", description="description_z", isbn="11111112")
    #     br = BookRewiev.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
    #
    #     response = self.client.put(reverse('api:review-detail', kwargs={'id': br.id}),data={'user_id':self.user.id,'book_id':book.id,'stars_given': 5, 'comment':'nice book',})
    #     br.refresh_from_db()
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(br.stars_given, 4)
    #     self.assertEqual(br.comment, 'nice book')
    #
    # def test_create_review(self):
    #     book = Book.objects.create(title="Book", description="description_z", isbn="11111112")
    #     data = {
    #         "stars_given":2,
    #         "comment":"bad book",
    #         "user_id":self.user.id,
    #         "book_id":book.id
    #      }
    #     response = self.client.post(reverse('api:review-list'), data=data)
    #     br = BookRewiev.objects.get(book = book)
    #
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(br.stars_given, 2)
    #     self.assertEqual(br.comment, "bad book")



    def test_book_review_list(self):
        user_two = CustomUser.objects.create(username="somebody", first_name="Somebody")
        book = Book.objects.create(title="Book", description="description_z", isbn="11111112")
        br = BookRewiev.objects.create(book=book, user=self.user, stars_given=3, comment="Very good book")
        br_two = BookRewiev.objects.create(book=book, user=user_two, stars_given=4, comment="best book")

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][1]['id'], br_two.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br_two.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br_two.comment)
        self.assertEqual(response.data['results'][0]['id'], br.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br.comment)