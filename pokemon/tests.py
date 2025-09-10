import logging
import re
from django.test import TestCase
from unittest.mock import patch

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client


class PokemonViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='ash', password='pikachu123')

    def test_main_page_accessible(self):
        # Test main page respone
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_main_page_shows_pokemon_list(self):
        """
        The main page should show a header and a list of Pokémon names
        with links to their card pages.
        """
        response = self.client.get(reverse('main'))
        self.assertContains(response, "Pokemon list")  # Check for the header

        # The default API returns at least 20 pokemons,
        # check for a few known ones and their links
        for name in ["bulbasaur", "charmander", "squirtle"]:
            self.assertContains(response, name)
            self.assertContains(response, reverse('card', args=[name]))

    def test_pokemon_detail_page(self):
        # Assuming a Pokemon model with a factory or fixture

        response = self.client.get(reverse('card', args=["bulbasaur"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "bulbasaur")

    def test_pokemon_detail_page_stats_exist(self):
        """
        Check that the pokemon detail page contains stats with numbers:
        hp, attack, defense, special-attack, special-defense, speed
        """
        response = self.client.get(reverse('card', args=["bulbasaur"]))
        self.assertEqual(response.status_code, 200)

        stats = [
            "hp",
            "attack",
            "defense",
            "special-attack",
            "special-defense",
            "speed"
        ]
        content = response.content.decode()
        for stat in stats:
            # Look for e.g. "hp: 45" or "special-attack: 65"
            pattern = rf"{stat}:\s*<b>\d+</b>"
            self.assertRegex(
                content, pattern,
                msg=f"Stat '{stat}' with number not found in page")

    def test_compare_page_shows_stats_fields(self):
        """
        The compare page should show the stats fields for both pokemons.
        """
        left = "bulbasaur"
        right = "charmander"
        url = reverse('compare', args=[left, right])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        stats = [
            "hp",
            "attack",
            "defense",
            "special-attack",
            "special-defense",
            "speed"
        ]
        for stat in stats:
            self.assertIn(stat, response.content.decode())

    def test_card_page_shows_stats_fields(self):
        """
        The card page should show the stats fields for the pokemon.
        """
        name = "bulbasaur"
        url = reverse('card', args=[name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        stats = [
            "hp",
            "attack",
            "defense",
            "special-attack",
            "special-defense",
            "speed"
        ]
        for stat in stats:
            self.assertIn(stat, response.content.decode())

    def test_compare_page(self):
        """
        Test compare page for two pokemons
        """
        p1 = "bulbasaur"
        p2 = "charmander"
        url = reverse('compare', args=[p1, p2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compare pokemons")
        self.assertContains(response, p1)
        self.assertContains(response, p2)

    def test_card_page_compare_form(self):
        """
        The card page should contain a form
        to compare this pokemon with another.
        """
        name = "bulbasaur"
        url = reverse('card', args=[name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check for a form element
        self.assertIn("<form", response.content.decode().lower())
        # Check for an input for right_name
        self.assertIn("name=\"right_name\"", response.content.decode().lower())
        # Check that the form action points
        # to the compare_redirect URL for this pokemon
        compare_redirect_url = reverse('compare_redirect', args=[name])
        self.assertIn(compare_redirect_url, response.content.decode())
        # Check that the form contains a name attribute for right_name
        self.assertIn('name="right_name"', response.content.decode().lower())
        # Optionally, check that the input is empty (value="")

    def test_card_compare_post_form(self):
        """
        The test checks form redirection to compare page
        """
        left = "bulbasaur"
        right = "pikachu"
        url = reverse('compare_redirect', args=[left])
        response = self.client.get(url, {"right_name": right})
        redirect = reverse("compare", args=[left, right])
        # Check that the response is a redirect to the compare page
        self.assertRedirects(response, expected_url=redirect)

    def test_add_link_visible_only_for_authorized_user(self):
        """
        The 'Add' link should appear on the card page only
        for an authenticated user.
        """
        name = "bulbasaur"
        url = reverse('card', args=[name])

        # Not logged in: should not see "Add" link
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Add to deck', response.content.decode())

        # Log in as a user
        self.client.login(username='ash', password='pikachu123')

        # Now should see "Add" link
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add to', response.content.decode())

    def test_add_and_remove_pokemon_to_deck(self):
        """
        This test checks that a user can add a pokemon to a deck
        and then remove it.
        It assumes the user 'ash' exists and is authenticated,
        and that the add view creates a new deck
        if no deck is specified.
        """
        name = "bulbasaur"
        self.client.login(username='ash', password='pikachu123')
        add_url = reverse('add', args=[name])
        response = self.client.post(add_url)
        self.assertEqual(response.status_code, 302)  # Redirect after add

        deck_url = response.url
        response = self.client.get(deck_url)
        self.assertContains(response, name)

        # Find the remove link in the response content
        # and extract deck.id and pokemon.id
        content = response.content.decode()
        match = re.search(r'/remove/(\d+)/(\d+)', content)
        self.assertIsNotNone(
            match,
            "Remove link with deck and pokemon ids not found in response")
        deck_id = int(match.group(1))
        pokemon_id = int(match.group(2))

        remove_url = reverse('remove', args=[deck_id, pokemon_id])
        response = self.client.post(remove_url)
        self.assertEqual(response.status_code, 302)  # Redirect after remove

        response = self.client.get(deck_url)
        self.assertNotContains(response, name)

    def test_deck_visibility_only_for_owner(self):
        """
        Test that a created deck is visible only to the user who created it.
        """
        name = "bulbasaur"
        # Log in as user 'ash' and add a pokemon to create a new deck
        self.client.login(username='ash', password='pikachu123')
        add_url = reverse('add', args=[name])
        response = self.client.post(add_url)
        self.assertEqual(response.status_code, 302)
        deck_url = response.url

        # 'ash' should see the deck in their deck list
        response = self.client.get(deck_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, name)

        # Log out and create a new user 'misty'
        self.client.logout()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='misty').exists():
            User.objects.create_user(username='misty', password='staryu123')

        self.client.login(username='misty', password='staryu123')
        # 'misty' should not see the deck created by 'ash'
        # don't re-raise PermissionDenied
        self.client.raise_request_exception = False
        logger = logging.getLogger("django.security.PermissionDenied")
        old_level = logger.level
        logger.setLevel(logging.CRITICAL)
        with patch("django.core.handlers.exception.log_response"):
            response = self.client.get(deck_url)
            self.assertEqual(response.status_code, 403)
        logger.setLevel(old_level)
