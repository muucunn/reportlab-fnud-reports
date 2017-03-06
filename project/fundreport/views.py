import os

from django.http import HttpResponse
from django.shortcuts import render

from models import Rationale, Fund, Theme

from fundreport.utils import create_fund_report

def index(request):
    context = {}
    context['funds'] = Fund.objects.all()
    return render(request, 'index.html', context)
   
def fundreport(request,id):
    # Create a PDF for the fund and return as HTTP Response
    
    # All the work is done in a separate function, so we can
    # call it from background commands as well as web requests.
    pdf = create_fund_report(id)
    
    response = HttpResponse(pdf, content_type="application/pdf")
    
    #note that 'inline' will bring up the PDF in a browser tab in most
    #modern browsers; changing this to 'attachment' will prompt it to
    #be downloaded to the desktop.  The choice is yours.
    response['Content-Disposition'] = 'inline; filename="fund_report.pdf"'
    return response


