from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from portfolio.forms import PortfolioForm, CommentsForm
from portfolio.models import Portfolio, Comments
# Create your views here.


    

class PortfCreateView(CreateView):
    form_class = PortfolioForm
    template_name = 'portfolio/form.html'
    model = Portfolio
    success_url = reverse_lazy('portfolio')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
       
class PortfUpdateView(UpdateView):
    form_class = PortfolioForm
    template_name = 'portfolio/form.html'
    model = Portfolio
    success_url = reverse_lazy('portfolio')

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
    success_url = reverse_lazy('portfolio')


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