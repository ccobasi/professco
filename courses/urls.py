from django.urls import path
from courses.views import *

app_name = 'courses'

urlpatterns = [
    path('detail/<uuid:course_uuid>/', CourseDetail.as_view()),
    path('', CoursesHomeViews.as_view()),
    path('<uuid:sector_uuid>/', SectorCourse.as_view()),

]
