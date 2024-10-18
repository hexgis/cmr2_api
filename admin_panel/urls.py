from django.urls import path, include

from admin_panel import views

urlpatterns = [
    path('usuarios/instituicao/', views.UsersInstitutionsView.as_view(), name='Users institutions'),
    path('instituicao/', views.InstitutionsView.as_view(), name='institutions-list-create'),
    path('instituicao/<int:id>/', views.InstitutionsView.as_view(), name='institutions-detail'),
    path('tickets/', include('admin_panel.critics_and_suggestions.urls'))

]
