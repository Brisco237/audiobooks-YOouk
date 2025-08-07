import PyPDF2
from django.shortcuts import render, redirect, get_object_or_404
from .models import book
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from authapp.models import User
from django.contrib import messages
from gtts import gTTS
from django.http import FileResponse
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image

# Create your views here.
@login_required(login_url='login_user')
def selectpdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file and uploaded_file.name.endswith('.pdf'):
            titre = uploaded_file.name
            slug = slugify(titre)
            new_book = book.objects.create(title=uploaded_file.name,file=uploaded_file,user=request.user,slug=slug)
            return redirect('audiopdf', slug=new_book.slug)
    pdf_books = book.objects.filter(user=request.user).order_by('-date')
    return render(request, 'readpdf/selectpdf.html', {'pdf_books': pdf_books})

def audiopdf(request, slug):
    pdf_book = get_object_or_404(book, slug=slug, user=request.user)
    text = ""
    page_num = int(request.GET.get('page', 1))
    num_pages = 0
    audio_url = None
    
    #si le pdf n'est pas scanné et est fichier numérique utilise juste PyPDF2
    if pdf_book.file:
        pdf_file = pdf_book.file.open('rb')
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)
        if 1 <= page_num <= num_pages:
            page = reader.pages[page_num - 1]
            text = page.extract_text() or ""
            # Si pas de texte, tente l'OCR
            if not text.strip():
                pdf_file.seek(0)
                images = convert_from_bytes(pdf_file.read(), first_page=page_num, last_page=page_num)
                if images:
                    text = pytesseract.image_to_string(images[0], lang='fra')
        pdf_file.close()

    if request.GET.get('audio') == '1' and text:
        tts = gTTS(text, lang='fr')
        import io
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return FileResponse(audio_fp, as_attachment=False, content_type='audio/mpeg')
    
    audio_url = f"?page={page_num}&audio=1"
    
    return render(request, 'readpdf/audiopdf.html', context={'text': text, 'book': pdf_book, 'num_pages': num_pages,'current_page': page_num, 'audio_url':audio_url})