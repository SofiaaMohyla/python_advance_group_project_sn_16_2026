from django.shortcuts import render
from .material import Material

def material_list(request):
    materials = Material.objects.all()
    return render(request, 'material_list.html', {'materials': materials})