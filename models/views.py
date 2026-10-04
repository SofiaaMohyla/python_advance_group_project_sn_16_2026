import re
from urllib.parse import parse_qs, urlparse

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .forms import MaterialForm
from .material import Material


class MaterialListView(ListView):
    model = Material
    template_name = 'material_list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        return Material.objects.all().order_by('-id')


class MaterialDetailView(DetailView):
    model = Material
    template_name = 'material_detail.html'
    context_object_name = 'material'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['youtube_embed_url'] = get_youtube_embed_url(self.object.you_tube_link)
        return context


def get_youtube_embed_url(url):
    """Return a privacy-enhanced embed URL for supported YouTube links."""
    if not url:
        return ''

    parsed_url = urlparse(url)
    host = (parsed_url.hostname or '').lower().rstrip('.')
    allowed_hosts = {
        'youtube.com', 'www.youtube.com', 'm.youtube.com',
        'youtube-nocookie.com', 'www.youtube-nocookie.com', 'youtu.be',
        'www.youtu.be',
    }
    if host not in allowed_hosts:
        return ''

    video_id = ''
    if host.endswith('youtu.be'):
        video_id = parsed_url.path.strip('/').split('/')[0]
    elif parsed_url.path == '/watch':
        video_id = parse_qs(parsed_url.query).get('v', [''])[0]
    else:
        match = re.match(r'^/(?:embed|shorts|live)/([^/]+)', parsed_url.path)
        if match:
            video_id = match.group(1)

    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', video_id):
        return ''
    return f'https://www.youtube-nocookie.com/embed/{video_id}'


def material_add(request):
    form = MaterialForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        material = form.save()
        return redirect(reverse('material_detail', kwargs={'pk': material.pk}))
    return render(request, 'material_form.html', {'form': form})