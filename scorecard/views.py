from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View, DetailView, ListView

from .models import Overview, Commitment, Status, Achievement
from .models import Challenge, Recommendation, Document

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
            'chart_dict': self.get_chart_dict(
                context['object'].commitment_set.all()),
            'title': 'Overview',
        })
        return context

    def get_chart_dict(self, commitment_list):
        statuses = Status.objects.filter(
            commitment__in=commitment_list).order_by('status')
        chart_dict = {}
        for year in (2019, 2020):
            chart_dict[year] = {}
            year_values = statuses.filter(date__year=year)
            values = year_values.values('status').annotate(
                status_count=Count('status')).order_by('status')
            for value in values:
                chart_dict[year][value['status']] = \
                    value['status_count']
        return chart_dict

class CommitmentList(ListView):
    model = Commitment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overview'] = Overview.objects.first()
        context['title'] = 'Commitments'
        return context

class DocumentList(ListView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overview'] = Overview.objects.first()
        context['title'] = 'Documents'
        return context