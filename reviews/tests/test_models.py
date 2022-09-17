from django.test import TestCase
from reviews.models import Book, Publisher, Contributor

class TestPublisherModel(TestCase):
    def test_create_publisher(self):
        publisher = Publisher.objects.create(name='Packt', website='www.packt.com',
                                             email='contact@packt.com')
        self.assertIsInstance(publisher, Publisher)
