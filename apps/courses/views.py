# Path: apps/courses/views.py
from django.views.generic import ListView
from .models import Course

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