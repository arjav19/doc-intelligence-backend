from django.contrib import admin
from apps.documents.models import Document,DocumentInsight

class DocumentInsightInline(admin.StackedInline):
    model = DocumentInsight
    extra = 0
    readonly_fields = ('created_at')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id','title','user','status','file_size_bytes','created_at')
    list_filter = ('status','created_at')
    search_fields = ('title','user_username')
    inlines = [DocumentInsightInline]    