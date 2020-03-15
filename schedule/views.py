from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Groups
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all().order_by('name')
    serializer_class = GroupSerializer


class JSONGroupsView(APIView):
    def get(self, request):
        import urllib.request, json

        with urllib.request.urlopen("https://rasp.dmami.ru/groups-list.json") as url:
            response = json.loads(url.read().decode())

        return Response(response)
