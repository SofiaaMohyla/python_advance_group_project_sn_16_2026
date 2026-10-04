from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Advertisement


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'advertisements/list.html'
    context_object_name = 'advertisements'
    ordering = ['-created_at']


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    template_name = 'advertisements/create.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('advertisement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdvertisementUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Advertisement
    template_name = 'advertisements/edit.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('advertisement_list')

    def test_func(self):
        advertisement = self.get_object()
        return (
            self.request.user.is_staff
            or self.request.user.groups.filter(
                name='Moderators'
            ).exists()
            or self.request.user == advertisement.author  # <-- Додано перевірку автора
        )


class AdvertisementDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Advertisement
    template_name = 'advertisements/delete.html'
    success_url = reverse_lazy('advertisement_list')

    def test_func(self):
        advertisement = self.get_object()
        return (
            self.request.user.is_staff
            or self.request.user.groups.filter(
                name='Moderators'
            ).exists()
            or self.request.user == advertisement.author  # <-- Додано перевірку автора
        )