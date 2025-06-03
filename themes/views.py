from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AdminTheme
from .serializers import AdminThemeSerializer, AdminThemeToggleSerializer
from rest_framework.permissions import IsAdminUser
from admin_customizer.ai_service import generate_text_with_openai
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import process_ai_request # Import the Celery task






def ai_response_view(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt', 'Tell me a fun fact about Django.')
        ai_text = generate_text_with_openai(prompt)
        return JsonResponse({'prompt': prompt, 'ai_response': ai_text})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

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


def trigger_ai_task_view(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt', 'Write a short poem about a purple sunset.')
        # Call the Celery task
        task = process_ai_request.delay(prompt)
        return JsonResponse({'message': 'AI processing started in background', 'task_id': task.id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



