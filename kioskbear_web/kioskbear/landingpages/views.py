from django.views.generic import TemplateView


class StartPageView(TemplateView):
    template_name = 'landingpages/index.html'


