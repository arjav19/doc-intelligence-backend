import pytest
from unittest.mock import patch
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from apps.documents.models import Document


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.mark.django_db
class TestDocumentFlow:
    def test_unauthenticated_request_fails(self, api_client):
        response = api_client.get('/api/documents/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    @patch('apps.documents.services.extractor.DocumentExtractor.extract_text')
    @patch('apps.documents.services.ai_analyzer.AIService.analyze_document')
    def test_upload_document_success(self, mock_ai, mock_extractor, auth_client, test_user):
        # Mock extractor and AI so tests run offline instantly
        mock_extractor.return_value = ("Sample extracted text", 1)
        mock_ai.return_value = {
            "executive_summary": "Clean invoice test summary.",
            "key_takeaways": ["Total is $7,200", "Net 30 terms"],
            "topics": ["Billing", "Invoices"],
            "sentiment": "NEUTRAL",
            "tokens_used": 85
        }


        test_file = SimpleUploadedFile("invoice.txt", b"Mock invoice content", content_type="text/plain")
        response = auth_client.post(
            '/api/documents/',
            {'title': 'Invoice 2026', 'file': test_file},
            format='multipart'
        )


        assert response.status_code == status.HTTP_201_CREATED
        doc = Document.objects.get(id=response.data['id'])
        assert doc.status == Document.Status.COMPLETED
        assert doc.user == test_user
        assert doc.insight.sentiment == "NEUTRAL"
        assert len(doc.insight.key_takeaways) == 2


    def test_user_cannot_access_other_users_document(self, api_client, test_user):
        other_user = User.objects.create_user(username="other", password="password123")
        other_doc = Document.objects.create(user=other_user, title="Private Doc")


        api_client.force_authenticate(user=test_user)
        response = api_client.get(f'/api/documents/{other_doc.id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
