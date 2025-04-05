from rest_framework import serializers

from accounts.models import Users


class PhoneNumberSerializer(serializers.Serializer):
    number_phone = serializers.CharField()

    def validate_number_phone(self, value):
        if Users.objects.filter(number_phone=value).exists():
            raise serializers.ValidationError("Номер уже зарегистрирован")
        return value


class ConfirmCodeSerializer(serializers.Serializer):
    number_phone = serializers.CharField()
    code = serializers.CharField(max_length=4)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["notification"]
