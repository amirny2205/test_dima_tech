from django.contrib.auth.models import User
from djoser.conf import settings
from djoser.serializers import UserSerializer
from shop.serializers import BillSerializerForUserS


class UserSerializerCustom(UserSerializer):
    bills = BillSerializerForUserS(many=True)

    class Meta:
        depth = 2
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'bills',
        )
        read_only_fields = (settings.LOGIN_FIELD,)
