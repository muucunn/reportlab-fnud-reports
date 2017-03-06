from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import cache
from settings import RML_DIR

import StringIO
import os

import preppy
from rlextra.rml2pdf import rml2pdf

from fundreport.utils import create_fund_report

Fund = cache.get_model('fundreport', 'Fund')
FundValue = cache.get_model('fundreport', 'FundValue')
IndexValue = cache.get_model('fundreport', 'IndexValue')

class Command(BaseCommand):
    args = '<fund_id fund_id ...>'
    help = 'Please provide a numeric id for the fund for which you want to generate a command'
    
    def handle(self, *args, **kwargs):
        try:
            arg = args[0]
        except:
            raise CommandError('please provide a fund id')
        ids = []

        if args[0] == 'ALL':
            for fund in Fund.objects.all():
                ids.append(fund.id)
        else:
            ids.append(int(arg))


        for id in ids:
            'create files named fund_001.pdf, fund_002.pdf etc in current directory'
            outfilename = 'fund_%03d.pdf' % id
            rawpdf = create_fund_report(id)
            open(outfilename, 'wb').write(rawpdf)
            print 'Created', outfilename
        

