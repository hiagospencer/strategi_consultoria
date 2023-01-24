from django.contrib import admin

from .models import HeroiMarvel, EquipeHeroi


admin.site.register(HeroiMarvel)

@admin.register(EquipeHeroi)
class EquipeHeroiAdmin(admin.ModelAdmin):
    list_filter = ('user',)

