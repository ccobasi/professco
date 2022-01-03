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
