import re
import os
import json
import unittest

import pytest
import requests
from constants import ASSETS_PATH, CRAWLER_CONFIG_PATH

class RawBasicDataValidator(unittest.TestCase):
    def setUp(self) -> None:
        # open and prepare texts
        self.texts = []
        for file_name in os.listdir(ASSETS_PATH):
            if file_name.endswith("_raw.txt"):
                with open(os.path.join(ASSETS_PATH, file_name), encoding='utf-8') as f:
                    file = f.read()
                    print(file_name)
                    self.texts.append((int(file_name.split('_')[0]), file))
        self.texts = tuple(self.texts)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_validate_sort(self):
        list_ids = [pair[0] for pair in self.texts]
        for i in range(1, len(list_ids)+1):
            self.assertTrue(i in list_ids,
                            msg="""Articles ids are not homogeneous. E.g. numbers are not from 1 to N""")

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_texts_are_not_empty(self):
        for file_name in self.texts:
            self.assertTrue(len(file_name[1]) > 50,
                            msg="""Text with ID: {} seems to be empty (less than 50 characters).
                            Check if you collected article correctly""".format(file_name[0]))


class RawMediumDataValidator(unittest.TestCase):
    def setUp(self) -> None:
        # check metadata is created under ./tmp/articles directory
        error_message = """Articles were not created in the ./tmp/articles directory after running scrapper.py
                                        Check where you create articles"""
        self.assertTrue(os.path.exists(ASSETS_PATH), msg=error_message)

        # open and prepare metadata
        self.metadata = []
        for file_name in os.listdir(ASSETS_PATH):
            if file_name.endswith(".json"):
                with open(os.path.join(ASSETS_PATH, file_name), encoding='utf-8') as f:
                    config = json.load(f)
                    self.metadata.append((config['id'], config))
        self.metadata = tuple(self.metadata)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_match_requested_volume_sample(self):
        metas, raws = 0, 0
        for file in os.listdir(ASSETS_PATH):
            if file.endswith("_raw.txt"):
                raws += 1
            if file.endswith("_meta.json"):
                metas += 1
        self.assertEqual(metas, raws, msg="""Resulted number of meta.json files is not equal 
        to num_articles param specified in config - not in range(2, 8)""")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_validate_sort(self):
        list_ids = [pair[0] for pair in self.metadata]
        for i in range(1, len(list_ids)+1):
            self.assertTrue(i in list_ids,
                            msg="""Articles ids are not homogeneous. E.g. numbers are not from 1 to N""")

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_validate_metadata(self):
        # can i open this URL?
        for metadata in self.metadata:
            if metadata[1]['url'].endswith(".pdf"):  # skip monolithic metadata checks
                continue
            self.assertTrue(requests.get(metadata[1]['url']),
                            msg="Can not open URL: <{}>. Check how you collect URLs".format(
                                metadata[1]['url']))

            html_source = requests.get(metadata[1]['url']).text

            print(metadata[1]['title'])
            self.assertTrue(metadata[1]['title'] in
                            html_source,
                            msg="""Title is not found by specified in metadata URL <{}>.
                            Check how you collect titles""".format(metadata[1]['url']))

            # author is presented? NOT FOUND otherwise?
            try:
                self.assertTrue(metadata[1]['author'] in html_source)
            except AssertionError:
                self.assertEqual(metadata[1]['author'], 'NOT FOUND',
                                 msg="""Author field <{}> (url <{}>) is incorrect. 
                                        Collect author from the page or specify it with special keyword <NOT FOUND> 
                                        if it is not presented at the page.""".format(
                                     metadata[1]['author'], metadata[1]['url']))

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_texts_are_not_empty(self):
        for file_name in os.listdir(ASSETS_PATH):
            if file_name.endswith("_raw.txt"):
                with open(os.path.join(ASSETS_PATH, file_name), encoding='utf-8') as f:
                    self.assertTrue(len(f.read()) > 50,
                                    msg="""File {} seems to be empty (less than 50 characters).
                                     Check if you collected article correctly""".format(file_name))


class RawAdvancedDataValidator(unittest.TestCase):
    def setUp(self) -> None:
        # check metadata is created under ./tmp/articles directory
        error_message = """Articles were not created in the ./tmp/articles directory after running scrapper.py
                                        Check where you create articles"""
        self.assertTrue(os.path.exists(ASSETS_PATH), msg=error_message)

        # datetime pattern
        self.data_pattern = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"

        # open and prepare metadata
        self.metadata = []
        for file_name in os.listdir(ASSETS_PATH):
            if file_name.endswith(".json"):
                with open(os.path.join(ASSETS_PATH, file_name), encoding='utf-8') as f:
                    config = json.load(f)
                    self.metadata.append((config['id'], config))
        self.metadata = tuple(self.metadata)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_match_requested_volume_sample(self):
        metas, raws = 0, 0
        for file in os.listdir(ASSETS_PATH):
            if file.endswith("_raw.txt"):
                raws += 1
            if file.endswith("_meta.json"):
                metas += 1
        self.assertEqual(metas, raws, msg="""Resulted number of meta.json files is not equal 
        to num_articles param specified in config - not in range(2, 8)""")

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_validate_sort(self):
        list_ids = [pair[0] for pair in self.metadata]
        for i in range(1, len(list_ids)+1):
            self.assertTrue(i in list_ids,
                            msg="""Articles ids are not homogeneous. E.g. numbers are not from 1 to N""")

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_validate_metadata(self):
        # can i open this URL?
        for metadata in self.metadata:
            if metadata[1]['url'].endswith(".pdf"):  # skip monolithic metadata checks
                continue
            self.assertTrue(requests.get(metadata[1]['url']),
                            msg="Can not open URL: <{}>. Check how you collect URLs".format(
                                metadata[1]['url']))

            html_source = requests.get(metadata[1]['url']).text

            self.assertTrue(metadata[1]['title'] in
                            html_source,
                            msg="""Title is not found by specified in metadata URL <{}>.
                            Check how you collect titles""".format(metadata[1]['url']))

            # is a date in given format?
            self.assertTrue(re.search(self.data_pattern, metadata[1]['date']),
                            msg="""Date <{}> do not match given format <{}> (url <{}>). 
                            Check how you write dates.""".format(
                                metadata[1]['date'], self.data_pattern, metadata[1]['url']))

            # author is presented? NOT FOUND otherwise?
            try:
                self.assertTrue(metadata[1]['author'] in html_source)
            except AssertionError:
                self.assertEqual(metadata[1]['author'], 'NOT FOUND',
                                 msg="""Author field <{}> (url <{}>) is incorrect. 
                                        Collect author from the page or specify it with special keyword <NOT FOUND> 
                                        if it is not presented at the page.""".format(
                                     metadata[1]['author'], metadata[1]['url']))

            topics = metadata[1]['topics']
            if topics is not []:
                for topic in topics:
                    self.assertTrue(topic in html_source,
                                    msg="""Topics <{}> (topic <{}>) for url <{}> are not found.
                                    Check how you create topics.""".format(
                                        metadata[1]['topics'], topic, metadata[1]['url']))

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_5_dataset_validation
    def test_texts_are_not_empty(self):
        for file_name in os.listdir(ASSETS_PATH):
            if file_name.endswith("_raw.txt"):
                with open(os.path.join(ASSETS_PATH, file_name), encoding='utf-8') as f:
                    self.assertTrue(len(f.read()) > 50,
                                    msg="""File {} seems to be empty (less than 50 characters).
                                     Check if you collected article correctly""".format(file_name))


if __name__ == "__main__":
    unittest.main()
