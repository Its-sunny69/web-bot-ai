from django.db import models
from core.utils.base_models import ReferencBaseModel

# Create your models here.
from django.db import models
from pgvector.django import VectorField


class CodeEmbedding(ReferencBaseModel):
    repo_id = models.BigIntegerField()
    file_path = models.TextField()  # e.g., "src/auth.py"
    chunk_id = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()  # snippet or full file
    embedding = VectorField(dimensions=1536)  # dimension depends on embedding model
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["repo_id"]),
            models.Index(fields=["file_path"]),
        ]
        unique_together = ("repo_id", "file_path", "chunk_id")

    def __str__(self):
        return f"{self.repo_id}::{self.file_path}::{self.chunk_id or 'full'}"
