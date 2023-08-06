from __future__ import annotations
from .__version__ import __version__  # noqa
from .lib import export
from typing import Type, TypeVar, List, Dict
import praw  # type: ignore
import requests

__all__ = []  # type: List

__header__ = 'plex_posters'
# __section__ = 'module'

T_movie_poster_porn_scraper = TypeVar(
    'T_movie_poster_porn_scraper', bound="movie_poster_porn_scraper"
)


@export
class movie_poster_porn_scraper(object):

    """Poster scraper

    Attributes
    ----------
    reddit_instance : praw.Reddit
        A praw instance connected to Reddit
    """

    def __init__(self, instance: praw.Reddit) -> None:
        """
        Parameters
        ----------
        instance : praw.Reddit
            A praw instance connected to Reddit
        """
        super().__init__()
        self.reddit_instance = instance

    @classmethod
    def create_instance(
        cls: Type[T_movie_poster_porn_scraper],
        client_id: str,
        client_secret: str,
        user_agent: str,
    ) -> T_movie_poster_porn_scraper:
        """`classmethod` to connect to reddit using the api.

        Parameters
        ----------
        client_id : str
            a valid client id
        client_secret : str
            the secret key for the client
        user_agent : str
            a user agent
        """
        reddit_instance = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

        return cls(reddit_instance)

    def get_hot_posters(
        self,
    ) -> T_movie_poster_porn_scraper:
        """
        """
        self._poster_urls: Dict = {}
        for post in self.reddit_instance.subreddit('MoviePosterPorn').hot(
            limit=10
        ):
            print(post.title)
            print(post.url)
            # print(dir(post))
            # self._poster_urls.append(post.url)
            self._poster_urls[post.title] = post.url
        print(self._poster_urls)
        return self

    def get_posters(self):
        """download the posters

        Returns
        -------
        self
        """
        for title, url in self._poster_urls.items():
            r = requests.get(url)
            with open('posters/' + title + '.jpg', 'wb') as p:
                p.write(r.content)
        return self
