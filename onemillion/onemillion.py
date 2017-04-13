#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Determine if domain is in Alexa or Cisco top one million domain list."""

import csv
import datetime
import json
import os
try:
    from StringIO import StringIO as ZipIO
except:
    from io import BytesIO as ZipIO
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
DEFAULT_CACHE_LOCATION = '~/.onemillion'


def get_current_etag(domain_list_url):
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


class OneMillion(object):
    """Find if a given domain is in the top one million domain list."""

    def __init__(self, cache=True, cache_location=DEFAULT_CACHE_LOCATION,
                 update=True):
        self.cache = cache
        self.cache_location = os.path.expanduser(cache_location)
        self.update = update
        self.first_time = False

        # if cache location does not exist, create it and metadata file
        if not os.path.exists(self.cache_location):
            # create the directory in the specified cache_location
            os.makedirs(self.cache_location)
            # create the metadata.json file
            open(os.path.join(self.cache_location, 'metadata.json'), 'a').close()
            self.first_time = True

        self.update_lists()

    def _get_metadata(self):
        """Read the metadata from the metadata file."""
        metadata = None

        # return None if this is the first pass
        if self.first_time:
            self.first_time = False
            return metadata
        # try to read the metadata
        else:
            with open(os.path.join(self.cache_location, 'metadata.json'), 'r') as f:
                metadata = json.load(f)

        return metadata

    def _update_domain_list(self, domain_list):
        """Update the given domain list."""
        try:
            response = requests.get(domain_list['url'])
        except Exception as e:
            # TODO: consider adding logging here
            raise e
        else:
            # read the data from the zip file
            zip_file = zipfile.ZipFile(ZipIO(response.content))
            data = zip_file.read('top-1m.csv')

            # write the data into the cache_location
            with open(os.path.join(self.cache_location,
                                   domain_list['output_file_path']),
                      'w+') as f:
                f.write(data.decode("utf-8"))

    def _update_etag(self, domain_list_name, etag):
        """Update the etag for a domain list."""
        if self.metadata is None:
            self.metadata = dict()

        # update the etag
        self.metadata[domain_list_name + ' etag'] = etag

        # update the datestamp
        self.metadata['last_updated'] = str(datetime.date.today())

        # write the updated metadata
        with open(os.path.join(self.cache_location, 'metadata.json'), 'w') as f:
            f.write(json.dumps(self.metadata))

    def _check_for_updates(self):
        """Check to see if lists need updated and update if needed."""
        # get the metadata
        self.metadata = self._get_metadata()
        
        # if the metadata is empty, initialize it
        if self.metadata is None:
            self.metadata = dict()

        # if the top domain list was already updated today, skip the update and move on
        if self.metadata.get('last_updated') == str(datetime.date.today()):
            return

        # check each of the lists to see if they need to be updated
        for domain_list in CONFIG['domain_lists']:
            previous_etag = self.metadata.get(domain_list['name'] + ' etag')
            current_etag = get_current_etag(domain_list['url'])

            # if the domain list needs to be updated...
            if previous_etag != current_etag:
                # update the domain list
                self._update_domain_list(domain_list)
                # update the etag for this list (and the datestamp)
                self._update_etag(domain_list['name'], current_etag)
                # TODO: add logging here
            else:
                # TODO: add logging here
                pass

    def domain_in_million(self, domain):
        """Check if the given domain is in a top on million list."""
        # TODO: parse the registered domain out of the given domain using tldextract
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

    def update_lists(self):
        """Update the lists if appropriate."""
        # if we are caching and updating...
        if self.cache and self.update:
            # cache/update the lists
            self._check_for_updates()
        # if we are caching but not updating and this is the first pass...
        elif self.cache and not self.update and self.first_time:
            # cache the contents of the lists as this is the first pass
            self._check_for_updates()
        # if instructions given to onemillion are contrary, raise error message
        elif self.update and not self.cache:
            raise ValueError("It is not possible to update the top one " +
                             "million domain lists without caching them. " +
                             "This script will use the most updated version " +
                             "of the domain lists by default if cache is " +
                             "set to True.")
