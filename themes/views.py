from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AdminTheme
from .serializers import AdminThemeSerializer, AdminThemeToggleSerializer
from rest_framework.permissions import IsAdminUser

class AdminThemeViewSet(viewsets.ModelViewSet):
    queryset = AdminTheme.objects.all()
    serializer_class = AdminThemeSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'])
    def toggle_active(self, request):
        serializer = AdminThemeToggleSerializer(data=request.data)
        if serializer.is_valid():
            theme = AdminTheme.objects.get(pk=serializer.validated_data['id'])
            theme.is_active = serializer.validated_data['is_active']
            theme.save()
            return Response({'status': 'theme updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
