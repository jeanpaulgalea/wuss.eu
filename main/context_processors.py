from django.conf import settings

def site(request):
    return '%s://%s' % ('https' if request.is_secure() else 'http',
                        request.get_host())
