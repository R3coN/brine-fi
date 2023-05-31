from rest_framework import serializers
from alerts.models import Alert, Statuses


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alert
        fields = "__all__"