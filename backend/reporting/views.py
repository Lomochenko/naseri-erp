from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get(self, request):
        reports = Report.objects.all()
        data = [{'id': report.id, 'name': report.name, 'description': report.description} for report in reports]
        return Response(data)

    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)