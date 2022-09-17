from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r'books', api_views.BookViewSet)
router.register(r'reviews', api_views.ReviewViewSet)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/login', api_views.Login.as_view(), name='login'),
    path('api/', include( (router.urls, 'api') )),
    path('', views.welcome_view),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:book_pk>/reviews/new/', views.review_edit, name="review_create"),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name="review_edit"),
    path('books/<int:pk>/media/', views.book_media, name='book_media'),
    path('book-search', views.book_search, name='book_search'),
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publishers/new/', views.publisher_edit, name='publisher_create'),
    # path('api/first_api_view/', api_views.first_api_view),
 #   path('api/all_books/', api_views.AllBooks.as_view(), name='all_books'),
 #   path('api/contributors/', api_views.ContributorView.as_view(), name='contributors'),
]

pass
