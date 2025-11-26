from django.contrib.auth.models import User
from rest_framework import generics, viewsets, permissions
from .models import Address
from .serializers import RegisterSerializer, UserSerializer, AddressSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/accounts/register/
    Creates a new user and a CustomerProfile.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET /api/accounts/me/  -> get details of logged-in user
    PUT/PATCH /api/accounts/me/ -> update first_name, last_name, email
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AddressViewSet(viewsets.ModelViewSet):
    """
    CRUD for addresses of the logged-in user.

    Endpoints:
    - GET /api/accounts/addresses/
    - POST /api/accounts/addresses/
    - GET /api/accounts/addresses/{id}/
    - PUT/PATCH /api/accounts/addresses/{id}/
    - DELETE /api/accounts/addresses/{id}/
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return addresses for the current authenticated user
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate address with the current user
        serializer.save(user=self.request.user)