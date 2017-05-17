from rest_framework import serializers
from models import User


# used for registration, it holds the value of user table with all fields.
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'country_code', 'contact_no',
                  'created', 'modified', 'city', 'state', 'country')


# serialize data of user for common need of user table.
class UserProfileSerializer(serializers.ModelSerializer):
    contact_no = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'first_name', 'last_name', 'created', 'country_code', 'contact_no', 'city',
            'state', 'country')


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'genre', 'song_title', 'audio_file', 'is_favorite')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'genre', 'is_favorite')
