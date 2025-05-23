from django.urls import path
from .views import TicketListCreateView, TicketDetailView, TicketStatusView, GenXLSXView, GetChoices, SendTicketEmailView, DownloadDocument, DownloadManual

urlpatterns = [
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),

    path(
        'tickets/status-update/<int:ticket_id>/',
        TicketStatusView.as_view(),
        name='ticket-status-update'
    ),
    path('tickets/status/<int:ticket_id>/', TicketStatusView.as_view(),
         name='ticket-status-detail'),
    path('tickets/status/', TicketStatusView.as_view(), name='ticket-status-list'),

    path('tickets/choices/', GetChoices.as_view(), name='ticket-status-choices'),

    path('tickets/download-tickets/', GenXLSXView.as_view(),
         name='download-tickets-xlsx'),

    path('tickets/send-email/', SendTicketEmailView.as_view(),
         name='send-email-ticket'),
    path('tickets/download/attachments/critcs_and_suggestions/answer/<str:filename>/',
         DownloadDocument.as_view(), name='download_document'),
    path('manual/',
         DownloadManual.as_view(), name='download_manual'),
]
