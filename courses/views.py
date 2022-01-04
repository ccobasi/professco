from django.shortcuts import render
from rest_framework.views import APIView
from courses.models import Course, Sector
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from courses.serializers import CartItemSerializer, CommentSerializer, CourseDisplaySerializer, CourseListSerializer, CoursePaidSerializer, CourseUnPaidSerializer, SectorSerializer


class CoursesHomeViews(APIView):
    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.order_by('?')[:6]

        sector_response = []

        for sector in sectors:
            sector_courses = sector.related_courses.order_by('?')[:4]
            courses_serializer = CourseDisplaySerializer(
                sector_courses, many=True)
            sector_obj = {
                "sector_name": sector.name,
                "sector_uuid": sector.sector_uuid,
                "featured_courses": courses_serializer.data,
                "sector_image": sector.sector_image.url
            }
            sector_response.append(sector_obj)

        # serializer=SectorSerializer(sectors=sector_response,many=True)

        return Response(data=sector_response, status=status.HTTP_200_OK)


class CourseDetail(APIView):
    def get(self, request, course_uuid, *args, **kwargs):
        try:

            course = Course.objects.filter(course_uuid=course_uuid)
        except ValidationError:
            return HttpResponseBadRequest('Invalid Course uuid')

        if not course:
            return HttpResponseBadRequest('Course does not exist')

        serializer = CourseUnPaidSerializer(course[0])

        return Response(serializer.data, status=status.HTTP_200_OK)

class SectorCourse(APIView):
    def get(self, request, sector_uuid, *args, **kwargs):
        sector = Sector.objects.filter(sector_uuid=sector_uuid)

        if not sector:
            return HttpResponseBadRequest("Course sector does not exist")

        sector_courses = sector[0].related_courses.all()

        serializer = CourseListSerializer(sector_courses, many=True)

        total_students = 0

        for course in sector_courses:
            total_students += course.get_enrolled_students()

        return Response({'data': serializer.data,
                        'sector_name': sector[0].name,
                         'total_students': total_students,
                         'image': sector[0].sector_image.url},
                        status=status.HTTP_200_OK)
