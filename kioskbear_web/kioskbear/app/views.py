from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from kioskbear.feedback.models import Rating, Option, ScoredOption
from kioskbear.kiosk.models import Survey, Block
from kioskbear.accounts.models import Customer

from operator import itemgetter


from django.utils import timezone


class DashboardView(DetailView):
    template_name = 'app/dashboard.html'
    model = Customer

    def get_object(self, queryset=None):
        return self.request.user.customer

    def _get_change(self, current, previous):
        if current == previous:
            return 0
        if previous:
            if current:
                if current > previous:
                    trend = 'up'
                else:
                    trend = 'down'
            else:
                trend = 'down'
                return trend, float('inf')
        else:
            return 'inf', float('inf')
        try:
            return trend, (abs(current - previous) / previous) * 100.0
        except ZeroDivisionError:
            return trend, float('inf')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        survey = Survey.objects.filter(customer=self.request.user.customer).first()

        last_7days = timezone.now() - timezone.timedelta(days=7)
        last_14days = timezone.now() - timezone.timedelta(days=14)
        last_30days = timezone.now() - timezone.timedelta(days=30)
        last_60days = timezone.now() - timezone.timedelta(days=60)

        avg_today = Rating.objects.filter(survey=survey, created_datetime__date=timezone.now().date()).aggregate(Avg('score'))
        avg_yesterday = Rating.objects.filter(survey=survey, created_datetime__date=timezone.now() - timezone.timedelta(
            days=1)).aggregate(Avg('score'))
        change_today = self._get_change(avg_today['score__avg'], avg_yesterday['score__avg'])
        context['avg_today'] = avg_today
        context['change_today'] = change_today
        context['avg_yesterday'] = avg_yesterday

        avg_7d = Rating.objects.filter(survey=survey, created_datetime__gte=last_7days).aggregate(Avg('score'))
        avg_7d_last_period = Rating.objects.filter(survey=survey, created_datetime__gte=last_14days, created_datetime__lt=last_7days).aggregate(Avg('score'))
        change_7d = self._get_change(avg_7d['score__avg'], avg_7d_last_period['score__avg'])
        context['avg_7d'] = avg_7d
        context['change_7d'] = change_7d

        avg_30d = Rating.objects.filter(survey=survey, created_datetime__gte=last_30days).aggregate(Avg('score'))
        avg_30d_last_period = Rating.objects.filter(survey=survey, created_datetime__gte=last_60days, created_datetime__lt=last_30days).aggregate(Avg('score'))
        change_30d = self._get_change(avg_30d['score__avg'], avg_30d_last_period['score__avg'])
        context['avg_30d'] = avg_30d
        context['change_30d'] = change_30d

        context['daily_ratings_10d'] = self._get_daily_ratings(limit=10)
        context['daily_ratings_30d'] = self._get_daily_ratings(limit=30)
        context['latest_ratings'] = Rating.objects.filter(survey=survey).order_by('-pk')[:10]
        return context


    def _get_daily_ratings(self, limit=30):
        items = Rating.objects.filter(survey=Survey.objects.filter(customer=self.request.user.customer).first(),
                                      created_datetime__date__lte=timezone.now().date(),
                                      created_datetime__date__gt=timezone.now().date() - timezone.timedelta(
                                          days=limit)
                                      ).order_by('-created_datetime').annotate(created_date=TruncDate('created_datetime')
                                                                               ).order_by('-created_date').values('created_date').annotate(**{'count': Count('created_date'), 'avg_score': Avg('score')})
        items = list(items)

        dates = [x.get('created_date') for x in items]

        for d in (timezone.datetime.today() - timezone.timedelta(days=x) for x in range(0, limit)):
            if d.date() not in dates:
                items.append({'created_date': d.date(), 'count': 0, 'avg_score': '-'})
        items.sort(key=itemgetter('created_date'), reverse=True)
        return items


class SurveyBuilderView(DetailView):
    model = Survey
    template_name = 'app/survey_builder.html'

    def get_object(self):
        return Survey.objects.filter(customer=self.request.user.customer).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        survey = self.request.user.customer.survey_set.first()
        if self.request.GET.get('q'):
            block_list = self.request.GET.get('q').split(',')
            open_blocks = Block.objects.filter(Q(pk=survey.start_block.pk) | Q(pk__in=block_list))
        else:
            open_blocks = Block.objects.filter(pk=survey.start_block.pk)
        context['open_blocks'] = open_blocks

        return context


class UpdateScoredOptionText(UpdateView):
    model = ScoredOption
    template_name = 'app/survey_builder.html'
    fields = ('text',)

    def get_success_url(self):
        return reverse('app:survey-builder')


class UpdateScoredOptionFollowUp(UpdateView):
    model = ScoredOption
    template_name = 'app/survey_builder.html'
    fields = ('follow_up_block',)

    def get_success_url(self):
        if self.object.follow_up_block:
            return '%s?q=%s' % (reverse('app:survey-builder'), self.object.follow_up_block.pk)
        else:
            return reverse('app:survey-builder')


class CreateBlock(CreateView):
    model = Block
    fields = ('title', )
    template_name = 'app/survey_builder.html'

    def form_valid(self, form):
        block = form.save(commit=False)
        block.survey = Survey.objects.filter(customer=self.request.user.customer).first()
        block.save()
        if self.request.GET.get('parenttype') == 'scoredoption':
            parent = ScoredOption.objects.get(pk=self.request.GET.get('parentid'))
        else:
            parent = Option.objects.get(pk=self.request.GET.get('parentid'))
        parent.follow_up_block = block
        parent.save()
        if self.request.GET.get('q'):
            return redirect('%s?q=%s,%s' % (reverse('app:survey-builder'), self.request.GET.get('q'), block.pk))
        else:
            return redirect('%s?q=%s' % (reverse('app:survey-builder'), block.pk))


class UpdateFollowUpQuestion(UpdateView):
    model = Block
    template_name = 'app/survey_builder.html'
    fields = ('title',)

    def get_success_url(self):
        return '%s?q=%s' % (reverse('app:survey-builder'), self.request.GET.get('q'))


class CreateOption(CreateView):
    model = Option
    template_name = 'app/survey_builder.html'
    fields = ('text',)

    def form_valid(self, form):
        option = form.save(commit=False)
        block = Block.objects.get(pk=self.request.GET.get('edit'))
        block.save()
        option.block = block
        option.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        return '%s?q=%s&edit=%s' % (reverse('app:survey-builder'), self.request.GET.get('q'), self.request.GET.get('edit'))


class DeleteOption(DeleteView):
    model = Option
    template_name = 'app/survey_builder.html'

    def get_success_url(self):
        return '%s?q=%s' % (reverse('app:survey-builder'), self.request.GET.get('q'))


class UpdateOptionFollowUp(UpdateView):
    model = Option
    template_name = 'app/survey_builder.html'
    fields = ('follow_up_block', )

    def get_success_url(self):
        if self.object.follow_up_block:
            return '%s?q=%s,%s' % (reverse('app:survey-builder'), self.request.GET.get('q'), self.object.follow_up_block.pk)
        else:
            questions_list = self.request.GET.get('q').split(',')
            open_blocks = Block.objects.filter(pk__in=questions_list)

            for b in open_blocks:
                if not Option.objects.filter(follow_up_block=b).first():
                    if str(b.pk) in questions_list:
                        if not ScoredOption.objects.filter(follow_up_block=b).first():
                            questions_list.remove(str(b.pk))
            questions_list = ','.join(questions_list)
            return '%s?q=%s' % (reverse('app:survey-builder'), questions_list)


class UpdateOption(UpdateView):
    model = Option
    template_name = 'app/survey_builder.html'
    fields = ('text',)

    def get_success_url(self):
        return '%s?q=%s' % (reverse('app:survey-builder'), self.request.GET.get('q'))
