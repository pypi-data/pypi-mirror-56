# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Dashboard, MenuSettings, ModelDescription
)


class DashboardCreateView(CreateView):

    model = Dashboard
    fields = ()
    template_name = 'vadmin/base.html'


# class OrderDeleteView(DeleteView):

#     model = Order


# class OrderDetailView(DetailView):

#     model = Order


# class OrderUpdateView(UpdateView):

#     model = Order


# class OrderListView(ListView):

#     model = Order
