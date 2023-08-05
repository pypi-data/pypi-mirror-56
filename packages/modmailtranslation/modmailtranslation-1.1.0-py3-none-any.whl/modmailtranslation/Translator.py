import asyncio
import json

import aiohttp

from modmailtranslation.errors.KeyNotFoundError import KeyNotFoundError

loop = asyncio.get_event_loop()


class Translator:
    """
    The heart of the  package.
    """

    def __init__(self, language_file_url: str, default_language: str = None):
        """
        Construct a new Translator object

        :param language_file_url: The raw github link of the language file.
        :param default_language: Optional - If you want to set a default language
        """
        self.language_file_url = language_file_url
        self.default_language = default_language
        self._language_file_data = None
        self.session = aiohttp.ClientSession()
        loop.run_until_complete(self._request_file())

    async def _request_file(self):
        async with self.session as session:
            await self._request_file_raw(session)

    async def _request_file_raw(self, session):
        async with session.get(self.language_file_url) as resp:
            try:
                data = await resp.read()
                self._language_file_data = json.loads(data)
            except Exception as e:
                print(f"An error occurred while fetching language data from {self.language_file_url} - {e}")

            return

    def set_default_language(self, language: str):
        """
        Set the default language to respond in.
        Returns True if language is updated and False if the language is not present in the file.

        :param language: The keyword of the language
        :return: bool
        """
        if language not in self._language_file_data["languages"]:
            return False
        else:
            self.default_language = language
            return True

    async def update_language(self):
        """
        Update the language file from the url

        :return:
        """
        await self._request_file()
        return

    def get_languages(self):
        """
        Retrieve all supported languages

        :return:
        """
        return self._language_file_data["languages"]

    def get(self, key, language=None):
        """
        Get the language string from the language file.

        :param key: The key name
        :param language: Optional - The language to fetch the key from. (defaults to default language if set or en-US)
        :return:
        :raises: KeyNotFoundError: if the key was not found in the language
        """
        if language is None:
            if self.default_language is not None:
                language = self.default_language
            else:
                language = "en-US"

        try:
            return self._language_file_data[language][key]
        except KeyError:
            if self.default_language is not None and language != self.default_language:
                try:
                    return self._language_file_data[self.default_language][key]
                except KeyError:
                    raise KeyNotFoundError(language, key)
            else:
                raise KeyNotFoundError(language, key)
