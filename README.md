# 3일 미니프로젝트

## 자세한 발표 내용
https://docs.google.com/presentation/d/1VLmCHjaWDqAz_kyOshTMrtB0ZM41ctZk_6xLuwlO3nE/edit?usp=drive_link

## Jungle GYM
Jungle GYM is an application that helps you find your running mate.

## 설치
```
# Create venv
python3 -m venv .venv

# Run venv (window, Powershell)
.\venv\Scripts\activate

# Run venv (mac)
. .venv/bin/activate

# Install Packages
pip install Flask
pip install pymongo
pip install Jinja2
pip install python-dotenv
pip install wtforms
pip install flask_jwt_extended
pip install flask_pymongo
pip install flask_wt
pip install requests



# Run
flask run
```

## 파일 구조

```
JungleGYM/
├── app/
│   ├── __init__.py           # Flask 앱 초기화 및 설정
│   ├── auth/                 # 인증 관련 기능 (로그인, 회원가입)
│   │   ├── __init__.py       # 블루프린트 등록
│   │   ├── routes.py         # 로그인, 회원가입 관련 라우트
│   │   ├── forms.py          # 로그인, 회원가입 폼 정의
│   │   ├── models.py         # 사용자 데이터베이스 모델
│   │   ├── services.py       # 인증 관련 비즈니스 로직
│   │   └── templates/        # 인증 관련 템플릿
│   │       ├── login.html
│   │       ├── register.html
│   ├── meetings/             # 모임 관련 기능 (모임 개설, 리스트, 수정, 삭제)
│   │   ├── __init__.py       # 블루프린트 등록
│   │   ├── routes.py         # 모임 관련 라우트
│   │   ├── forms.py          # 모임 생성 및 수정 폼 정의
│   │   ├── models.py         # 모임 데이터베이스 모델
│   │   ├── services.py       # 모임 관련 비즈니스 로직
│   │   └── templates/        # 모임 관련 템플릿
│   │       ├── createAndModify.html   # 모임 개설 + 수정 페이지
│   │       ├── listAndDetail.html     # 모임 리스트(카드 형식) + 상세 페이지(모달 형식)
│   ├── ranking/              # 활동량 랭킹 페이지
│   │   ├── __init__.py       # 블루프린트 등록
│   │   ├── routes.py         # 랭킹 페이지 라우트
│   │   ├── models.py         # 랭킹 관련 데이터 처리
│   │   ├── services.py       # 랭킹 관련 비즈니스 로직
│   │   └── templates/        # 랭킹 관련 템플릿
│   │       └── ranking.html  # 랭킹 페이지
│   ├── static/               # 정적 파일 (CSS, JS, 이미지 등)
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── img/
│   │       └── logo.png
│   └── templates/            # 공통 템플릿
│       ├── index.html        # 홈 페이지 템플릿
├── venv/                     # 가상 환경
└── run.py                    # 애플리케이션 실행 진입점
```
