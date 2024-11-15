from django.contrib import admin
from .models import Tag, Author, Quote, User
from django.contrib.sessions.models import Session

# Register your models here.
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Quote)
admin.site.register(User)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]


admin.site.register(Session, SessionAdmin)
