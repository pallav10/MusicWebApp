from django.contrib.auth import authenticate
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import messages
import utils
import validations_utils
from models import Genre, Song
from exceptions_utils import ValidationException
from permission import UserPermissions
from serializers import UserProfileSerializer, GenreSerializer, SongSerializer


# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_registration(request):
    """
    **Registers a new user- Ignore**

    * Accepts only POST requests
dd
    > POST

    * Requires following fields of users in JSON format:

        - Sign Up with Email

            1. `email` - Valid email address
            2. `password` - String


    * Possible HTTP status codes and JSON response:

        * `HTTP_201_CREATED` - When new user registration is done successfully:

                {
                      "first_name": null or string,
                      "last_name": null or string,
                      "created": date_timestamp,
                      "contact_no": integer,
                      "token": "token string",
                      "user_role": integer,
                      "email": string
                }

        * `HTTP_400_BAD_REQUEST` :

            - Email already used to register one user.
            Use a different email address

                {
                 "message": "User with this email already exists."
                }

        * `HTTP_400_BAD_REQUEST` - Invalid email address

                {
                    "message": "Enter a valid email address."
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

    * Status code can be used from HTTP header. A separate status field in json
    data is not provided.
    :param request:

    """
    if request.method == 'POST':
        try:
            data = validations_utils.email_validation(
                request.data)  # Validates email id, it returns lower-cased email in data.
            data = validations_utils.password_validation(data)  # Validates password criteria.
            data['password'] = utils.hash_password(data['password'])  # password encryption
            data = utils.create_user(data)  # Creates user with request data.
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)


@api_view(['GET', 'PUT'])
@permission_classes((UserPermissions, IsAuthenticated))
def user_detail(request, pk):
    """

    **Get or change the user profile data- Ignore**

    > GET

    Returns the User Profile data.

    * Requires `user id` which is an integer and taken as primary key
    to identify user.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` - Returns the User Profile data:

                {
                  "email": String,
                  "id": Integer,
                  "first_name": String,
                  "last_name": String,
                  "created": String,
                  "contact_no": Integer
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error



    > PUT

    ### Update User Profile Data

    * Requires data that needs to be changed. Any and all of the below fields
    could be modified in a single PUT request.

        1. `first_name`: String
        2. `last_name`: String
        3. `contact_no`: Integer
        4. `email` : String


    * Requires only the changed data of the user and `email` along the changed
    parameters.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` - User profile data in JSON format:

                {
                  "email": String,
                  "id": Integer,
                  "first_name": String,
                  "last_name": String,
                  "created": String,
                  "contact_no": Integer
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR`

        :param pk:
        :param request:
    """
    data = request.data
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    if request.method == 'GET':
        user_profile_serializer = UserProfileSerializer(user)
        return Response(user_profile_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        try:
            data = validations_utils.email_validation(data)  # Validates email id, it returns lower-cased email in data.
            updated_data = utils.update_user(data, user)  # Updates user data.
            return Response(updated_data, status=status.HTTP_200_OK)
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_login(request):
    """
    **User Login**

    Login an existing user.

    Used for authenticating the user.

    > POST

    * Requires following fields of users in JSON format:

        1. `email` - String
        2. `password` - String

    * Returns user profile data on successful login.
    * Also returns Authentication token to be used by frontend for further
     communication with backend.
    * On failure it returns appropriate HTTP status and message in JSON
    response.

    * Possible HTTP status codes and JSON response:

        * `HTTP_200_OK` on successful login.

        * `HTTP_401_UNAUTHORIZED` for failed login attempt.

                {
                 "message": "Invalid username or password"
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error.

        * `HTTP_404_NOT_FOUND` - When user is not found.

                {
                 "message": "User with specified email does not exist."
                }
    :param request:
    """
    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response(
            messages.REQUIRED_EMAIL_AND_PASSWORD,
            status=status.HTTP_400_BAD_REQUEST)
    try:
        user = authenticate(email=email, password=password)  # Validates credentials of user.
    except ValidationException:
        return Response(messages.INVALID_EMAIL_OR_PASSWORD, status=status.HTTP_401_UNAUTHORIZED)
    try:
        login_user = utils.authenticate_user(user, request.data)  # Authorizes the user and returns appropriate data.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    return Response(login_user, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((UserPermissions, IsAuthenticated))
@cache_page(60 * 15)
def genre(request, pk):
    """
    **creates a new genre**

    * Accepts only POST requests
dd
    > POST

    * Requires following fields of users in JSON format:

        - Sign Up with Email

            1. `genre` - genre type


    * Possible HTTP status codes and JSON response:

        * `HTTP_201_CREATED` - When new genre creation is done successfully:

                {
                      "id": integer
                      "genre": string
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

    * Status code can be used from HTTP header. A separate status field in json
    data is not provided.
    :param pk:
    :param request:

    """
    if request.method == 'POST':
        try:
            user = validations_utils.user_validation(pk)  # Validates if user exists or not.
            validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)
        try:
            data = request.data
            genre_data = utils.create_genre(data)  # Creates genre with request data.
            return Response(genre_data, status=status.HTTP_201_CREATED)
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)


@api_view(['POST'])
@permission_classes((UserPermissions, IsAuthenticated))
@cache_page(60 * 15)
def song(request, pk):
    """
    **creates a new song**

    * Accepts only POST requests
dd
    > POST

    * Requires following fields of users in JSON format:

        - Sign Up with Email

            1. `song_title` - string
            2. `genre` - genre type(string)
            3. `audio_file` - file
            4. `ratings` - integer between 0 to 5


    * Possible HTTP status codes and JSON response:

        * `HTTP_201_CREATED` - When new genre creation is done successfully:

                {
                      "id":integer,
                      "song_title": string,
                      "genre": string,
                      "audio_file": file,
                      "ratings": integer,
                }

        * `HTTP_500_INTERNAL_SERVER_ERROR` - Internal server error

    * Status code can be used from HTTP header. A separate status field in json
    data is not provided.
    :param pk:
    :param request:

    """
    if request.method == 'POST':
        try:
            user = validations_utils.user_validation(pk)  # Validates if user exists or not.
            validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)
        try:
            data = request.data
            song_data = utils.create_song(data)  # Creates song with request data.
            return Response(song_data, status=status.HTTP_201_CREATED)
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)


@api_view(['GET'])
@permission_classes((UserPermissions, IsAuthenticated))
@cache_page(60 * 15)
def get_all_genres(request, pk):
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    if request.method == 'GET':
        genres = Genre.objects.filter(user_id=user.id)
        genre_serializer = GenreSerializer(genres, many=True)
        return Response(genre_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes((UserPermissions, IsAuthenticated))
@cache_page(60 * 15)
def genre_detail(request, pk, key):
    data = request.data
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
        genre_info = validations_utils.genre_validation(key)
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)

    if request.method == 'GET':
        genre_serializer = GenreSerializer(genre_info)
        return Response(genre_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        try:
            updated_genre = utils.update_genre(data, genre_info)  # Updates genre details.
            return Response(updated_genre, status=status.HTTP_200_OK)
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)


@api_view(['GET'])
@permission_classes((UserPermissions, IsAuthenticated))
@cache_page(60 * 15)
def get_all_tracks(request, pk):
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)
    query_params = request.query_params.dict()  # Gets parameters.
    if request.method == 'GET':
        if 'song_title' in query_params:
            filter_by_title = str(query_params['song_title'][:-1] if '/' in query_params['song_title']
                                  else query_params['song_title'])
            track = Song.objects.filter(user_id=user.id,
                                        song_title=filter_by_title)  # Get all tracks for particular title
            track_serializer = SongSerializer(track, many=True)
            return Response(track_serializer.data, status=status.HTTP_200_OK)
        elif 'genre' in query_params:
            filter_by_genre = str(query_params['genre'][:-1] if '/' in query_params['genre']
                                  else query_params['genre'])
            track = Song.objects.filter(user_id=user.id,
                                        genre=filter_by_genre)  # Get all tracks for particular genre
            track_serializer = SongSerializer(track, many=True)
            return Response(track_serializer.data, status=status.HTTP_200_OK)
        else:
            track = Song.objects.filter(user_id=user.id)  # Get all tracks for particular user
            track_serializer = SongSerializer(track, many=True)
            return Response(track_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes((UserPermissions, IsAuthenticated))
@cache_page(60 * 15)
def track_detail(request, pk, key):
    data = request.data
    try:
        user = validations_utils.user_validation(pk)  # Validates if user exists or not.
        validations_utils.user_token_validation(request.auth.user_id, pk)  # Validates user's Token authentication.
        track = validations_utils.track_validation(key)
    except ValidationException as e:  # Generic exception
        return Response(e.errors, status=e.status)

    if request.method == 'GET':
        track_serializer = SongSerializer(track)
        return Response(track_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        try:
            updated_track = utils.update_track(data, track)  # Updates track details.
            return Response(updated_track, status=status.HTTP_200_OK)
        except ValidationException as e:  # Generic exception
            return Response(e.errors, status=e.status)

