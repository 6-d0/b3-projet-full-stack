# Web
## 3 dossiers
- `backend`: api
- `frontend`: les pages web
- `proxy`: la liaison des 2
----
Pour lancer le projet, il faut se rendre dans chacun de ces 3 dossiers depuis un terminal et faire:
### `backend`
présent sur le port `8000`
```sh
cd backend
uv sync
uv run manage.py makemigrations     # au cas où
uv run manage.py migrate            # appliquer les migrations
uv run python reviwcopies/scripts/populate_ft1.py
uv run manage.py runserver 8000
```

### `frontend`
présent sur le port `3000`
> #### Prérequis
> -  `npm`

```sh
cd frontend
npm install
npm run dev
```

## proxy
> #### Prérequis
> - [caddy](https://caddyserver.com/docs/install#debian-ubuntu-raspbian) (pour linux je pense)

```sh
cd proxy
./chemin/vers/caddy run
```

# Connexion
[localhost:9000](localhost:9000)
```
h000123 - motdepasse -> teacher
e111111 - motdepasse -> student
admin - motdepasse -> admin (baclé lui)
```
