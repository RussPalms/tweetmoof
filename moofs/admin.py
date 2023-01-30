from django.contrib import admin

# Register your models here.
from .models import Moof, MoofLike

class MoofLikeAdmin(admin.TabularInline):
    model = MoofLike

class MoofAdmin(admin.ModelAdmin):
    inlines = [MoofLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Moof

admin.site.register(Moof, MoofAdmin)
