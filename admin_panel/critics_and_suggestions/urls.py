from django.urls import path
from .views import TicketViewSet, TicketStatusViewSet, TicketAnalysisHistoryViewSet

urlpatterns = [
    path('', TicketViewSet.as_view({'get': 'list', 'post': 'create'}), name='ticket-list'),
    path('<int:pk>/', TicketViewSet.as_view({'get': 'retrieve'}), name='ticket-detail'),

    path('status-update/<int:ticket_id>/', TicketStatusViewSet.as_view({'patch': 'update', 'get': 'retrieve'}), name='ticket-status'),
    path('status/', TicketStatusViewSet.as_view({'get': 'list'}), name='ticket-status-list'),
    
    path('ticket-analysis-history/', TicketAnalysisHistoryViewSet.as_view({'get': 'list'}), name='ticket-analysis-history-list'),
    path('ticket-analysis-history/<int:pk>/', TicketAnalysisHistoryViewSet.as_view({'get': 'retrieve'}), name='ticket-analysis-history-detail'),
]
