from django import template
from reviews.models import Review

register = template.Library()

@register.inclusion_tag('book_list.html')
def book_list(username):
    '''Render the list of boooks read by user.
        :param: str username The Username for whom the books should be fetched
    '''
    reviews = Review.objects.filter(creator__username__contains=username)
    book_list = [review.book.title for review in reviews]
    return { 'books_read': book_list }