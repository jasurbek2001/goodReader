from django.urls import reverse
from django.test import TestCase
from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")


    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="description1", isbn="11111111")
        book2 = Book.objects.create(title="Book2", description="description2", isbn="22222222")
        book3 = Book.objects.create(title="Book2", description="description2", isbn="22222222")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1,book2]:
            self.assertContains(response, book.title)
        self.assertContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)


    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="description1", isbn="11111111")
        response = self.client.get(reverse("books:detail", kwargs={"id":book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)


    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="description1", isbn="11111111")
        book2 = Book.objects.create(title="English", description="description2", isbn="22222222")
        book3 = Book.objects.create(title="Math", description="description2", isbn="22222222")

        response = self.client.get(reverse("books:list") + "?q=sport")
        self.assertContains(response,book1.title)
        self.assertNotContains(response,book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=english")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=math")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Sport", description="description1", isbn="11111111")
        user = CustomUser.objects.create(
            username="jasurbek",
            first_name="Jasurbek",
            last_name="Suyunov",
            email="sj@gmail.com"
        )
        user.set_password("somepassword")
        user.save()
        self.client.login(username="jasurbek", password="somepassword")

        self.client.post(reverse("books:reviews", kwargs={"id":book.id}), data={
            "stars_given":4,
            "comment":"Nice book"
        })
        book_reviews = book.bookrewiev_set.all()

        self.assertEqual(book_reviews.count(),1)
        self.assertEqual(book_reviews[0].stars_given,4)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)