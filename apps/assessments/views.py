from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Assessment
from .forms import AssessmentForm
from apps.courses.models import Course
from apps.courses.mixins import TeacherRequiredMixin

class AssessmentCreateView(TeacherRequiredMixin, CreateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = 'assessments/assessment_form.html'
    success_url = reverse_lazy('courses:course_list')


    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, slug=self.kwargs.get('course_slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course'] = self.course
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

    def form_valid(self, form):
        form.instance.course = self.course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'course_slug': self.course.slug})