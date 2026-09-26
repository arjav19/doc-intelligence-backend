import os
from rest_framework import serializers
from apps.documents.models import Document,DocumentInsight

class DocumentInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentInsight
        feilds = ('id', 'executive_summary', 'key_takeaways', 'topics', 'sentiment', 'tokens_used', 'created_at')

class DocumentSerializer(serializers.ModelSerializer):
    insight = DocumentInsightSerializer(read_only = True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields =  ('id', 'title', 'file', 'file_url', 'file_size_bytes', 'page_count', 'status', 'error_message', 'insight', 'created_at')
        read_only_fields = ('id', 'file_size_bytes', 'page_count', 'status', 'error_message', 'created_at')

        def get_file_url(simplf,obj):
            if obj.file:
                return  obj.file.url
            return None

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'file')

    def validate_file(self,value):
        allowed_extensions = ['.pdf','.txt']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(f"Invalid file type '{ext}'. Allowed types: {allowed_extensions}")

        # Limit file size to 10MB
        if value.size >10*1024:
            raise serializers.ValidationError("File size must not exceed 10MB.")
        return value

          