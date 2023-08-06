import requests
from .calculations import counting_days_release

main_url = 'https://api.crackwatch.com/api/games?'


class UnreleasedGames:
    def __init__(self, page=0, count=0, sort_by='release_date', is_aaa='false'):
        url = f'{main_url}page={page}&sort_by={sort_by}&is_aaa={is_aaa}' \
            f'&is_cracked=false&is_released=false'

        result = requests.get(url).json()
        self.game_info = result[count]
        self.status = 'UNRELEASED'

    @property
    def get_title(self):
        return self.game_info['title']

    @property
    def get_slug(self):
        return self.game_info['slug']

    @property
    def get_release_date(self):
        return self.game_info['releaseDate'][:10]

    @property
    def get_counting(self):
        return counting_days_release(self.game_info['releaseDate'][:10])

    @property
    def get_protection(self):
        return self.game_info['protections']

    @property
    def get_version(self):
        return self.game_info['versions']

    @property
    def get_image(self):
        return self.game_info['image']

    @property
    def get_poster(self):
        return self.game_info['imagePoster']

    @property
    def is_aaa(self):
        return self.game_info['isAAA']

    @property
    def get_comments_count(self):
        return self.game_info['commentsCount']

    @property
    def get_followers_count(self):
        return self.game_info['followersCount']

    @property
    def get_url(self):
        return self.game_info['url']

    @property
    def get_id(self):
        return self.game_info['_id']

    @property
    def get_status(self):
        return self.status
