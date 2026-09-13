from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from events.models import Event
from django.urls import reverse_lazy, reverse
from events.forms import EventForm

class EventListView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'events/list.html'


class EventCreateView(CreateView):
    form_class = EventForm
    template_name = 'events/form.html'
    model = Event
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    success_url =reverse_lazy("event-list")


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'event/detail.html'


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/delete.html'
    success_url = reverse_lazy("event-list")