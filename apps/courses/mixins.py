# Path: apps/courses/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Course, Module, Lesson, Enrollment


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Allows access only to the teacher who owns the content or superusers.
    Works with Course, Module and Lesson.
    """
    permission_denied_message = "Only the content owner can perform this action."
    
    def test_func(self):
        obj = self.get_object()
        
        # Get the course depending on the object type
        if isinstance(obj, Course):
            course = obj
        elif isinstance(obj, Module):
            course = obj.course
        elif isinstance(obj, Lesson):
            course = obj.module.course
        else:
            return False
        
        return course.teacher == self.request.user or self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            raise PermissionDenied
        return super().handle_no_permission()


class TeacherRequiredMixin(UserPassesTestMixin):
    """
    Allows access only to users with a teacher profile.
    """
    permission_denied_message = "This action is only available to teachers."
    
    def test_func(self):
        return self.request.user.is_teacher
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, self.permission_denied_message)
            return redirect('home')
        return super().handle_no_permission()


class EnrollmentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Allows access only to users enrolled in the course.
    The course teacher and superusers always have access.
    """
    
    def test_func(self):
        # Determine the course depending on the context
        try:
            if 'course_slug' in self.kwargs:
                course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
            elif hasattr(self, 'object') and self.object:
                course = self.object
            else:
                course = self.get_object()
        except Exception:
            return False
        
        user = self.request.user
        
        # Teacher and superusers always have access
        if course.teacher == user or user.is_superuser:
            return True
        
        # Check active enrolment
        return course.enrollments.filter(
            user=user, 
            status=Enrollment.Status.ACTIVE
        ).exists()
    
    def handle_no_permission(self):
        if 'course_slug' in self.kwargs:
            if self.request.user.is_authenticated:
                messages.warning(
                    self.request, 
                    'You must enrol in this course to access the content.'
                )
            return redirect('courses:course_detail', course_slug=self.kwargs['course_slug'])
        
        return super().handle_no_permission()