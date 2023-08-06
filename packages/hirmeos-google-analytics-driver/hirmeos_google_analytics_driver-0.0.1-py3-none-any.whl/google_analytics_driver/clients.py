"""HIRMEOS client that has been modified, specifically for requests
associated with the Google Analytics driver.
"""

from dataclasses import dataclass, field

from hirmeos_clients import TranslatorClient

from .logic import standardise_row, sanitise_url, normalise_url, convert_url


@dataclass
class GAClient:

    translator: TranslatorClient = field(repr=False)
    uri_scheme: str
    uri_strict: bool = field(default=False)
    country_uri_scheme: str = field(default='')

    def standardise_country(self, country):
        if self.country_uri_scheme:
            country = f'{self.country_uri_scheme}:{country}'
        return country

    def uri_to_ids(self, uri):
        return self.translator.uri_to_id(uri, self.uri_scheme, self.uri_strict)

    def resolve_report(self, timestamp, prefix, regexes, cached_row):
        """Provide a non-aggregated measure for all identifiers that match
        URLs from GA report via the translation API.

        Args:
            timestamp (str): datetime associated with the record.
            prefix (str): Prepend to path identified by GA to create a URL.
            regexes (list): Regular expressions to match against the URLs.
            cached_row (list): Single row from cached GA CSV.

        Yields:
            tuple: Raw GA measure for an identifier matched against the URL.
        """
        path, country_code, value = standardise_row(cached_row)
        url = sanitise_url(
            normalise_url(
                convert_url(path),
                prefix
            ),
            regexes
        )

        country = ''
        if country_code != 'ZZ':  # no country data available
            country = self.standardise_country(country_code)

        for identifier in self.uri_to_ids(url):
            yield (timestamp, identifier['URI'], country, value)
