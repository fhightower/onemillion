#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Determine if domain is in Alexa or Cisco top one million domain list."""

import csv
import json
import os
import StringIO
import zipfile

import requests

CONFIG = {
    'domain_lists': [
        {
            'name': "alexa",
            'output_file_path': "alexa.csv",
            'url': "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
        }, {
            'name': "cisco umbrella",
            'output_file_path': "cisco.csv",
            'url': "http://s3-us-west-1.amazonaws.com/umbrella-static/" +
                   "top-1m.csv.zip"
        }
    ]
}
DEFAULT_CACHE_LOCATION = '~/.one_million'


class OneMillion(object):
    """Find if a given domain is in the top one million domain list."""

    def __init__(self, cache=True, cache_location=DEFAULT_CACHE_LOCATION,
                 update=True):
        self.cache = cache
        self.cache_location = os.path.expanduser(cache_location)
        self.update = update
        self.first_time = False

        if not os.path.exists(self.cache_location):
            os.makedirs(self.cache_location)
            open(os.path.join(self.cache_location, 'metadata.json'), 'a').close()
            self.first_time = True

        if self.update and not self.cache:
            raise ValueError("It is not possible to update the top one " +
                             "million domain lists without caching them. " +
                             "This script will use the most updated version " +
                             "of the domain lists by default if cache is " +
                             "set to True.")

    # # TODO: update this function appropriately
    # def __call__(self, domain):
    #     self.one_million(domain)

    def _get_metadata(self):
        """Read the metadata from the metadata file."""
        metadata = None

        if self.first_time:
            self.first_time = False
            return metadata
        else:
            with open(os.path.join(self.cache_location, 'metadata.json'), 'r') as f:
                try:
                    metadata = json.load(f)
                # this exception occurs on first pass if no metadata is recorded
                except ValueError:
                    pass

        return metadata

    def _get_previous_etag(self, domain_list_name):
        """Get the previous etag for a given domain list."""
        previous_etag = None
        metadata = self._get_metadata()

        if metadata is not None:
            try:
                # get the previous etag as stored in the metadata json
                previous_etag = metadata[domain_list_name + ' etag']
            # this exception occurs on the first pass after the first domain list has been recorded in metadata.json, but the second one does not exist
            except KeyError:
                pass

        return previous_etag

    def _get_current_etag(self, domain_list_url):
        """Get the current etag for a given domain list."""
        current_etag = None

        try:
            results = requests.head(domain_list_url)
        except Exception as e:
            # TODO: consider adding logging here
            raise e
        else:
            current_etag = results.headers.get('etag')

        return current_etag

    def _update_domain_list(self, domain_list):
        """Update the given domain list."""
        try:
            response = requests.get(domain_list['url'])
        except Exception as e:
            # TODO: consider adding logging here
            raise e
        else:
            zip_file = zipfile.ZipFile(StringIO.StringIO(response.content))
            data = zip_file.read('top-1m.csv')

            with open(os.path.join(self.cache_location, domain_list['output_file_path']), 'w+') as f:
                f.write(data)

    def _update_etag(self, domain_list_name, etag):
        """Update the etag for a domain list."""
        # get the current metadata
        metadata = self._get_metadata()

        if metadata is None:
            metadata = dict()

        # update the etag
        metadata[domain_list_name + ' etag'] = etag

        # write the updated metadata
        with open(os.path.join(self.cache_location, 'metadata.json'), 'w') as f:
            f.write(json.dumps(metadata))

    def _update_lists(self):
        """Update the top one million lists."""
        for domain_list in CONFIG['domain_lists']:
            previous_etag = self._get_previous_etag(domain_list['name'])
            current_etag = self._get_current_etag(domain_list['url'])

            # if the domain list has been updated since the last pass...
            if previous_etag != current_etag:
                # update the domain list
                self._update_domain_list(domain_list)
                self._update_etag(domain_list['name'], current_etag)
                # TODO: add logging here
                # print("Updated {} domain list".format(domain_list['name']))
            # if the domain list has not been updated...
            else:
                # TODO: add logging here
                # print("The {} domain list has ".format(domain_list['name']) +
                      # "not changed since the last run")
                pass

    def domain_in_million(self, domain):
        """Check if the given domain is in a top on million list."""
        # TODO: parse the registered domain out of the given domain using tldextract
        if self.update:
            self._update_lists()

        # see if the given domain is in the up-to-date domain lists
        for domain_list in CONFIG['domain_lists']:
            # open the domain list as a CSV
            with open(os.path.join(self.cache_location, domain_list['output_file_path']), 'r') as domain_csv:
                domain_reader = csv.reader(domain_csv)
                for row in domain_reader:
                    # if the domain is in the given list, return true
                    if row[1] == domain:
                        return True

        # if the domain was not found in the list, return false
        return False
