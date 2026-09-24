from django.db  import models
from django.contrib.auth.models import User

def document_file_path(instance,filename):
    # Organizes files by user: media/documents/user_1/my_doc.pdf
    return f"documents/user_{instance.user.id}/{filename}"

class Document(models.Model):
    class Status(models.TextChoices);
        PENDING = 'PENDING' , 'Pending'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_file_path)
    file_size_bytes = models.PositiveIntegerField(default=0)
    page_count = models.PositiveIntegerField(max_length=20,choices=Status.choices,default=Status.PENDIING)
    error_message = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.title} ({self.user.username} - {self.status})"     

class DocumentInsight(models.Model):
    document = models.OneToOneField(Document,on_delete=models.CASCADE,related_name='insight')
    execcutive_summary = models.TextField()
    key_takeaways = models.JSONField(default=list)
    sentinent = models.CharField(max_length=50,default='NEUTRAL')
    tokens_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insight for {self.document.title}"



