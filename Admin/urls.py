from django.contrib import admin
from django.urls import path
from myadmin import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginView, name='loginView'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    path('service-provider/', views.service_provider, name='service-provider'),
    path('add-invoice/', views.add_invoice, name='add-invoice'),
    path('add-services/', views.add_services, name='add-services'),
    path('report/', views.report, name='report'),  # Adjust the view function name as needed
    path('generate-pdf/', views.generate_pdf, name='generate-pdf'),
    path('review-invoice/',views.review_invoice,name='review-invoice'),
    path('generate-pdf-review/', views.generate_pdf_review, name='generate-pdf-review'),
    path('generate-pdf-report/', views.generate_pdf_report, name='generate-pdf-report'),

    # ... other URLs ...
]
