from django.conf import settings
from django.utils import translation


class ChosenLanguageMiddleware:
    """Use Ukrainian until the visitor presses UA or EN."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        allowed = {code for code, _name in settings.LANGUAGES}
        if language not in allowed:
            language = settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
        response = self.get_response(request)
        response.headers['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
