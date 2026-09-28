from rest_framework import viewsets,parsers
from apps.documents.models import Document
from apps.documents.serializers import DocumentSerializer,DocumentUploadSerializer
from apps.documents.services.extractor import DocumentExtractor
from apps.documents.services.ai_analyzer import AIService
from apps.documents.models import Document, DocumentInsight


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
        uploaded_file = self.request.FILES.get('file')
        file_size = uploaded_file.size if uploaded_file else 0


        # 1. Save document with PROCESSING status
        instance = serializer.save(
            user=self.request.user,
            file_size_bytes=file_size,
            status=Document.Status.PROCESSING
        )


        try:
            # 2. Extract text from uploaded document
            text, page_count = DocumentExtractor.extract_text(instance.file.path)
            instance.page_count = page_count


            # 3. Analyze with AI service
            ai_service = AIService()
            insights = ai_service.analyze_document(text)


            # 4. Save structured insights to PostgreSQL
            DocumentInsight.objects.create(
                document=instance,
                executive_summary=insights.get('executive_summary', ''),
                key_takeaways=insights.get('key_takeaways', []),
                topics=insights.get('topics', []),
                sentiment=insights.get('sentiment', 'NEUTRAL'),
                tokens_used=insights.get('tokens_used', 0)
            )


            instance.status = Document.Status.COMPLETED
            instance.save()


        except Exception as e:
            instance.status = Document.Status.FAILED
            instance.error_message = str(e)
            instance.save()




