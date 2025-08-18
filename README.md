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
Note: If the app is read-only and doesn’t use its own models, migrations may not apply.
```

### 5. Run the development server
```bash
python manage.py runserver
Visit http://127.0.0.1:8000/ to browse Pokémon.
```
