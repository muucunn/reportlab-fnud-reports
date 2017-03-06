from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

import os

from fundreport.models import Fund


class FundReportTestCases(TestCase):
    
    def test_demo(self):
        self.assertEqual(2+2, 4, 'something is up')

    def test_web_report(self):
        "Check the URL creates a PDF"
        response = self.client.get('/fundreport/1.pdf')
        self.assertEqual(response.status_code, 200)
        startOfFile = response.content[0:8]
        self.assertEqual(startOfFile, '%PDF-1.4', 'unexpected content in response: %s' % startOfFile)

    def test_command_tier1report(self):
        "Check our command creates the file in the current directory"
        from django.core.management import call_command

        basepath = os.path.dirname(__file__)
        filepath = os.path.abspath(os.path.join(basepath, "..", "fund_001.pdf"))
        if os.path.isfile(filepath):
            os.remove(filepath)
        call_command('makepdf', 1)
        f = open(filepath, "r")
        self.assertEqual(f.readline()[0:8], '%PDF-1.4')
        
