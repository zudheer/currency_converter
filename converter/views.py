from django.views.generic import TemplateView
from converter.forms import CSVUploadForm
from django.views.generic.edit import FormView


class HomeView(FormView):
    """Landing page."""
    template_name = 'index.html'
    form_class = CSVUploadForm

    def form_valid(self, form):
        return form.parse_csv()
