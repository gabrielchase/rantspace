from rest_framework import (
    serializers,
    pagination
)

from user_profile.models import UserProfile
from menu_item.serializers import MenuItemSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer for UserProfile objects"""
    
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'email', 'business_name', 'identifier', 'full_business_name',
            'owner_surname', 'owner_given_name', 'password',
            'address', 'city', 'state', 'menu_items'
        )
        extra_kwargs = {
            'full_business_name': {'read_only': True},
            'password': { 'write_only': True }
        }

    def create(self, validated_data):
        """ Create and return a new user """

        user = UserProfile(
            email=validated_data.get('email'),
            business_name=validated_data.get('business_name'),
            identifier=validated_data.get('identifier'),
            owner_surname=validated_data.get('owner_surname'),
            owner_given_name=validated_data.get('owner_given_name'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state')
        )

        user.full_business_name = user.get_full_name()

        user.set_password(validated_data.get('password'))
        user.save()

        return user

    def update(self, full_business_name, validated_data):
        user = UserProfile.objects.get(full_business_name=full_business_name)

        for k, v in validated_data.items():
            if k != 'password':
                setattr(user, k, v)
            else:
                user.set_password(validated_data.get('password'))
        
        user.full_business_name = user.get_full_name()
        user.save()

        return user
