from http import client
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import ClientForm,ServiceProviderForm,  ServicesForm,  UserLogin

from .models import Services, Client ,Company # Import the Client model

from .forms import ClientForm, ServicesForm, ServiceProviderForm


def loginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserLogin(request=request, data=request.POST)
            
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']  # Corrected 'passwaord' to 'password'
                userOBJ = authenticate(username=uname, password=upass)
                
                if userOBJ is not None:
                    login(request, userOBJ)
                    return HttpResponseRedirect('/dashboard/')  # Use HttpResponseRedirect to redirect

        else:
            fm = UserLogin()
        return render(request, 'login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/dashboard/')  # Use HttpResponseRedirect to redirect

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')  # Redirect to the login page

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return HttpResponseRedirect('/')  # Redirect to the login page
    
    
######################################################################################################################################################################################    

def add_invoice(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            clientFm = ClientForm(request.POST)
            if clientFm.is_valid():
                comp = clientFm.cleaned_data['company_name']
                gst = clientFm.cleaned_data['gst_number']
                cntry = clientFm.cleaned_data['country']
                sts = clientFm.cleaned_data['state']
                add = clientFm.cleaned_data['address']
          
                obj = Client(company_name=comp, gst_number=gst, country=cntry, state=sts, address=add)
                obj.save()
                 # Generate the report data for the added client
              
                
                messages.success(
                    request, "Your 'Client' form has been saved successfully"
                )
            return redirect('add-invoice')
                
        else:
            clientFm = ClientForm()  
        return render(request, 'add_invoice.html', {'clientFm': clientFm ,})
    
def review_invoice(request):
    clients = Client.objects.all()  # Retrieve all clients for generating the report
    return render(request, 'review_invoice.html', {'clients': clients})
######################################################################################################################################################################################  

def add_services(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            addservicesfm = ServicesForm(request.POST)
            if addservicesfm.is_valid():
                client = addservicesfm.cleaned_data['client']
                description = addservicesfm.cleaned_data['description']
                quantity = addservicesfm.cleaned_data['quantity']
                amount = addservicesfm.cleaned_data['amount']

                # Create a new Service object and save it to the database
                obj = Services(
                    client=client,
                    description=description,
                    quantity=quantity,
                    amount=amount
                )
                # Process the form data and save to the database
                obj.save()
                
                messages.success(
                    request, "Your 'Service Invoice' form has been saved successfully"
                )
                
                return redirect('add-services')  # Redirect to the review_invoice view

        else:
            addservicesfm = ServicesForm()
            
        # Retrieve existing invoices for review
        
        return render(request, 'add_services.html', {'form': addservicesfm})
    
    from django.shortcuts import render
from .models import Services  # Import your model here

def report(request):
    # Retrieve all services from the database
    services = Services.objects.all()

    return render(request, 'report.html', {'services': services})


######################################################################################################################################################################################

def service_provider(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Servicefm = ServiceProviderForm(request.POST)
            if Servicefm.is_valid():
                  # Access cleaned data from each field
                client = Servicefm.cleaned_data['client']
                company_name = Servicefm.cleaned_data['company_name']
                handle_by = Servicefm.cleaned_data['handle_by']
                email = Servicefm.cleaned_data['email']
                phone = Servicefm.cleaned_data['phone']
                account_number = Servicefm.cleaned_data['account_number']
                ifsc_code = Servicefm.cleaned_data['ifsc_code']
                bank_name = Servicefm.cleaned_data['bank_name']
                gst_number = Servicefm.cleaned_data['gst_number']
                
               
                obj=Company(client=client,company_name=company_name,handle_by=handle_by,email=email,phone=phone,account_number=account_number,ifsc_code=ifsc_code,bank_name=bank_name,gst_number=gst_number)
                
                # Process the form data and save to the database
                obj.save()
                messages.success(
                    request, "Your 'Service Provider' form has been saved successfully"
                )
                companies = Company.objects.all()

                return render(request, 'service_provider.html', {'form': Servicefm, 'companies': companies})

        else:
            Servicefm = ServiceProviderForm()

        companies = Company.objects.all()

        return render(request, 'service_provider.html', {'form': Servicefm, 'companies': companies})


############################################################################################################################################


  




############################################################################################################################################

from django.template.loader import get_template
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bill_report.pdf"'

    companies = Company.objects.all()  # Fetch your company data here

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Create a list of data to populate the table
    data = [['Company Name', 'Handle By', 'Phone', 'Client']]

    for company in companies:
        data.append([
            company.company_name,
            company.handle_by,
            company.phone,
            company.client
        ])


    # Create the table and style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add the table to the PDF document
    elements = [table]
    doc.build(elements)
    
    return response

###############################################################################################################################################################
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Client  # Import the Client model

def generate_pdf_review(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="client_report.pdf"'

    # Get data from the database (Client model)
    clients = Client.objects.all()

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Create a list of data to populate the table
    data = [['Company Name', 'GST Number', 'Country', 'State', 'Address']]
    for client in clients:
        data.append([client.company_name, client.gst_number, client.country, client.state, client.address])

    # Create the table and style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add the table to the PDF document
    elements = [table]
    doc.build(elements)

    return response

######################################################################################################################################################################################
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Services  # Import your Service model

def generate_pdf_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="service_report.pdf"'

    # Get data from the database (Service model)
    services = Services.objects.all()

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Create a list of data to populate the table
    data = [['Client', 'Description', 'Quantity', 'Amount']]
    for service in services:
        data.append([service.client, service.description, service.quantity, service.amount])

    # Create the table and style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add the table to the PDF document
    elements = [table]
    doc.build(elements)

    return response
