from django.contrib import admin

from .models import Overview, Commitment, CommitmentCategory
from .models import Achievement, Challenge, Recommendation
from .models import Status, Document

admin.site.register(Overview)

@admin.register(CommitmentCategory)
class CommitmentCategoryAdmin(admin.ModelAdmin):
    list_items = (
        'order_num',
        'name',
    )
    list_display = list_items
    list_display_links = list_items

@admin.register(Commitment)
class CommitmentAdmin(admin.ModelAdmin):
    list_items = (
        'order_num',
        'order_letter',
        'name',
        'category',
    )
    list_display = list_items
    list_display_links = list_items
    list_filter = ('category',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_items = (
        'commitment',
        'status',
        'date',
        'is_current',
    )
    list_display = list_items
    list_display_links = list_items
    list_filter = ('commitment','status')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_items = (
        'order_id',
        'name',
        'image',
        'is_featured',
    )
    list_display = list_items
    list_display_links = list_items

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_items = (
        'order_id',
        'name',
        'image',
        'is_featured',
    )
    list_display = list_items
    list_display_links = list_items


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_items = (
        'order_id',
        'name',
        'image',
        'is_featured',
    )
    list_display = list_items
    list_display_links = list_items

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_items = (
        'name',
        'document',
    )
    list_display = list_items
    list_display_links = list_items

