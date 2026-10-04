from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from events.models import Event
from django.urls import reverse_lazy, reverse
from events.forms import EventForm, EventFilterForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    events = Event.objects.all().order_by('-created_at')
    paginator = Paginator(events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events/list.html', {'events': events, 'page_obj': page_obj})

class EventListView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = 'events/list.html'
    paginate_by = 3


    def get_context_data(self, *, object_list=...,  **kwargs):
        context = super().get_context_data()
        context['filter_form'] = EventFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = EventFilterForm(self.request.GET)

        if self.filter_form.is_valid():
            type = self.filter_form.cleaned_data['type']
            if type:
                queryset = queryset.filter(type=type)

        return queryset


class EventCreateView(LoginRequiredMixin, CreateView):
    form_class = EventForm
    template_name = 'events/form.html'
    model = Event
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/form.html'
    success_url =reverse_lazy("event-list")

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.creator or self.request.user.role in ['moderator', 'admin']


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'events/detail.html'


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/delete.html'
    success_url = reverse_lazy("event-list")

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.creator or self.request.user.role in ['moderator', 'admin']