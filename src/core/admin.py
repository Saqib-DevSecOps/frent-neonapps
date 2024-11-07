from django.contrib import admin

from .models import (
    Country, Application, Language
)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'tagline', 'is_active', 'created_on')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'language', 'currency', 'phone_code', 'is_active', 'created_on')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'is_active', 'created_on')
