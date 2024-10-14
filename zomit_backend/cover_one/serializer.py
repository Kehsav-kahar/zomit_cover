from rest_framework import serializers
from .models import two_d_cover

class two_d_cover_serializers(serializers.ModelSerializer):
    class Meta:
        model = two_d_cover
        fields = ['id', 'cover_model', 'cover_template', 'created_at']  # Include the new fields
