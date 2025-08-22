# quizly_app/quizly/forms.py

from django import forms

class UploadForm(forms.Form):
    pdf_file = forms.FileField(
        label="📄 PDF 파일 업로드",
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf'})
    )

    audio_file = forms.FileField(
        label="🎤 녹음 파일 업로드 (예: m4a, mp3)",
        required=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.m4a,.mp3'})
    )

    transcript_txt = forms.FileField(
        label="📝 요약 텍스트(txt) 업로드 (선택)",
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': '.txt'})
    )
