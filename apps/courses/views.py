from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from .models import Course, Lesson
from .forms import CourseForm

# View to list all published courses
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses' 
    paginate_by = 10 

    def get_queryset(self):
        return Course.objects.filter(status='published').select_related('teacher')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Explore our Courses"
        return context
    
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'
    query_pk_and_slug = False

    # Query optimised to fetch modules and lessons in a single trip to the database (Prefetching)
    def get_queryset(self):
        return Course.objects.filter(status='published').prefetch_related('modules__lessons').select_related('teacher')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context
    
class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'

    def get_object(self, queryset=None):
        # Overwrite to ensure that the lesson belongs to the correct course and the correct module.
        return Lesson.objects.get(
            slug=self.kwargs.get('lesson_slug'),
            module__course__slug=self.kwargs.get('course_slug')
        )
    
class OwnerRequiredMixin(UserPassesTestMixin):
     def test_func(self):
          obj = self.get_object()
          return obj.teacher == self.request.user or self.request.user.is_superuser
     
     def handle_no_permission(self):
          if self.request.user.is_authenticated:
              raise PermissionDenied
          return super().handle_no_permission()

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)
    
class CourseUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    slug_url_kwarg = 'course_slug'

    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'course_slug': self.object.slug})
    
class CourseDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    slug_url_kwarg = 'course_slug'
    success_url = reverse_lazy('courses:course_list')