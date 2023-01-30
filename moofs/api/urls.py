from django.contrib import admin
from django.urls import path

from .views import (
    moof_action_view,
    moof_delete_view,
    moof_detail_view,
    moof_feed_view,
    moof_list_view,
    moof_create_view
)

'''
CLIENT
Base ENDPOINT /api/moofs/
'''

urlpatterns = [
    path('', moof_list_view),
    path('feed/', moof_feed_view),
    path('action/', moof_action_view),
    path('create/', moof_create_view),
    path('<int:moof_id>/', moof_detail_view),
    path('<int:moof_id>/delete/', moof_delete_view),
]
