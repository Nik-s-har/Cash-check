from django.test import TestCase
from django.urls import resolve
# from ststistic_output.views import month_statistics

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, month_statistics)