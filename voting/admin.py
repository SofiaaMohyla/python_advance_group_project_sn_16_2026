from django.contrib import admin

from .models import Poll, PollOption, Vote


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_by", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    inlines = (PollOptionInline,)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "option", "user", "updated_at")
    list_filter = ("poll",)
    search_fields = ("user__username", "poll__title")
