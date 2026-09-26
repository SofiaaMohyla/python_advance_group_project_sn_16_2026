from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Poll, PollOption, Vote


class VotingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="student", password="secret")
        self.moderator = get_user_model().objects.create_user(
            username="moderator", password="secret", role="moderator"
        )
        self.poll = Poll.objects.create(title="Куди йдемо?", created_by=self.moderator)
        self.first_option = PollOption.objects.create(poll=self.poll, text="У парк")
        self.second_option = PollOption.objects.create(poll=self.poll, text="У кіно")

    def test_results_are_visible_to_anonymous_users(self):
        response = self.client.get(reverse("voting:detail", args=(self.poll.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Результати")

    def test_user_can_change_vote_without_creating_second_vote(self):
        self.client.login(username="student", password="secret")
        url = reverse("voting:vote", args=(self.poll.pk,))

        self.client.post(url, {"option": self.first_option.pk})
        self.client.post(url, {"option": self.second_option.pk})

        self.assertEqual(Vote.objects.filter(poll=self.poll, user=self.user).count(), 1)
        self.assertEqual(Vote.objects.get(poll=self.poll, user=self.user).option, self.second_option)

    def test_regular_user_cannot_manage_polls(self):
        self.client.login(username="student", password="secret")

        response = self.client.get(reverse("voting:create"))

        self.assertEqual(response.status_code, 403)

    def test_moderator_can_create_poll_with_two_options(self):
        self.client.login(username="moderator", password="secret")
        response = self.client.post(
            reverse("voting:create"),
            {
                "title": "Дата зустрічі",
                "description": "Оберіть дату",
                "is_active": "on",
                "options-TOTAL_FORMS": "2",
                "options-INITIAL_FORMS": "0",
                "options-MIN_NUM_FORMS": "2",
                "options-MAX_NUM_FORMS": "1000",
                "options-0-text": "Понеділок",
                "options-1-text": "Вівторок",
            },
        )

        new_poll = Poll.objects.get(title="Дата зустрічі")
        self.assertRedirects(response, reverse("voting:detail", args=(new_poll.pk,)))
        self.assertEqual(new_poll.options.count(), 2)
