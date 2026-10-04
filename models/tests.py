from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .material import Material
from .views import get_youtube_embed_url


class MaterialPagesTests(TestCase):
    def setUp(self):
        self.material = Material.objects.create(
            title='Django basics',
            description='A complete description that is longer than fifteen characters.',
            you_tube_link='https://www.youtube.com/watch?v=abcdefghijk',
        )

    def test_list_shows_short_description_and_public_add_link(self):
        response = self.client.get(reverse('material_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A complete des…')
        self.assertContains(response, reverse('material_add'))
        self.assertNotContains(response, 'youtube-nocookie.com')

    def test_detail_embeds_youtube_video(self):
        response = self.client.get(reverse('material_detail', args=[self.material.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.material.description)
        self.assertContains(response, 'https://www.youtube-nocookie.com/embed/abcdefghijk')

    def test_public_form_creates_material(self):
        response = self.client.post(reverse('material_add'), {
            'title': 'New learning material',
            'description': 'Publicly submitted content',
            'you_tube_link': 'https://youtu.be/abcdefghijk',
        })

        created = Material.objects.get(title='New learning material')
        self.assertRedirects(response, reverse('material_detail', args=[created.pk]))

    def test_youtube_urls_are_validated_before_embedding(self):
        self.assertEqual(
            get_youtube_embed_url('https://youtu.be/abcdefghijk'),
            'https://www.youtube-nocookie.com/embed/abcdefghijk',
        )
        self.assertEqual(get_youtube_embed_url('https://example.com/watch?v=abcdefghijk'), '')


class MaterialAdminAccessTests(TestCase):
    def test_staff_can_manage_materials_in_admin(self):
        user = get_user_model().objects.create_user(
            username='staff-member', password='safe-test-password', is_staff=True,
        )
        self.client.force_login(user)

        response = self.client.get('/admin/models/material/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add material')

    def test_regular_user_cannot_access_admin(self):
        user = get_user_model().objects.create_user(
            username='regular-member', password='safe-test-password',
        )
        self.client.force_login(user)

        response = self.client.get('/admin/models/material/')

        self.assertEqual(response.status_code, 302)