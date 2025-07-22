from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from pokemon.models import Deck, Card

import requests

# functions to get data from PokeApi

POKEAPI_URL = 'https://pokeapi.co/api/v2/pokemon/'
LIMIT = 20

def get_pokemons_list(page: int = 1):
    # get pokemons' names from PokeApi
    response = requests.get(POKEAPI_URL, params={"offset": (page-1)*LIMIT, "limit":LIMIT})
    if not response.ok:
        raise Http404("PokeAPI doesn't answer.")
    return response.json()

def get_pokemon(name: str):
    # get pokemon's stats from PokeApi
    response = requests.get(f'{POKEAPI_URL}/{name}')
    if not response.ok:
        raise Http404(f"Pokemon {name} wasn't found.")
    return response.json()



# Create your views here.
def main(request):
    # pokemon list
    try:
        page = int(request.GET.get("page"))
    except TypeError:
        page = 1
    poke_list = get_pokemons_list(page)
    
    return render(request, 'pokemon/main.html', 
                  {"poke_list": poke_list, "title": "Pokemon list", "page": page})

def card(request, name: str):
    # pokemon details
    return render (request, 'pokemon/card.html',
                   {"pokemon": get_pokemon(name), "title": "Pokemon"})

def compare(request, left_name: str, right_name: str):
    # compare two pokemons
    return render (request, 'pokemon/compare.html',
                   {
                    "left": get_pokemon(left_name),
                    "right": get_pokemon(right_name),
                    "title": "Compare pokemons",
                    })

def compare_redirect(request, left_name: str):
    right_name = request.GET.get("right_name")
    if right_name:
        return redirect("compare", left_name=left_name, right_name=right_name)
    return redirect("card", name=left_name)

def add(request, card: str, deck_id: int = 0):
    # add card to deck
    from datetime import datetime

    if deck_id == 0: # new deck
        deck = Deck.objects.create(title=f"Deck {datetime.now()}",
                                   owner=request.user)
    else:
        deck = get_object_or_404(Deck, pk=deck_id)
    if deck.owner != request.user:
        raise Http404("You can not edit this deck.")
    card = Card.objects.create(name=card, deck=deck)
    return redirect("deck", id=deck.pk)

def deck(request, id: int):
    # show deck, only for its owner
    deck = get_object_or_404(Deck, pk=id)
    return render (request, 'pokemon/deck.html',
                   {"deck": deck, "title": deck.title})

def remove(request, deck_id: int, card_id: int):
    # remove card from deck
    deck = get_object_or_404(Deck, pk=deck_id)
    if deck.owner != request.user:
        raise Http404("You can not edit this deck.")
    try:
        deck.cards.get(pk=card_id).delete()
    except Http404:
        pass
    return redirect("deck", id=deck.pk)