from django.urls import path
from .views import IssueListView
from .views import issue_stats

urlpatterns = [
    path('issues/', IssueListView.as_view(), name='issue-list'),
    path('stats/', issue_stats, name='issue-stats'),
]