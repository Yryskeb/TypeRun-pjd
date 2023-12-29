from rest_framework import serializers 
from apps.account.models import Account 


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    
    class Meta:
        model = Account 
        fields = ('username', 'password', 'password_confirm', 'email', 'rank', )

    def validate(self, attrs):
        password = attrs['password']
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            raise  serializers.ValidationError(
                'Passwords didnt match!'
            )
        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError(
                'Password feild must contain alpha and numeric symbols'
            )
        return attrs
    
    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account 
        exclude = ('password', )