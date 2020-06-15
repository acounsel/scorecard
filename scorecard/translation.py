from modeltranslation.translator import register, TranslationOptions
from .models import Overview, CommitmentCategory, Commitment
from .models import Status, Achievement, Challenge, Recommendation
from .models import Document

@register(Overview)
class OverviewTranslationOptions(TranslationOptions):
    fields = ('name', 'subtitle', 'story_part1', 'story_part2', 'story_part3',
        'achievements_text', 'challenges_text',
        'commitment_chart_text', 'about_us', 'methodology')

@register(CommitmentCategory)
class CommitmentCategoryOptions(TranslationOptions):
    fields = ('name', 'order_num')

@register(Commitment)
class CommitmentOptions(TranslationOptions):
    fields = ('name', 'description', 'original_timeline',
        'order_num', 'order_letter')

@register(Status)
class StatusOptions(TranslationOptions):
    fields = ('description',)

@register(Achievement)
class AchievementOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Challenge)
class ChallengeOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Recommendation)
class RecommendationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Document)
class DocumentOptions(TranslationOptions):
    fields = ('name', 'description')
