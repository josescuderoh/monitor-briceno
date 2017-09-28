from django.views import generic


# Default views
class HomeView(generic.TemplateView):
    template_name = 'projects/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
