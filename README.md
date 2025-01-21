# softorks.eu | softarna.cz
The project of my website itself.

# Environment variables needed to set
## Development
- `DJANGO_SETTINGS_MODULE` => **www.settings**
- `SECRET_KEY` **xxx**
- `DEBUG` => **1**
- `DATABASE_NAME` => **xxx**

## Production
- `PYTHONPATH` => **...www/www**
- `DJANGO_SETTINGS_MODULE` => **www.settings**
- `ALLOWED_HOSTS` => **softarna.cz,softorks.eu**
- `SECRET_KEY` **xxx**
- `DEBUG` => **0**
- `DATABASE_NAME` => **xxx**
- `STATIC_ROOT` => **xxx**
