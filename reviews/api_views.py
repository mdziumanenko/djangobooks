from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Contributor, Review
from .serializers import BookSerializer, ReviewSerializer, ContributorSerializer
from rest_framework import generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

class Login(APIView):
    def post(self, request):
        user = authenticate(username=request.data.get("username"),password=request.data.get("password"))
        if not user:
            return Response({'error': 'Credentials are incorrect or user doesn’t exist'}, 						status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = []
    permission_classes = []
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.order_by('-date_created')
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = []


# ######### OLD non veiwset code
class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ContributorView(generics.ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

# @api_view()
# def all_books(request):
#     books = Book.objects.all()
#     book_serializer = BookSerializer(books, many=True)
#     return Response(book_serializer.data)

# @api_view()
# def first_api_view(request):
#     num_books = Book.objects.count()
#     return Response({"num_books": num_books})