from rest_framework import serializers
from .models import WebResult

class WebSerializer(serializers.ModelSerializer):
    """WebResult serializer"""
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='web-detail',
    #     lookup_field='url'
    # )
    class Meta:
        model = WebResult
        # fields = '__all__'
        fields = ['url', 'http_code', 'datetime', 'ip', 'timeout']
