from django.contrib import admin


class BasicModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
