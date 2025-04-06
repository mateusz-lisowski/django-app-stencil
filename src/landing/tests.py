from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from .views import landing_view, cached_page_view


class LandingPageTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # Example user creation
        # self.user = User.objects.create_user(
        #     username="jacob", email="jacob@…", password="top_secret"
        # )

    def test_landing_page(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        # request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = landing_view(request)

        # Assert landing page loaded properly
        self.assertEqual(response.status_code, 200)

    def test_cached_page(self):
        request = self.factory.get('/cached/')
        request.user = AnonymousUser()
        response = cached_page_view(request)
        self.assertEqual(response.status_code, 200)
