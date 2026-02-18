# Path: apps/assessments/views.py
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView

from apps.courses.mixins import TeacherRequiredMixin
from apps.courses.models import Course

from .forms import AssessmentForm, QuestionFormSet
from .models import Assessment


class AssessmentCreateView(TeacherRequiredMixin, CreateView):
    model = Assessment
    form_class = AssessmentForm
    template_name = "assessments/assessment_form.html"

    # Ensure the course context from the start.
    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, slug=self.kwargs.get("course_slug"))
        return super().dispatch(request, *args, **kwargs)

    # Inject the course into the AssessmentForm.
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["course"] = self.course
        return kwargs

    # Send the course and the Question FormSet to the template.
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["course"] = self.course  # For the cancel button and titles

        if self.request.POST:
            data["questions"] = QuestionFormSet(self.request.POST)
        else:
            data["questions"] = QuestionFormSet()
        return data

    # Atomic handling of Exam + Questions.
    def form_valid(self, form):
        context = self.get_context_data()
        questions = context["questions"]

        # Use transactions to avoid creating an exam without questions if something fails
        with transaction.atomic():
            # 1. Assign the course and save the exam (Assessment)
            form.instance.course = self.course
            self.object = form.save()

            # 2. Validate and save the questions
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
            else:
                # If the questions are not valid, return to the form with errors
                return self.render_to_response(self.get_context_data(form=form))

        return redirect("courses:course_detail", course_slug=self.course.slug)
