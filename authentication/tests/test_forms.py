from django.test import SimpleTestCase
from authentication.forms import ProfileUpdateForm


class TestForms(SimpleTestCase):
    """
    Unittest case for forms in authentication app.
    """
    def test_profile_update_form_valid_data(self):
        """
        Testing the profile update form with valid bio text data.
        """
        form = ProfileUpdateForm(data={
            'bio': 'This is your new bio.'
        })
        self.assertTrue(form.is_valid())

    # Testing bio with invalid data (201 characters)
    def test_profile_update_form_invalid_data(self):
        """
        Testing the profile update form with invalid bio text data.
        """
        form = ProfileUpdateForm(data={
            'bio': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr,'
            ' sed diam nonumy eirmod tempor invidunt ut labore et dolore magna'
            ' aliquyam erat, sed diam voluptua. At vero eos et accusam et'
            ' justo duo dolores e'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
