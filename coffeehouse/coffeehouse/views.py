from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'coffeehouse/main.html'
