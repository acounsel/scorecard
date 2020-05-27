from django.shortcuts import render
from django.views.generic import View, DetailView, ListView

from .models import Overview, Commitment, Status, Achievement
from .models import Challenge, Recommendation

class Home(DetailView):
    model = Overview

    def get_object(self, queryset=None):
        return Overview.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'achievement_list': Achievement.objects.all(),
            'challenge_list': Challenge.objects.all(),
            'recommendation_list': Recommendation.objects.all(),
            'title': 'Overview',
        })
        return context


