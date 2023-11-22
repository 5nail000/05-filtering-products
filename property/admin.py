from django.contrib import admin
from .models import Flat, Сlaim, Like, Owner


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    raw_id_fields = ('user',)


class OwnerInline(admin.TabularInline):
    model = Owner.flats.through
    extra = 1
    raw_id_fields = ('owner',)
    verbose_name = 'Владелец'
    verbose_name_plural = 'Владельцы'


class FlatAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'address', 'price', 'new_building', 'construction_year', 'town'
        )
    list_editable = ('new_building',)
    list_filter = ('new_building', 'rooms_number', 'has_balcony', 'town')
    search_fields = ('town', 'address', 'owner')
    readonly_fields = ("created_at",)
    raw_id_fields = ('liked_by',)
    inlines = [LikeInline, OwnerInline]


class СlaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'flat', 'text')
    raw_id_fields = ('user', 'flat')


class LikeAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'flat')


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'normalized_phone')
    search_fields = ('full_name', 'normalized_phone')
    raw_id_fields = ('flats',)


admin.site.register(Flat, FlatAdmin)
admin.site.register(Сlaim, СlaimAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Owner, OwnerAdmin)

# '''
