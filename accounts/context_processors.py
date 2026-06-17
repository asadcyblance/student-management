from .models import UserProfile


def sidebar_profile(request):
    if not request.user.is_authenticated:
        return {'sidebar_profile': None}

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return {'sidebar_profile': profile}
