# Path: apps/courses/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Course, Lesson
from .forms import CourseForm
from .mixins import OwnerRequiredMixin, EnrollmentRequiredMixin, TeacherRequiredMixin


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
        user = self.request.user
        
        if user.is_authenticated:
            context['is_teacher'] = (self.object.teacher == user or user.is_superuser)
            context['is_enrolled'] = self.object.enrollments.filter(
                user=user, 
                status='active'
            ).exists()
        else:
            context['is_teacher'] = False
            context['is_enrolled'] = False
            
        return context
    
class LessonDetailView(EnrollmentRequiredMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Lesson.objects.select_related('module__course').prefetch_related('module__lessons'),
            slug=self.kwargs.get('lesson_slug'),
            module__course__slug=self.kwargs.get('course_slug')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_lessons'] = self.object.module.lessons.all()
        return context
    
class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_teacher
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()
    
class CourseCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
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