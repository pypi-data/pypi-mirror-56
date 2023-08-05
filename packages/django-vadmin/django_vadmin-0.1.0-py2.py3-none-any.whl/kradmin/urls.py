# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'kradmin'
# Use ~ to identify actions
urlpatterns = [
    path("dashboard/~create/",
         views.DashboardCreateView.as_view(),
         name='dashboard_create',
         ),
    #     url(
    #         regex="^Order/(?P<pk>\d+)/~delete/$",
    #         view=views.OrderDeleteView.as_view(),
    #         name='Order_delete',
    #     ),
    #     url(
    #         regex="^Order/(?P<pk>\d+)/$",
    #         view=views.OrderDetailView.as_view(),
    #         name='Order_detail',
    #     ),
    #     url(
    #         regex="^Order/(?P<pk>\d+)/~update/$",
    #         view=views.OrderUpdateView.as_view(),
    #         name='Order_update',
    #     ),
    #     url(
    #         regex="^Order/$",
    #         view=views.OrderListView.as_view(),
    #         name='Order_list',
    #     ),
]
