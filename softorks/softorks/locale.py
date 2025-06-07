from django.middleware.locale import LocaleMiddleware
from django.utils import translation
from django.conf import settings


class LanguageMiddleware(LocaleMiddleware):
    def process_request(self, request):
        host = request.get_host().split(":")[0]
        language_from_domain = getattr(settings, "DOMAIN_LANGUAGE_MAP", {}).get(host, None)

        if language_from_domain is not None:
            translation.activate(language_from_domain)
            request.LANGUAGE_CODE = language_from_domain
        else:
            super().process_request(request)
