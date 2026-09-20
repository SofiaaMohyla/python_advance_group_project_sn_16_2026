from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comment, MediaItem
from .forms import CommentForm, MediaItemForm


class MediaItemListView(LoginRequiredMixin, ListView):
    model = MediaItem
    template_name = 'media_item_list.html'
    context_object_name = 'media_items'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MediaItemForm()
        return context

    def get_queryset(self):
        return MediaItem.objects.select_related('uploaded_by').order_by('-created_at')
        

class MediaItemCreateView(LoginRequiredMixin, CreateView):
    model = MediaItem
    form_class = MediaItemForm
    template_name = 'media_item_form.html'
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('media_item_list')

class MediaItemDetailView(LoginRequiredMixin, DetailView):
    model = MediaItem
    template_name = 'media_item_detail.html'

    def get_queryset(self):
        return MediaItem.objects.select_related('uploaded_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(media_item=self.object)
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.media_item = MediaItem.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('media_item_detail', kwargs={'pk': self.kwargs['pk']})

class MediaItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MediaItem
    form_class = MediaItemForm
    template_name = 'media_item_form.html'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('media_item_list')

    def get_queryset(self):
        return MediaItem.objects.filter(uploaded_by=self.request.user)


class MediaItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MediaItem
    template_name = 'media_item_confirm_delete.html'
    success_url = reverse_lazy('media_item_list')

    def test_func(self):
        media_item = self.get_object()
        return (
            media_item.uploaded_by == self.request.user
            or self.request.user.role == 'admin'
            or self.request.user.is_staff
        )

    def form_valid(self, form):
        file = self.object.file
        response = super().form_valid(form)
        file.delete(save=False)
        return response

