from rest_framework import viewsets,parsers
from apps.documents.models import Document
from apps.documents.serializers import DocumentSerializer,DocumentUploadSerializer

class DocumesntViewSet(viewsets.ModelViewSet):
    parser_classes =(parsers.MultiPartParser,parsers.FormParser,parsers.JSONParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentUploadSerializer
        return DocumentSerializer

    def get_queryset(self):
        # Scoped strictly to the logged-in user with joined insights
        return Document.objects.filter(user = self.request.user).select_related('insight')

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('files')
        file_size = uploaded_file.size if uploaded_file else 0
        serializer.save(
            user = self.request.user,
            file_size_byte =file_size,
            status = Document.Status.PENDING
        )

    