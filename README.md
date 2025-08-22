# 📚 Quizly: PDF & 오디오 강의 요약 + 퀴즈 생성 웹서비스

**Quizly**는 강의 자료(PDF)와 오디오 강의를 자동으로 요약하고, 강조된 내용을 바탕으로 퀴즈까지 생성해주는 Django 기반의 웹서비스입니다.

---

## 🚀 주요 기능

| 기능 | 설명 |
|------|------|
| 📘 PDF 요약 | Gemini API로 강의 자료 요약 |
| 🎧 오디오 요약 | Whisper로 음성 인식 후 요약 |
| ✅ 의미 강조 | PDF 요약과 오디오 요약 간 유사 문장 강조 |
| 🧠 퀴즈 생성 | 강조 문장을 기반으로 객관식, OX, 빈칸 퀴즈 자동 생성 |
| 📥 다운로드 제공 | 모든 결과 텍스트 파일로 저장 및 다운로드 가능 |
| 🔔 알림 지원 | 각 단계 완료 시 alert 알림 팝업 제공 |

---

## 🛠️ 사용 방법

1. **웹페이지 접속 후 파일 업로드**
   - `📘 PDF 업로드 및 요약`: PDF 파일 업로드 후 핵심 내용 요약
   - `🎧 오디오 업로드 및 요약`: m4a/mp3 파일 업로드 후 텍스트화 및 요약
   - `🧠 PDF + 오디오 요약`: 두 파일을 동시에 요약하고 통합 처리

2. **요약 결과 표시 및 파일 다운로드**
   - 업로드 후 웹페이지에 요약 결과 표시
   - 다음 결과 파일을 다운로드할 수 있습니다:
     - `summary.txt`: PDF 요약 결과
     - `recording_summary.txt`: 오디오 요약 결과
     - `recording_summary_highlighted.txt`: ✅ 강조 포함 오디오 요약
     - `generated_quiz.txt`: 자동 생성된 퀴즈

3. **의미 유사 문장 강조 (✅)**
   - PDF와 오디오 요약 간 의미 유사한 문장을 판단하여 오디오 요약에서 강조

4. **퀴즈 자동 생성**
   - ✅ 강조 문장을 바탕으로 다양한 유형의 퀴즈 5개 생성:
     - 객관식 4지선다
     - O/X 퀴즈
     - 빈칸 채우기

---

## 📂 프로젝트 구조

Quizly_django/   
├── quizly_app/   
│   ├── forms.py   
│   ├── views.py   
│   ├── templates/   
│   │   └── upload.html   
├── media/   
│   ├── summary.txt   
│   ├── recording_summary.txt   
│   ├── recording_summary_highlighted.txt   
│   ├── generated_quiz.txt   
├── manage.py   
├── requirements.txt   
└── .env   

---
## ✅ 설치 및 실행 방법

```bash
# 1. 가상환경 설정
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. 라이브러리 설치
pip install -r requirements.txt

# 3. Django 서버 실행
python manage.py runserver








