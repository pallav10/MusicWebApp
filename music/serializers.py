from rest_framework import serializers
from models import User, Song, Genre


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


# it holds the value of song table with all fields.
class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('id', 'song_title', 'genre', 'audio_file', 'ratings', 'is_deleted')


# it holds the value of genre table with all fields.
class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'genre', 'is_favorite', 'is_deleted')
