import io
from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model

# Get the User model configured in your settings
User = get_user_model()

# The path to the 'config' object used within your command file
CONFIG_PATH = 'cli.management.commands.setup_admin.config'


class SetupAdminCommandTest(TestCase):

    def setUp(self):
        """Optional: Setup common test data if needed, though often not necessary for command tests"""
        pass

    # Helper function to mock decouple.config behavior
    def _mock_config(self, mock_config_object, env_vars):
        """
        Configures the mock object for decouple.config.

        Args:
            mock_config_object: The mock object passed by @patch.
            env_vars (dict): A dictionary simulating environment variables.
        """
        def config_side_effect(key, default=None, cast=None):
            val = env_vars.get(key, default)
            # Simulate decouple's casting behavior
            if cast and val is not None:
                try:
                    return cast(val)
                except ValueError:
                    return default  # Or handle error as decouple would
            return val
        mock_config_object.side_effect = config_side_effect

    @patch(CONFIG_PATH)  # Patch the config object used in the command
    def test_missing_env_vars(self, mock_config):
        """
        Test command execution when environment variables are missing.
        """
        # Simulate missing DJANGO_SUPERUSER_PASSWORD
        env_vars = {
            'DJANGO_SUPERUSER_USERNAME': 'testadmin',
            'DJANGO_SUPERUSER_EMAIL': 'test@example.com',
            # 'DJANGO_SUPERUSER_PASSWORD': 'password123' # Missing!
        }
        self._mock_config(mock_config, env_vars)

        # Capture stdout
        out = io.StringIO()
        call_command('setup_admin', stdout=out)

        # Assertions
        # Check for the error message
        self.assertIn("Missing environment variables", out.getvalue())
        # Ensure the specific missing var is mentioned
        self.assertIn("DJANGO_SUPERUSER_PASSWORD", out.getvalue())
        # Ensure no user was created
        self.assertFalse(User.objects.filter(username='testadmin').exists())

    @patch(CONFIG_PATH)
    def test_user_does_not_exist(self, mock_config):
        """
        Test command successfully creates a superuser when it doesn't exist.
        """
        # Simulate all required environment variables present
        env_vars = {
            'DJANGO_SUPERUSER_USERNAME': 'newadmin',
            'DJANGO_SUPERUSER_EMAIL': 'newadmin@example.com',
            'DJANGO_SUPERUSER_PASSWORD': 'password123'
        }
        self._mock_config(mock_config, env_vars)

        # Capture stdout
        out = io.StringIO()
        call_command('setup_admin', stdout=out)

        # Assertions
        self.assertIn("Creating superuser: newadmin", out.getvalue())
        self.assertIn("Superuser created successfully.", out.getvalue())
        self.assertTrue(User.objects.filter(username='newadmin').exists())  # Check user exists

        # Verify user details
        user = User.objects.get(username='newadmin')
        self.assertEqual(user.email, 'newadmin@example.com')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)  # create_superuser usually sets is_staff too
        self.assertTrue(user.check_password('password123'))  # Verify password

    @patch(CONFIG_PATH)
    def test_user_already_exists(self, mock_config):
        """
        Test command skips creation if the superuser already exists.
        """
        # 1. Pre-create a user with the same username
        existing_username = 'existingadmin'
        existing_email = 'original@example.com'
        existing_password = 'oldpassword'
        User.objects.create_user(username=existing_username, email=existing_email, password=existing_password)
        # Ensure it's just a regular user initially, or make it a superuser if desired
        # user = User.objects.get(username=existing_username)
        # user.is_superuser = True
        # user.save()

        # 2. Simulate environment variables pointing to the existing username
        env_vars = {
            'DJANGO_SUPERUSER_USERNAME': existing_username,  # Same username
            'DJANGO_SUPERUSER_EMAIL': 'new@example.com',  # Different email/password
            'DJANGO_SUPERUSER_PASSWORD': 'newpassword123'
        }
        self._mock_config(mock_config, env_vars)

        # 3. Capture stdout and call the command
        out = io.StringIO()
        call_command('setup_admin', stdout=out)

        # 4. Assertions
        self.assertIn(f"Superuser {existing_username} already exists. Skipping.", out.getvalue())
        self.assertNotIn("Creating superuser", out.getvalue())  # Ensure a creation message isn't present

        # Verify only one user exists with that username
        self.assertEqual(User.objects.filter(username=existing_username).count(), 1)

        # Verify the existing user was not modified
        user = User.objects.get(username=existing_username)
        self.assertEqual(user.email, existing_email)  # Should still have the original email
        self.assertTrue(user.check_password(existing_password))  # Should still have the original password
        # self.assertTrue(user.is_superuser) # Check superuser status if it was set initially
