from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin(request):
    username = "evaldo"
    password = "admin123"
    email = "evaldo.dev2025@gmail.com"

    if User.objects.filter(username=username).exists():
        return HttpResponse("✅ Usuário já existe.")

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    return HttpResponse("✅ Superusuário criado com sucesso!")
