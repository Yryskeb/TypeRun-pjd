from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView 
from rest_framework.viewsets import ModelViewSet 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response 
from rest_framework.filters import SearchFilter 
from rest_framework.pagination import PageNumberPagination 
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.account.models import Account 
from apps.account.serializers import RegisterSerializer, UserSerializer
from apps.account.tasks import send_activation_email
from apps.account.permissions import IsAuthor


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            try:
                send_activation_email.delay(user.email, user.activation_code)
            except:
                return Response({'message': 'Registered, but troubles with email.', 'data': serializer.data}, status=201)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ActivationView(APIView):
    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(Account, activation_code=code)
        user.is_active = True 
        user.activation_code = 'ACTIVATED'
        return Response('Succesfully activated.', status=status.HTTP_200_OK)
    

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            customer = Account.objects.get(email=email, is_active=True)
        except Account.DoesNotExist:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if customer.check_password(password):
            refresh = RefreshToken.for_user(customer)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh.refresh_token)
            return Response({"access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class StandartPargination(PageNumberPagination):
    page_size = 10 
    page_query_param = 'page'

class UserViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandartPargination 
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('username', 'rank', )
    filterset_fields = ('username', 'rank', )

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthor()]
        return [IsAuthenticatedOrReadOnly()]