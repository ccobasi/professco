from django.urls import path
from courses.views import *

app_name = 'courses'

urlpatterns = [
    path('cart/',GetCartDetail.as_view()),
    path('detail/<uuid:course_uuid>/', CourseDetail.as_view()),
    path("search/<str:search_term>/", CourseSearch.as_view()),
    path('comment/<uuid:course_uuid>/', AddComment.as_view()),
    path('', CoursesHomeViews.as_view()),
    path('<uuid:sector_uuid>/', SectorCourse.as_view()),

]
