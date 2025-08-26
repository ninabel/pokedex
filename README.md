#  Pokedex — Django Demo App

A demo Django web application that integrates with the [PokéAPI](https://pokeapi.co) to display Pokémon data. Browse Pokémon, see their details, and explore through a clean, user-friendly interface.

---

##  Features

- Displays Pokémon data fetched from the PokéAPI  
- Detail pages for each Pokémon with stats and information  
- Responsive UI using Django templates  
- A starting project to build upon with search, filtering, or caching  

---

##  Prerequisites

- Python 3.8+
- [Pipenv](https://pipenv.pypa.io/) or `venv` for virtual environments
- (Optional) Docker or Podman if running containerized

---

##  Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/ninabel/pokedex.git
cd pokedex
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create admin user
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to browse Pokemons.


## Running with Docker

You can run the application using Docker for easy setup and isolation.

### 1. Build the Docker image

```
docker build -t pokedex:latest .
```

### 2. Run the container (migrations run automatically, detached mode)

```
docker run --name pokedex -d --rm -it -p 8000:8000 pokedex:latest
```

The app listens on 0.0.0.0:8000 in the container and is published to your host at `http://127.0.0.1:8000/`.

### 3. Create a superuser

While container is running, execute the command:

```
docker exec -it pokedex python manage.py createsuperuser
```

### 4. Stop the app

If you started it without --rm or in detached mode, stop it with:

```
docker stop pokedex
```

## Usage

### Anonymous and regular users

- Browse the main page to see the list of Pokémon.
- Open any Pokémon to view its details and stats.
- Use the compare page to compare two Pokémon side by side.

### Admin users

- Sign in at `/admin/` with a superuser account.
- Create and manage user accounts.

### Logged-in users

- Add Pokémon to your personal deck from a Pokémon detail page.
- Remove Pokémon from your deck.
- View your decks via the sidebar under "My decks".
- View pokemons list in your deck.
