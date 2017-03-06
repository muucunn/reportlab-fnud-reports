from django.contrib import admin
from fundreport.models import Fund, Theme, Position, Rationale, Region, Country, AssetClass, FundValue, IndexValue

class RationaleAdmin(admin.ModelAdmin):
    list_display = ['theme', 'action', 'rationale', 'date']
    list_filter = ['action']

class PositionAdmin(admin.ModelAdmin):
    list_display = ['theme', 'LTD', 'SL', 'var', 'cvar']
    list_filter = ['theme__fund']

class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'fund']
    list_filter = ['fund']

admin.site.register(Fund)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Rationale, RationaleAdmin)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(AssetClass)
admin.site.register(FundValue)
admin.site.register(IndexValue)

            
