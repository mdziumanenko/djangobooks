from django.db import models
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PublisherForm, SearchForm, ReviewForm, BookMediaForm
from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from django.contrib import messages
from django.utils.timezone import now
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied

def is_staff_user(user):
    return user.is_staff

def welcome_view(request):
    return render(request, "base.html")

def book_search(request):
    "In solutions other implementation of this function"
    search_text = request.GET.get("search", "")
    search_history = request.session.get('search_history', [])
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data['search']:
        # DEBUG: print cleaned data items
        #for name, value in form.cleaned_data.items():
        #    print("{}: ({}) {}".format(name, type(value), value))

        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"

        if  search_in == "title":
            books = Book.objects.filter(title__icontains = search)
        else:   # by contributor
            books = Book.objects.filter(models.Q(contributors__first_names__icontains = search) |
                                        models.Q(contributors__last_names__icontains = search))

        if request.user.is_authenticated:
            search_history.append([search_in, search])
            request.session['search_history'] = search_history
    elif search_history:
        initial = dict(search=search_text, search_in=search_history[-1][0])
        form = SearchForm(initial = initial)

    return render(request, "reviews/search-results.html", {"form": form, 'search_text': search_text, 'books': books})

def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0

        book_list.append({'book': book, 'book_rating': book_rating, 'number_of_reviews': number_of_reviews})

    context = {  'book_list': book_list   }
    return render(request, "reviews/book_list.html", context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = { "book": book, "book_rating": book_rating, "reviews": reviews }
    else:
        context = { "book": book, "book_rating": None, "reviews": None }

    if request.user.is_authenticated:       # store last 10 viewed books in session
        max_viewed_books_length = 10
        viewed_books = request.session.get('viewed_books', [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))

        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session['viewed_books'] = viewed_books
    return render(request, "reviews/book_detail.html", context)


def is_member_of_bookshop_staff(user):
    return user.groups.filter(name='bookshop_staff').exists()

@permission_required('reviews.add_publisher')
#@user_passes_test(is_staff_user)
@login_required
def publisher_edit(request, pk=None):
    publisher = None
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
        if publisher is None:
            messages.success(request, "Publisher \"{}\" was created.".format(updated_publisher))
        else:
            messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))

        return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "reviews/instance-form.html",
                  {"form": form, "instance": publisher, "model_type": "Publisher"})

@login_required
def review_edit(request, book_pk, review_pk = None):
    book = get_object_or_404(Book, pk=book_pk)
    review = None
    if review_pk is not None:
        review = get_object_or_404(Review, pk=review_pk, book__pk=book_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.book = book
            updated_review.date_edited = now()
            updated_review.save()
        if review is None:
            messages.success(request, f"Review \"{updated_review}\" was created.")
        else:
            messages.success(request, f"Review \"{updated_review}\" was updated.")

        return redirect("review_edit", book_pk, updated_review.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/instance-form.html",
                  {"form": form, "instance": review, "model_type": "Review",
                   "related_model_type": "Book",
                   "related_instance": book})

@login_required
def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)       # тут не мстворюємо книгу, лише редагуємо
    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)

            cover = form.cleaned_data.get("cover")
            if cover:
                image = Image.open(cover)
                image.thumbnail((300,300))
                image_data = BytesIO()
                image.save(fp=image_data, format=cover.image.format)
                image_file = ImageFile(image_data)
                book.cover.save(cover.name, image_file)

            sample_file = form.cleaned_data.get("cover") or None
            # save cover and sample fields
            book.save()
            messages.success(request, f'Book {book} was updated')
            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)

    return render(request, "reviews/instance-form.html",
            {"form":form, "instance":book,
             "model_type": "Book" })

def react_example(request):
    return render(request, "react-example.html", {"name": "Ben", "target": 5})