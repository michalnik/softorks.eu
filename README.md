# softorks.eu | softarna.cz
The project of my website itself.

# Environment variables needed to set in file `www/.env`
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

## Before run in production you need to build some parts
1. compile locale translations - `python manage.py compilemessages`
2. replace static files into static root - `python manage.py collectstatic`
