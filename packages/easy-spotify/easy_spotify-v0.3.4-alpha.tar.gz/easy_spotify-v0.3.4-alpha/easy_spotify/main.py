import requests
import json
from requests.auth import HTTPBasicAuth
from easy_spotify.artist import Artist


class Spotify:
    def __init__(self, client_id, client_secret):
        """
        Creates an authenticated Spotify object.

        :param client_id: Your client ID obtained on the Spotify Developers Website
        :param client_secret: Your client secret obtained on the Spotify Developers Website
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_access_token()

    def __repr__(self):
        return "Spotify API Wrapper"

    def get_access_token(self):
        """
        :return: Access token required to send requests to the Spotify Web API
        :rtype: str
        """
        token_url = 'https://accounts.spotify.com/api/token'
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {'grant_type': 'client_credentials'}
        request_token = requests.post(token_url, data, auth=auth)
        if request_token:
            if request_token.ok:
                return json.loads(request_token.text)['access_token']
            else:
                print(f"Request token not ok, error code: {request_token.status_code}")
        print(f"Token Access Failed.")
        exit()

    def _make_request(self, url, parameters=None):
        """
        Send a request to the Spotify Web API to get data.

        :param url: URL to send the request to
        :param parameters: Parameters to pass in the request
        :return: Data given by the Spotify Web API
        """
        headers = {'Authorization': 'Bearer ' + self.token}
        data = requests.get(url, headers=headers, params=parameters)
        if data.ok:
            return data
        print(f"Request failed to {url}. Error type: {data.status_code}")
        return None

    def get_artist_object(self, artist_id):
        """
        :param artist_id: ID of an artist in Spotify's catalogue
        :return: Artist object
        """
        artist_info = self.get_artist_info_from_id(artist_id)
        artist_albums = self.get_albums_from_id(artist_id)
        artist_top_tracks = self.get_artist_top_tracks_from_id(artist_id, True)
        if artist_info and artist_albums:
            artist = Artist(artist_info["name"], artist_id, artist_info["followers"], artist_info["genres"],
                            artist_info["popularity"], artist_info["image_link"], artist_albums, artist_top_tracks)
            return artist
        print("Unable to create artist object.")
        return None

    def get_artist_id(self, search_query, limit=1, only_id=True):
        """
        Search for an artist's ID by name.

        :param search_query: Name of artist
        :param limit: Number of results you want to get the ID for
        :param only_id: Get back only the id of the artist and not the name
        :return: artist's ID(s)
        """
        artist_id_data = self._make_request("https://api.spotify.com/v1/search",
                                            {"query": search_query, "type": "artist", "limit": limit})
        if artist_id_data:
            artist_id_json = artist_id_data.json()
            if artist_id_json["artists"]["total"] == 0:
                print("No artist was found.")
                return None
            if only_id:
                result = [result["id"] for result in artist_id_json["artists"]["items"]]
            else:
                result = [(result["id"], result["name"]) for result in artist_id_json["artists"]["items"]]
            if limit == 1:
                return result[0]
            return result

        print("Request failed. No artist id was obtained.")
        return None

    def get_track_id(self, search_query, limit=1):
        """
        Search for a track ID by it's name.

        :param search_query: Name of the track you are looking for
        :param limit: Number of results you want to get the ID for
        :return: the track ID
        """
        track_id_data = self._make_request("https://api.spotify.com/v1/search",
                                            {"query": search_query, "type": "track", "limit": limit})
        if track_id_data:
            track_id_json = track_id_data.json()
            if track_id_json["tracks"]["total"] == 0:
                print("No track was found.")
                return None
            result = [result["id"] for result in track_id_json["tracks"]["items"]]
            if limit == 1:
                return result[0]
            return result
        return None

    def get_multiple_track_id(self, search_queries):
        """
        Look up the ID of multiple tracks with different names.

        :param search_queries: Name of tracks
        :type search_queries: list
        :return: list of track IDs
        """
        track_ids = []
        for query in search_queries[:20]:
            track_id = self.get_track_id(query)
            track_ids.append(track_id)
        return track_ids

    def get_artist_info_from_name(self, artist_name):
        """
        Get the info for an artist by name.

        :param artist_name: The artist's name
        :return: Artist information
        :rtype: dict
        """
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_artist_info_from_id(artist_id)
        return None

    def get_artist_info_from_id(self, artist_id):
        """
        Get the info for an artist by ID.

        :param artist_id: The artist's ID
        :return: Artist information
        :rtype: dict
        """
        artist_info_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}")
        if artist_info_data:
            artist_info_json = artist_info_data.json()
            followers = artist_info_json["followers"]["total"]
            genres = artist_info_json["genres"]
            image_link = artist_info_json["images"][0]["url"]
            popularity = artist_info_json["popularity"]
            name = artist_info_json["name"]
            return {"name": name, "genres": genres, "image_link": image_link,
                    "popularity": popularity, "followers": followers}
        print("Request failed. No artist information was obtained.")
        return None

    def get_albums_from_id(self, artist_id, just_id_and_name=False):
        """
        Get an artist's albums with its ID.

        :param artist_id: The artist's ID
        :param just_id_and_name: Get just the ID and name
        :return: List of albums
        :rtype: list
        """
        artist_albums_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/albums")
        if artist_albums_data:
            artist_albums = []
            for album in artist_albums_data.json()["items"]:
                album_id = album["id"]
                album_name = album["name"]
                if just_id_and_name:
                    artist_albums.append({"id": album_id, "name": album_name})
                else:
                    artist_name = album["artists"][0]["name"]
                    release_date = album["release_date"]
                    total_tracks = album["total_tracks"]
                    album_cover = album["images"][0]["url"]
                    artist_albums.append({"artist": artist_name, "id": album_id, "name": album_name,
                                          "release_date": release_date, "total_tracks": total_tracks,
                                          "cover": album_cover})
            return artist_albums
        print("Request failed. No albums were obtained.")
        return None

    def get_albums_from_name(self, artist_name, just_id_and_name=False):
        """
        Get an artist's albums by name.

        :param artist_name: The artist's name
        :param just_id_and_name: Get just the ID and name
        :return: List of albums
        :rtype: list
        """
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_albums_from_id(artist_id, just_id_and_name)
        return None

    def get_artist_top_tracks_from_id(self, artist_id, just_id_and_name=False):
        """
        Get an artist's top tracks by ID.

        :param artist_id: The artist's ID
        :param just_id_and_name: Get just the ID and name
        :return: list of tracks
        :rtype: list
        """
        top_tracks_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
                                             {"market": "US"})
        if top_tracks_data:
            artist_tracks = []
            for track in top_tracks_data.json()["tracks"]:
                track_id = track["id"]
                track_name = track["name"]
                if just_id_and_name:
                    artist_tracks.append({"id": track_id, "name": track_name})
                else:
                    album_name = track["album"]["name"]
                    is_explicit = track["explicit"]
                    duration = track["duration_ms"]
                    track_artists = []
                    for artist in track["artists"]:
                        track_artists.append({"name": artist["name"], "id": artist["id"]})
                    artist_tracks.append({"id": track_id, "track_name": track_name, "artists": track_artists,
                                          "album_name": album_name, "is_explicit": is_explicit, "duration": duration})
            return artist_tracks
        return None

    def get_artist_top_tracks_from_name(self, artist_name, just_id_and_name=False):
        """
        Get an artist's top tracks by name.

        :param artist_name: The artist's name
        :param just_id_and_name: Get just the ID and name
        :return: list of tracks
        :rtype: list
        """
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_artist_top_tracks_from_id(artist_id, just_id_and_name)
        return None
    
    def get_tracks_of_album(self, album_id):
        """
        Get an album's tracks by ID.

        :param album_id: The album's ID
        :return: list of tracks
        :rtype: list
        """
        tracks_data = self._make_request(f"https://api.spotify.com/v1/albums/{album_id}/tracks", {"limit": 50})
        if tracks_data:
            tracks = []
            for track in tracks_data.json()["items"]:
                track_name = track["name"]
                track_id = track["id"]
                artists = []
                for artist in track["artists"]:
                    artists.append({"name": artist["name"], "id": artist["id"]})
                tracks.append({"name": track_name, "id": track_id, "artists": artists})
            return tracks
        return None

    def get_track_audio_features(self, track_id):
        """
        Get a track's audio features.

        :param track_id: The track ID
        :return: dictionary with audio features
        :rtype: dict
        """
        audio_features_data = self._make_request(f"https://api.spotify.com/v1/audio-features/{track_id}")
        if audio_features_data:
            return audio_features_data.json()
        return None

    def get_related_artists(self, artist_id):
        """
        Get related artists to an artist by ID.

        :param artist_id: The artist's ID
        :return: list of related artists
        :rtype: list
        """
        related_artists_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/related-artists")
        if related_artists_data:
            related_artists = []
            for artist in related_artists_data.json()["artists"]:
                artist_name = artist["name"]
                artist_id = artist["id"]
                related_artists.append({"name": artist_name, "id": artist_id})
            return related_artists
        return None

    def get_multiple_tracks_audio_features(self, tracks_id):
        """
        Get the audio features of multiple tracks with different IDs.

        :param tracks_id: A list of track IDs
        :return: dictionary with audio features
        :rtype: dict
        """
        id_string = ""
        for track_id in tracks_id:
            id_string += track_id + ","
        audio_features_data = self._make_request(f"https://api.spotify.com/v1/audio-features/?ids={id_string[:-1]}")
        if audio_features_data:
            return audio_features_data.json()
        return None

    def get_track_info(self, track_id):
        """
        Get a track's information by ID.

        :param track_id: The track ID
        :return: dictionary with information
        :rtype: dict
        """
        track_info_data = self._make_request(f"https://api.spotify.com/v1/tracks/{track_id}")
        if track_info_data:
            track_info_json = track_info_data.json()
            name = track_info_json["album"]["artists"][0]["name"]
            artist_id = track_info_json["album"]["artists"][0]["id"]
            song = track_info_json["name"]
            image = track_info_json["album"]["images"][1]
            return {"name": name, "artist_id": artist_id, "song": song, "image": image}

    def get_multiple_tracks_info(self, tracks_id):
        """
        Get information for multiple tracks by IDs.

        :param tracks_id: list of track IDs
        :return: list of track information
        :rtype: list
        """
        id_string = ""
        for track_id in tracks_id:
            id_string += track_id + ","
        track_info_data = self._make_request(f"https://api.spotify.com/v1/tracks/?ids={id_string[:-1]}")
        if track_info_data:
            tracks_info = []
            tracks = track_info_data.json()["tracks"]
            for track in tracks:
                name = track["album"]["artists"][0]["name"]
                artist_id = track["album"]["artists"][0]["id"]
                song = track["name"]
                image = track["album"]["images"][1]
                tracks_info.append({"name": name, "artist_id": artist_id, "song": song, "image": image})
            return tracks_info
        return None

