import os
import StringIO

import preppy
from rlextra.rml2pdf import rml2pdf

from settings import RML_DIR, WRITE_RML
from models import FundValue, IndexValue, Fund, Theme, Region, AssetClass

def create_fund_report(id):

    """
    Creates PDF as a binary stream in memory, and returns it
    This can then be used to write to disk from management commands or crons,
    or returned to caller via Django views.
    """

    # We call our own templating engine, preppy, and the filename of our template.
    # Most of the layout is driven by this template, and this function serves
    # simply to pass data to this template.
    template_file = preppy.getModule(os.path.join(RML_DIR, 'fundreport.prep'))    
    fund = Fund.objects.get(pk=id)

    # Initialise the context for the PDF template.  The template will need
    # to assemble fonts, images and so on, and we can't make assumptions
    #about current working directory within a web server, so we explicitly
    # work out the RML directory in settings.py and pass this in.
    context = {}
    context['RML_DIR'] = RML_DIR


    # It's generally good to assemble your data before entering the template.
    # Much easier to write and debug Python code in a Python module. Depending
    # on your object model, you may end up putting a lot in the dictionary, or
    # you may just pass in some high level object (e.g. a Fund object) with
    # methods to fetch its own related data.
        
    # Pass the appropriate fund and themes into the template
    context['fund'] = fund
    context['live_themes'] = fund.theme_set.filter(live=True)

    # Build up the appropriate data sets for the line chart and attribution section.
    # Another choice might be to implement a 'get_line_chart_data' method on
    # the Fund class and call it later in the template.
    context['line_chart_data'] = get_line_chart_data(fund.pk)
    context['attribution'] = get_attribution_data(fund.pk)

    # 'Execute' the template to generate an RML document, our mark-up language for laying out PDF
    rml = template_file.getOutput(context)

    # Option to save this intermediate RML file for later investigation.
    # It's worth you reviewing this during development.  Also, if you generate
    # bad RML, the pyRXPU validating parser will raise an exception and tell
    # you the line number; you'll need to look in the file below to see your
    # error.
    if WRITE_RML:
        open(os.path.join(RML_DIR,'latest.rml'), 'w').write(rml)   
    buf = StringIO.StringIO()

    # The magic step, converting the RML to PDF
    rml2pdf.go(rml, outputFileName=buf)

    # Return the PDF for the view to return to the user
    return buf.getvalue()

def get_line_chart_data(id):  
    #We have some fake time series values in the database.
    #Grab these and normalise so that start at 100
    
    fund = Fund.objects.get(pk=id)
    fundData = FundValue.objects.filter(fund=fund).order_by('date')
    indexData = IndexValue.objects.all().order_by('date')
    data1 = []
    data2 = []
    categoryNames = []
    data_scale = fundData[0].value / 100.0
    index_scale = indexData[0].value / 100.0
    for x in range(len(fundData)):
        data1.append((fundData[x].date.strftime('%Y%m%d'),(fundData[x].value / data_scale)))
        data2.append((indexData[x].date.strftime('%Y%m%d'),(indexData[x].value / index_scale)))
    return [data1,data2]

def get_attribution_data(id):
    #more fake data to drive one of the charts.
    AUMSCALE = 10000000.0
    fund = Fund.objects.get(pk=id)
    context = {}
    context['data'] = [[],[]]
    context['lookup'] = [[],[]]
    for r in Region.objects.all():
        context[r.name] = {}
        for ac in AssetClass.objects.all():
            context[r.name][ac.name] = 0
            context[ac.name] = 0
        context[r.name]['total'] = 0
        context['lookup'][0].append(r.name)
    for ac in AssetClass.objects.all():
        context['lookup'][1].append(ac.name)
    for ft in Theme.objects.filter(fund=fund).order_by("position__LTD"):
        context['data'][0].append(ft.name)
        context['data'][1].append(ft.position.LTD/AUMSCALE)
        context[ft.region.name][ft.asset_class.name] += ft.position.LTD / AUMSCALE
        context[ft.region.name]['total'] += ft.position.LTD / AUMSCALE
        context[ft.asset_class.name] += ft.position.LTD / AUMSCALE
    return context
