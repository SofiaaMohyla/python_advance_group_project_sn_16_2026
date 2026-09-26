from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from portfolio.forms import PortfolioForm, CommentsForm
from portfolio.models import Portfolio, Comments
# Create your views here.

class PortfListView(ListView):
    model = Portfolio
    template_name = 'portfolio/list.html'
    context_object_name = 'portfolios'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.filter(user=self.request.user)
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'Newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'Oldest':
            queryset = queryset.order_by('created_at')
        return queryset


class PortfCreateView(CreateView):
    form_class = PortfolioForm
    template_name = 'portfolio/form.html'
    model = Portfolio
    success_url = reverse_lazy('portfolio-list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
       
class PortfUpdateView(UpdateView):
    form_class = PortfolioForm
    template_name = 'portfolio/form.html'
    model = Portfolio
    success_url = reverse_lazy('portfolio-list')

class PortfDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio/detail.html'
    context_object_name = 'portfolio'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentsForm()
        return context

class PortfDeleteView(DeleteView):
    model = Portfolio
    template_name = 'portfolio/form.html'
    success_url = reverse_lazy('portfolio-list')


class CommentCreateView(CreateView):
    form_class = CommentsForm
    template_name = 'portfolio/form.html'
    model = Comments
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.portfolio_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('portfolio-detail', kwargs={'pk': self.kwargs['pk']})