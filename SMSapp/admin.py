from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Announcement)
admin.site.register(Course)
admin.site.register(Tutorial)
admin.site.register(Notes)
# admin.site.register(Quiz)
# admin.site.register(Question)
# admin.site.register(Answer)
admin.site.register(Learner)
admin.site.register(Instructor)
# admin.site.register(TakenQuiz)
# admin.site.register(LearnerAnswer)
