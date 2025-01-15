# Lancement du serveur de test

```sh
# Installer les dépencances de uv.lock
uv sync

uv run manage.py migrate

uv run reviewcopies/scripts/populate_ft1.py

uv run manage.py runserver
```
