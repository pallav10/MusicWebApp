from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token

import exceptions_utils
import messages
from serializers import UserSerializer, UserProfileSerializer, GenreSerializer, SongSerializer


def generate_token(user):
    # Token table is of Django Rest Framework
    # Creates the token at registration time
    token = Token.objects.create(user=user)
    # Return only the key with is associated with the object
    return token.key


def fetch_token(user):
    try:
        # Get the goal for the specified user and return key
        token = Token.objects.get(user_id=user.id)
        return token.key
    except Token.DoesNotExist:
        raise exceptions_utils.ValidationException(messages.TOKEN_NOT_FOUND, status.HTTP_404_NOT_FOUND)


def hash_password(password):
    return make_password(password)


def create_user(data):
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        token = Token.objects.create(user=user)
        keys = ['id', 'first_name', 'last_name', 'email', 'contact_no', 'created'
                ]  # data that we want to return as JSON response
        user_response = {k: v for k, v in user_serializer.data.iteritems() if k in keys}
        user_response['token'] = token.key
        return user_response
    else:
        raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


def update_user(data, user):
    user_serializer = UserProfileSerializer(data=data, instance=user)
    if user_serializer.is_valid():
        user_serializer.save()
        return user_serializer.data
    else:
        raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)


def authenticate_user(user, data):
    if user:
        token = fetch_token(user)
        user_serializer = UserProfileSerializer(user, data=data)
        if user_serializer.is_valid():
            keys = ['id', 'email']
            user_serializer_dict = {k: v for k, v in user_serializer.data.iteritems() if k in keys}
            user_serializer_dict['token'] = token
            user_serializer_dict.update(messages.LOGIN_SUCCESSFUL)
            return user_serializer_dict
        else:
            raise exceptions_utils.ValidationException(user_serializer.errors, status.HTTP_400_BAD_REQUEST)
    else:
        raise exceptions_utils.ValidationException(messages.INVALID_EMAIL_OR_PASSWORD, status.HTTP_401_UNAUTHORIZED)


def create_genre(data):
    genre_serializer = GenreSerializer(data=data)
    if genre_serializer.is_valid():
        genre = genre_serializer.save()
        keys = ['id', 'genre', 'is_favorite']  # data that we want to return as JSON response
        response = {k: v for k, v in genre_serializer.data.iteritems() if k in keys}
        return response
    else:
        raise exceptions_utils.ValidationException(genre_serializer.errors, status.HTTP_400_BAD_REQUEST)


def create_song(data):
    song_serializer = SongSerializer(data=data)
    if song_serializer.is_valid():
        song = song_serializer.save()
        keys = ['id', 'song_title', 'genre', 'audio_file', 'ratings']  # data that we want to return as JSON response
        response = {k: v for k, v in song_serializer.data.iteritems() if k in keys}
        return response
    else:
        raise exceptions_utils.ValidationException(song_serializer.errors, status.HTTP_400_BAD_REQUEST)


def update_track(data, track):
    track_serializer = SongSerializer(data=data, instance=track)
    if track_serializer.is_valid():
        track_serializer.save()
        return track_serializer.data
    else:
        raise exceptions_utils.ValidationException(track_serializer.errors, status.HTTP_400_BAD_REQUEST)


def update_genre(data, genre_info):
    genre_serializer = GenreSerializer(data=data, instance=genre_info)
    if genre_serializer.is_valid():
        genre_serializer.save()
        return genre_serializer.data
    else:
        raise exceptions_utils.ValidationException(genre_serializer.errors, status.HTTP_400_BAD_REQUEST)
