# softorks.eu | softarna.cz
The project of my website itself.

# Environment variables needed to set in file `softorks/.env`
## Development
- `SECRET_KEY` **xxx**
- `DEBUG` => **1**
- `DATABASE_NAME` => **xxx**

## Production
- `ALLOWED_HOSTS` => **softarna.cz,softorks.eu**
- `SECRET_KEY` **xxx**
- `DEBUG` => **0**
- `DATABASE_NAME` => **xxx**
- `STATIC_ROOT` => **xxx**

Please, place `gunicorn.conf.py` and `.env` files separately.
