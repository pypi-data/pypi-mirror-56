class Artist:
    def __init__(self, name, artist_id, followers, genres, popularity, image, albums, top_tracks):
        self.name = name
        self.artist_id = artist_id
        self.followers = followers
        self.genres = genres
        self.popularity = popularity
        self.image = image
        self.albums = albums
        self.top_tracks = top_tracks

    def __repr__(self):
        return f"Artist object for {self.name}"

    def get_data(self):
        return {"name": self.name, "genres": self.genres, "image_link": self.image,
                "popularity": self.popularity, "followers": self.followers,
                "albums": self.albums, "top_tracks": self.top_tracks}
