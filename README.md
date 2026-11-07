# kitup-backend
멋쟁이사자처럼 4호선톤 kitup 백엔드 레포지토리입니다.

## 처음 설정

`.python-version`에 적힌 버전의 [Python](https://www.python.org/downloads/)과 Docker Desktop을 먼저 설치합니다.

DB 설정은 `.env.example`의 개발용 기본값을 그대로 사용합니다.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
Copy-Item .env.example .env       # macOS/Linux: cp .env.example .env (기존 .env가 있으면 생략)
```

## 실행

Docker Desktop을 켠 뒤 실행합니다.

```powershell
.\.venv\Scripts\Activate.ps1     # macOS/Linux: source .venv/bin/activate
docker compose -f compose.dev.yaml up -d --wait db
python manage.py migrate
python manage.py runserver
```

## 개발 DB

PostgreSQL 18.6은 `compose.dev.yaml`로, Django는 PC의 가상환경에서 실행합니다.

- 접속 설정: `.env`
- 종료: `docker compose -f compose.dev.yaml stop db`
- DB를 종료해도 데이터는 유지됩니다.
- `docker compose -f compose.dev.yaml down -v`는 데이터를 삭제합니다.

## 구조

```
kitup-backend/
├── manage.py
├── requirements.txt
├── .env.example
│
├── config/
│   ├── settings/
│   │   ├── base.py                 # 공통 설정
│   │   ├── local.py                # 개발 (PostgreSQL)
│   │   └── prod.py                 # 배포 (postgres)
│   ├── urls.py                     # 루트 URL
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                           # 공통 모듈
│   ├── models.py                   # TimeStampedModel
│   ├── choices.py                  # TestStatus(계산용), CostMethod, CostSource,
│   │                               # Channel, OrderStatus, RecommendationStatus
│   ├── constants.py                # 수수료 9.8%, 배달비 3,200, 포장비 1,000,
│   │                               # 운영 시간·재료 단위 선택지
│   ├── responses.py                # 공통 응답 포맷
│   ├── exceptions.py               # 커스텀 예외(409 등) + 핸들러
│   ├── pagination.py
│   └── calc/                       # 순수 계산 함수 (FE와 같은 공식)
│       ├── margin.py               # 채널별 변동비·건당 공헌이익
│       └── aggregate.py            # 시간대별/일별/채널별 집계
│
├── ai/                             # LLM 호출 래퍼 (앱 아님)
│   ├── client.py
│   ├── schemas.py                  # AI 응답 JSON 검증
│   └── prompts/
│       ├── ingredient_estimate.py  # 재료·원가 추정
│       ├── review_analysis.py      # 리뷰 분류
│       └── recommendation.py       # 보고서 형태 개선안
│
├── menu_tests/                     # 테스트 생성, 재료, 원가
│   ├── models.py                   # MenuTest, Ingredient
│   ├── services/
│   │   ├── cost_service.py         # 식재료비 합산, 원가 수정, Freeze 검사
│   │   └── ai_estimate_service.py  # AI 재료 원가 추정
│   ├── serializers.py / views.py / urls.py
│   └── tests/
│
├── orders/                         # 주문·리뷰
│   ├── models.py                   # Order, Review
│   ├── fixtures/
│   │   └── sample_package.json     # 가상 주문·리뷰, 공유주방·운영 기간
│   ├── services/
│   │   └── import_service.py       # 데이터 불러오기 (= 운영 시작)
│   ├── serializers.py / views.py / urls.py
│   └── tests/
│
├── dashboard/                      # 대시보드 (모델 없음, 집계만)
│   ├── services/
│   │   └── metrics.py
│   ├── serializers.py / views.py / urls.py
│   └── tests/
│
└── reports/                        # 리포트
    ├── models.py                   # Report
    ├── services/
    │   ├── report_builder.py       # 리포트 생성 순서 관리
    │   ├── review_analysis.py      # 리뷰 분류 -> Review 칼럼 저장
    │   └── recommendation.py       # 개선안 생성·저장, retry
    ├── serializers.py / views.py / urls.py
    └── tests/
```

## URL

```
/api/tests/                          → menu_tests.urls
/api/tests/{test_id}/orders/         → orders.urls
/api/tests/{test_id}/dashboard/      → dashboard.urls
/api/tests/{test_id}/report/         → reports.urls
```
