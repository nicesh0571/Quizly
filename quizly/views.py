import os
import pdfplumber
import whisper
from dotenv import load_dotenv
import google.generativeai as genai
from tqdm import tqdm

from django.shortcuts import render
from django.core.files.storage import default_storage
from django.contrib import messages
from django.conf import settings
from .forms import UploadForm

# ✅ 환경변수 및 Gemini 모델 설정
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ✅ Whisper 모델 로딩
asr_model = whisper.load_model("small")

def upload_files(request):
    pdf_summary = None
    audio_summary = None

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        action = request.POST.get("action")

        if form.is_valid():
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            # ===== 📘 PDF 요약 =====
            if action in ["pdf", "both"] and "pdf_file" in request.FILES:
                pdf_file = request.FILES["pdf_file"]
                saved_path = default_storage.save(pdf_file.name, pdf_file)
                file_path = os.path.join(default_storage.location, saved_path)

                full_text = ""
                with pdfplumber.open(file_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            full_text += f"\n--- [페이지 {i+1}] ---\n{text}"

                prompt = f"다음은 이미지 필터링 강의 PDF에서 추출한 텍스트입니다. 핵심 내용을 구체적으로 **한국어로** 요약해 주세요:\n\n{full_text}"
                response = model.generate_content(prompt)
                pdf_summary = response.text.strip()

                with open(os.path.join(settings.MEDIA_ROOT, "summary.txt"), "w", encoding="utf-8") as f:
                    f.write(pdf_summary)

                messages.success(request, "✅ PDF 요약이 완료되었습니다!")

            # ===== 🎧 오디오 요약 =====
            if action in ["audio", "both"] and "audio_file" in request.FILES:
                audio_file = request.FILES["audio_file"]
                saved_path = default_storage.save(audio_file.name, audio_file)
                audio_path = os.path.join(default_storage.location, saved_path)

                result = asr_model.transcribe(audio_path, language="ko")
                transcript_text = result["text"]

                prompt = f"다음은 강의 녹취록입니다. 핵심 내용을 구체적으로 **한국어로** 요약해 주세요:\n\n{transcript_text}"
                response = model.generate_content(prompt)
                audio_summary = response.text.strip()

                with open(os.path.join(settings.MEDIA_ROOT, "recording_summary.txt"), "w", encoding="utf-8") as f:
                    f.write(audio_summary)

                messages.success(request, "✅ 오디오 요약이 완료되었습니다!")

            # ===== ✅ 중요 문장 강조 및 퀴즈 생성 =====
            if pdf_summary and audio_summary:
                with open(os.path.join(settings.MEDIA_ROOT, "summary.txt"), "r", encoding="utf-8") as f:
                    summary_sentences = [line.strip() for line in f if line.strip()]

                with open(os.path.join(settings.MEDIA_ROOT, "recording_summary.txt"), "r", encoding="utf-8") as f:
                    recording_sentences = [line.strip() for line in f if line.strip()]

                highlight_set = set()
                for r_line in tqdm(recording_sentences, desc="🔍 Gemini로 의미 유사도 평가 중"):
                    for s_line in summary_sentences:
                        prompt = f"""
다음 두 문장이 의미상 유사한 경우에만 "1"을 출력하세요.  
의미가 다르면 "0"을 출력하세요.  
문장은 순서나 표현이 달라도 의미가 같으면 유사하다고 간주하세요.

문장 A: "{r_line}"  
문장 B: "{s_line}"

숫자 하나만 출력하세요.
"""
                        try:
                            response = model.generate_content(prompt)
                            score = response.text.strip()
                            if score == "1":
                                highlight_set.add(r_line)
                                break
                        except:
                            continue

                highlighted_lines = []
                for line in recording_sentences:
                    if line in highlight_set:
                        highlighted_lines.append(f"✅ {line}")
                    else:
                        highlighted_lines.append(line)

                with open(os.path.join(settings.MEDIA_ROOT, "recording_summary_highlighted.txt"), "w", encoding="utf-8") as f:
                    f.write("\n".join(highlighted_lines))

                messages.success(request, "✅ 중요 문장 강조가 완료되었습니다!")

                # ===== 🧠 퀴즈 생성 =====
                quiz_prompt = f"""
다음은 강의 요약 텍스트입니다.  
- ✅ 표시된 문장은 반드시 퀴즈 문제에 포함되도록 해주세요.  
- 그 외 문장들은 선택적으로 반영해도 됩니다.
- 문제는 총 5문제로 구성해주세요.
- 각 문항에 정답도 함께 작성해주세요.
- 한국어로 출력해주세요.

1. 객관식 (보기 4개)
2. 참/거짓
3. 빈칸 채우기

퀴즈는 다음과 같은 형식으로 출력해 주세요:

Q1. [질문 내용]
A) 보기1
B) 보기2
C) 보기3
D) 보기4
정답: [정답]

또는

Q2. [질문 내용] (O/X)
정답: [정답]

또는

Q3. [____에 들어갈 알맞은 말은?]
정답: [정답]

다음은 강조된 요약입니다:
{os.linesep.join(highlighted_lines)}
"""
                try:
                    quiz_response = model.generate_content(quiz_prompt)
                    quiz_text = quiz_response.text.strip()
                    with open(os.path.join(settings.MEDIA_ROOT, "generated_quiz.txt"), "w", encoding="utf-8") as f:
                        f.write(quiz_text)
                    messages.success(request, "🧠 퀴즈 생성이 완료되었습니다!")
                except Exception as e:
                    messages.error(request, f"❌ 퀴즈 생성 중 오류 발생: {e}")

    else:
        form = UploadForm()

    return render(request, "upload.html", {
        "form": form,
        "pdf_summary": pdf_summary,
        "audio_summary": audio_summary,
    })
