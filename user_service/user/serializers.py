import re
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, FullName, Address

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = ['first_name', 'mid_name', 'last_name']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model: Address
        fields: ['houseNumber', 'street', 'city', 'district', 'nationality']

class UserSerializer(serializers.ModelSerializer):
    full_name = FullNameSerializer()
    address = AddressSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'address']
        extra_kwargs = {
            'password': {'write_only': True},  # Đảm bảo mật khẩu không được trả về khi serialized
        }

    def validate_password(self, value):
        # Kiểm tra độ dài của mật khẩu
        if len(value) < 8:
            raise serializers.ValidationError("Mật khẩu phải có ít nhất 8 ký tự.")

        # Kiểm tra xem mật khẩu có chứa ký tự hoa, thường và số không
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một ký tự hoa.")

        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một ký tự thường.")

        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Mật khẩu phải chứa ít nhất một số.")

        # Kiểm tra mật khẩu theo các quy tắc mặc định của Django
        try:
            validate_password(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        return value

    def create(self, validated_data):
        # Extract nested data for FullName and Address
        full_name_data = validated_data.pop('full_name', None)
        address_data = validated_data.pop('address', None)

        # Create FullName and Address instances if provided
        full_name = FullName.objects.create(**full_name_data) if full_name_data else None
        address = Address.objects.create(**address_data) if address_data else None

        # Create the user with the created FullName and Address
        print("ok")
        user = User.objects.create(full_name=full_name, address=address, **validated_data)
        user.set_password(validated_data['password'])  # Set the password
        user.save()
        return user

    def update(self, instance, validated_data):
        full_name_data = validated_data.pop('full_name', None)
        address_data = validated_data.pop('address', None)

        if full_name_data:
            if instance.full_name:
                FullName.objects.filter(id=instance.full_name.id).update(**full_name_data)
            else:
                full_name = FullName.objects.create(**full_name_data)
                instance.full_name = full_name

        if address_data:
            if instance.address:
                Address.objects.filter(id=instance.address.id).update(**address_data)
            else:
                address = Address.objects.create(**address_data)
                instance.address = address

        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
