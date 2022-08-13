from django import forms
from books.models import BookRewiev


class BookReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = BookRewiev
        fields = ('stars_given','comment')