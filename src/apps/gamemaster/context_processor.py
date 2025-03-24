from .views import is_gamemaster

def gamemaster_status(request):
    return {
        "is_gamemaster": is_gamemaster(request.user) if request.user.is_authenticated else False,
        "current_page": request.resolver_match.url_name if request.resolver_match else None,
    }