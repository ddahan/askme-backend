from django.contrib.auth.models import Group
from rest_framework import viewsets, schemas, response, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import LetterType
from .serializers import ShortLetterTypeSerializer, DetailedLetterTypeSerializer
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth import get_user_model
User = get_user_model()


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Mailator API')
    return response.Response(generator.get_schema(request=request))


class LetterTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    - Get all the lettertypes availaibles, without detail
    - Screen 1: used to search a template to use
    - Usage: GET / list()
    """
    queryset = LetterType.objects.all()
    serializer_class = ShortLetterTypeSerializer


class DetailedLetterTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    - For a given template, provide all information about it, including fields to use.
    - Screen 1 -> 2
    - Usage: GET / retrieve()
    """
    queryset = LetterType.objects.all()
    serializer_class = DetailedLetterTypeSerializer
