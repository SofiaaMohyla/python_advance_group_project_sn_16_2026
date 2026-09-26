from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PollForm, PollOptionFormSet, VoteForm
from .models import Poll, Vote


def can_manage_polls(user):
    return user.is_authenticated and (user.is_superuser or user.role in {"admin", "moderator"})


class PollManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return can_manage_polls(self.request.user)


class PollListView(ListView):
    model = Poll
    template_name = "voting/poll_list.html"
    context_object_name = "polls"


class PollDetailView(DetailView):
    model = Poll
    template_name = "voting/poll_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.object
        user_vote = None
        if self.request.user.is_authenticated:
            user_vote = Vote.objects.filter(poll=poll, user=self.request.user).first()
            context["vote_form"] = VoteForm(poll=poll, initial={"option": user_vote.option_id if user_vote else None})
        context["user_vote"] = user_vote
        total_votes = poll.votes.count()
        options = poll.options.annotate(vote_count=Count("votes"))
        for option in options:
            option.percentage = round(option.vote_count * 100 / total_votes, 1) if total_votes else 0
        context["total_votes"] = total_votes
        context["options_with_results"] = options
        return context


class PollFormsetMixin(PollManagerRequiredMixin):
    form_class = PollForm
    template_name = "voting/poll_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in context:
            context["formset"] = PollOptionFormSet(instance=getattr(self, "object", None))
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() if "pk" in kwargs else None
        form = self.get_form()
        formset = PollOptionFormSet(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    @transaction.atomic
    def forms_valid(self, form, formset):
        form.instance.created_by = form.instance.created_by or self.request.user
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        messages.success(self.request, "Голосування збережено.")
        return redirect(self.get_success_url())


class PollCreateView(PollFormsetMixin, CreateView):
    def get_success_url(self):
        return reverse("voting:detail", kwargs={"pk": self.object.pk})


class PollUpdateView(PollFormsetMixin, UpdateView):
    model = Poll

    def get_success_url(self):
        return reverse("voting:detail", kwargs={"pk": self.object.pk})


class PollDeleteView(PollManagerRequiredMixin, DeleteView):
    model = Poll
    template_name = "voting/poll_confirm_delete.html"
    success_url = "/voting/"

    def form_valid(self, form):
        messages.success(self.request, "Голосування видалено.")
        return super().form_valid(form)


@login_required
@require_POST
def vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if not poll.is_active:
        messages.error(request, "Це голосування завершене.")
        return redirect("voting:detail", pk=poll.pk)

    form = VoteForm(request.POST, poll=poll)
    if not form.is_valid():
        messages.error(request, "Оберіть один із запропонованих варіантів.")
        return redirect("voting:detail", pk=poll.pk)

    Vote.objects.update_or_create(
        poll=poll,
        user=request.user,
        defaults={"option": form.cleaned_data["option"]},
    )
    messages.success(request, "Ваш голос збережено. Ви можете змінити його, доки голосування активне.")
    return redirect("voting:detail", pk=poll.pk)
