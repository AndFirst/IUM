from pydantic import BaseModel, validator
# Klasa Pydantic do walidacji danych wejściowych,


class FeaturesInput(BaseModel):
    number_of_advertisements: int
    number_of_skips: int
    number_of_likes: int
    total_tracks_duration_ms: float
    number_of_different_artists: int
    average_release_date: float
    average_duration_ms: float
    explicit_tracks_ratio: float
    average_popularity: float
    average_acousticness: float
    average_danceability: float
    average_energy: float
    average_instrumentalness: float
    average_liveness: float
    average_loudness: float
    average_speechiness: float
    average_tempo: float
    average_valence: float

    @validator("number_of_advertisements", "number_of_skips", "number_of_likes",
               "number_of_different_artists", "average_duration_ms", "average_popularity",
               "average_tempo",
               )
    def validate_not_negative_value(cls, value):
        if value < 0:
            raise ValueError("variable cannot be negative")
        return value

    @validator("explicit_tracks_ratio", "average_acousticness", "average_danceability",
               "average_energy", "average_instrumentalness", "average_liveness",
               "average_speechiness", "average_valence"
               )
    def validate_percent_value(cls, value):
        if value < 0 or value > 1:
            raise ValueError("percent_variable must be between 0 and 1")
        return value

    @validator("average_loudness",)
    def validate_not_positive_value(cls, value):
        if value > 0:
            raise ValueError("variable cannot be positive")
        return value


class PredictionResult(BaseModel):
    premium_purchased: int
    premium_purchased_this_month: int

    @validator("premium_purchased", "premium_purchased_this_month")
    def validate_binary_variable(cls, value):
        if value not in {0, 1}:
            raise ValueError("binary_variable must be 0 or 1")
        return value


class FeaturesInputAB(BaseModel):
    user_id: int
    number_of_advertisements: int
    number_of_skips: int
    number_of_likes: int
    total_tracks_duration_ms: float
    number_of_different_artists: int
    average_release_date: float
    average_duration_ms: float
    explicit_tracks_ratio: float
    average_popularity: float
    average_acousticness: float
    average_danceability: float
    average_energy: float
    average_instrumentalness: float
    average_liveness: float
    average_loudness: float
    average_speechiness: float
    average_tempo: float
    average_valence: float

    @validator("number_of_advertisements", "number_of_skips", "number_of_likes",
               "number_of_different_artists", "average_duration_ms", "average_popularity",
               "average_tempo", "user_id",
               )
    def validate_not_negative_value(cls, value):
        if value < 0:
            raise ValueError("variable cannot be negative")
        return value

    @validator("explicit_tracks_ratio", "average_acousticness", "average_danceability",
               "average_energy", "average_instrumentalness", "average_liveness",
               "average_speechiness", "average_valence"
               )
    def validate_percent_value(cls, value):
        if value < 0 or value > 1:
            raise ValueError("percent_variable must be between 0 and 1")
        return value

    @validator("average_loudness",)
    def validate_not_positive_value(cls, value):
        if value > 0:
            raise ValueError("variable cannot be positive")
        return value
