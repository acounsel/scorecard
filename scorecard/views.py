from django.db.models import Count
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import activate
from django.views.generic import View, DetailView, ListView

from .models import Overview, Commitment, Status, Achievement
from .models import Challenge, Recommendation, Document


class Home(DetailView):
    model = Overview

    def get_object(self, queryset=None):
        return Overview.objects.first()

    def get_context_data(self, **kwargs):
        if 'gtzyavts' in self.request.META['HTTP_HOST']:
            if '/en/' not in self.request.path:
                activate('mn') 
        context = super().get_context_data(**kwargs)
        context.update({
            'achievement_list': Achievement.objects.all(),
            'challenge_list': self.get_challenges(),
            'recommendation_list': Recommendation.objects.all(),
            'chart_dict': self.get_chart_dict(
                context['object'].commitment_set.all()),
            'title': 'Overview',
            'redirect_to': reverse('home'),
        })
        return context

    def get_challenges(self):
        challenge_list = []
        i = 0
        for challenge in Challenge.objects.filter(
            overview=self.get_object()):
            challenge_list.append(challenge)
            i += 1
            if challenge.is_featured:
                i +=1
            if i == 3:
                challenge_list.append('DescriptionBlock')
                i = 0
        return challenge_list

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
        context['active'] = self.get_active_commitment(
            commitments=context['object_list'],
            order_num=self.request.GET.get('commitment'),
            order_letter=self.request.GET.get('section')
        )
        context['redirect_to'] = reverse('home')
        return context

    def get_active_commitment(self, commitments, order_num, 
        order_letter):
        if not order_num:
            order_num = 1
        kwargs = {'order_num': order_num}
        if order_letter:
            kwargs['order_letter':order_letter]
        return Commitment.objects.get(**kwargs)

class CommitmentExport(CommitmentList):

    def get(self, request, **kwargs):
        resp = super().get(request, **kwargs)
        context = super().get_context_data(**kwargs)
        response = context['overview'].export_commitments()
        return response

class CommitmentPDFExport(CommitmentList):

    def get(self, request, **kwargs):
        resp = super().get(request, **kwargs)
        context = super().get_context_data(**kwargs)
        response = context['overview'].export_pdf()
        # return FileResponse(response, 
        #     as_attachment=True, filename='commitments.pdf')
        return response

class DocumentList(ListView):
    model = Document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overview'] = Overview.objects.first()
        context['title'] = 'Documents'
        return context

class Methodology(DetailView):
    model = Overview
    template_name = 'scorecard/methodology.html'

    def get_object(self, queryset=None):
        return Overview.objects.first()



