from django.db import migrations

def create_initial_course(apps, schema_editor):
    
    User = apps.get_model('users', 'User')
    Course = apps.get_model('courses', 'Course')

    teacher = User.objects.filter(is_superuser=True).first()
    
    if teacher:
        Course.objects.get_or_create(
            title="Welcome to Evolaris Academy",
            slug="welcome-evolaris-academy",
            defaults={
                "description": "This is your first course on Evolaris Academy. Explore the features and start learning!",
                "teacher": teacher,
                "status": "published"
            }
        )

def remove_initial_course(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Course.objects.filter(slug="welcome-evolaris-academy").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_lesson_content_enrollment_course_students_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_course, reverse_code=remove_initial_course),
    ]