from typing import Optional

from pydantic import BaseModel

from .request import Media


class MusicTrack(BaseModel):
    # The name of the musician
    author: str

    # A HD version of the music's cover art
    cover_hd: Optional[Media] = None

    # A large version of the music's cover art
    cover_large: Optional[Media] = None

    # A medium version of the music's cover art
    cover_medium: Optional[Media] = None

    # A thumbnail version of the music's cover art
    cover_thumb: Media

    # The duration of the track
    duration: int

    # The ID of the track
    id: str

    # The handle of the owner of the track
    owner_handle: str

    # The ID of the owner of the track
    owner_id: Optional[str] = None

    # The nickname of the owner of the track
    owner_nickname: str

    # The link to play this track
    play_url: Media

    # The title of this track
    title: str

    # The number of posts that use this track
    user_count: int
