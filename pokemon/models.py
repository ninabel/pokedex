from django.db import models
from django.conf import settings
from django.urls import reverse


class Deck(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='decks',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def add_card(self, card):
        self.cards.add(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("deck-detail", kwargs={"pk": self.pk})


class Card(models.Model):
    # relates to pokemon name from pokeapi.co
    name = models.CharField(max_length=200)
    deck = models.ForeignKey(Deck, related_name='cards',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pokenames-detail", kwargs={"name": self.name})
