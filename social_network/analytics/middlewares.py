from django.utils import timezone
from users.models import EmailRequiredUser as User


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set last_request time for authenticated users
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            user.last_request = timezone.now()
            user.save()

        return response
