from django.db import models
from authapp.models import User

# Create your models here.
class book(models.Model):
    title = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=1200, unique=True, blank=True)
    file = models.FileField(upload_to='pdfbooks/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'
        
    class ordering:
        ordering = ['-date']
    
    def __str__(self):
        return self.title