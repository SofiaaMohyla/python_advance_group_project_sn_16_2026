from django.contrib import admin
from .material import Material

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	list_display = ('title', 'id')
	search_fields = ('title', 'description')
	ordering = ('-id',)

	def has_module_permission(self, request):
		return request.user.is_active and request.user.is_staff

	def has_add_permission(self, request):
		return request.user.is_active and request.user.is_staff

	def has_change_permission(self, request, obj=None):
		return request.user.is_active and request.user.is_staff

	def has_delete_permission(self, request, obj=None):
		return request.user.is_active and request.user.is_staff