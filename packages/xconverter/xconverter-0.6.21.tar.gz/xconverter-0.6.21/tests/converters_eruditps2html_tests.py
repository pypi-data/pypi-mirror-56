import unittest
import os
import io

from lxml import etree

from converter import converters

APP_PATH = os.path.dirname(os.path.realpath(__file__))


class TestEruditPS2HTML(unittest.TestCase):

    def setUp(self):

        self.conv = converters.EruditPS2HTML(
            source=APP_PATH + '/fixtures/eruditps/document_eruditps.xml'
        )

    def test_load_templates_base_templates(self):

        result = self.conv._prepare_templates(custom_templates=None)

        expected = [
            'static/templates/default/pagedmedia.css',
            'static/templates/default/style.css'
        ]

        self.assertEqual(result, expected)

    def test_load_templates_clean_one_column(self):

        custom_templates = [
            'clean-one-column'
        ]

        result = self.conv._prepare_templates(custom_templates=custom_templates)

        expected = [
            'static/templates/clean-one-column/pagedmedia.css',
            'static/templates/default/style.css',
            'static/templates/clean-one-column/style.css'
        ]

        self.assertEqual(result, expected)

    def test_load_templates_documentation(self):

        custom_templates = [
            'documentation'
        ]

        result = self.conv._prepare_templates(custom_templates=custom_templates)

        expected = [
            'static/templates/default/pagedmedia.css',
            'static/templates/default/style.css',
            'static/templates/documentation/style.css'
        ]

        self.assertEqual(result, expected)
