<p align="center">
  <img src="main/analytics/static/analytics/images/nachim-logo.png" alt="나침 로고" width="220" />
</p>

<h1 align="center">나침</h1>

<p align="center">
  스포츠 경험을 자격, 활동 기관, 일자리와 연결하는 체육지도자 커리어 플랫폼
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.13-3776AB?logo=python&amp;logoColor=white" alt="Python 3.13" /></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-6.1-092E20?logo=django&amp;logoColor=white" alt="Django 6.1" /></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-community_DB-4169E1?logo=postgresql&amp;logoColor=white" alt="PostgreSQL" /></a>
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/SQLite-analysis_DB-003B57?logo=sqlite&amp;logoColor=white" alt="SQLite" /></a>
</p>

## 목차

1. [팀 소개](#team)
2. [프로젝트 개요](#overview)
3. [기술 스택](#technology)
4. [WBS](#wbs)
5. [요구사항 명세서](#requirements)
6. [ERD](#erd)
7. [주요 프로시저](#procedure)
8. [수행결과·테스트·시연 페이지](#results)
9. [한 줄 회고](#retrospective)

---

<a id="team"></a>

## 1. 팀 소개

### 팀명

**나침**

### 팀원

| 이름 | GitHub | 주요 담당 |
|---|---|---|
| 이종연 | [@Leesannn](https://github.com/Leesannn) | 서비스 통합, PostgreSQL·배포, 고용24 연동 |
| 황유민 | [@HYM010219](https://github.com/HYM010219) | 자격·시험 정보, 채용 기능, 화면 구성 |
| 유성원 | [@ericsw2727](https://github.com/ericsw2727) | 공공데이터 정제, 분석 기능, 문서·UI 개선 |

### 멤버 개인 GitHub 계정과 연동

- 저장소: [github.com/Leesannn/Noanswer3Brothers](https://github.com/Leesannn/Noanswer3Brothers)
- 팀원별 작업 내용은 Git 커밋 이력으로 확인할 수 있습니다.
- 기능 단위 브랜치 작업 후 통합 브랜치에서 전체 서비스를 검증합니다.

<a id="overview"></a>

## 2. 프로젝트 개요

### 프로젝트명

**나침 - 스포츠 커리어 나침반**

나침은 사용자가 스포츠 분야에서 자신의 현재 위치를 확인하고 다음 진로를 찾도록 방향을 제시한다는 의미입니다.

### 프로젝트 소개

나침은 체육지도자를 준비하거나 활동 중인 사용자를 위해 **자격 취득 → 시험 준비 → 활동 기관 탐색 → 일자리·대타 활동 → 정보 공유**를 하나로 연결한 스포츠 커리어 플랫폼입니다.

관심 종목은 있지만 어떤 자격을 준비해야 할지 모르는 사용자에게는 자격 취득 방향을 추천하고, 이미 자격을 보유한 지도자에게는 종목·지역·요일·시간대에 맞는 활동 기관을 추천합니다. 프로그램과 지도자 현황을 분석하고, 고용24 채용공고와 단기 대타 공고, 커뮤니티까지 연결하여 진로 탐색 이후의 실제 활동도 지원합니다.

### 프로젝트 필요성·배경

- 체육지도자 자격, 시험 일정, 프로그램, 채용 정보가 여러 사이트에 분산되어 있습니다.
- 자격을 취득한 뒤에도 자신의 종목을 운영하는 기관과 지역을 찾기 어렵습니다.
- 공공데이터의 종목명과 지역명 형식이 달라 직접 비교하기 어렵습니다.
- 기관은 갑작스러운 강사 공백이 발생했을 때 적합한 대타 강사를 빠르게 찾기 어렵습니다.
- 자격 준비생과 현직 지도자가 시험·현장 정보를 나눌 공간이 필요합니다.
- 단순 정보 조회를 넘어 사용자의 조건에 맞는 다음 행동을 안내할 서비스가 필요합니다.

### 프로젝트 목표

1. 체육지도자 진입부터 실제 활동까지 이어지는 통합 진로 흐름을 제공합니다.
2. 보유 자격, 관심 종목, 지역, 대상, 시간 조건을 반영한 설명 가능한 추천을 제공합니다.
3. 자격·시험·프로그램·지도자·채용 데이터를 한곳에서 탐색하도록 구성합니다.
4. 지역별 프로그램 공급과 자격 취득 현황을 비교하여 활동 기회를 찾도록 돕습니다.
5. 기관과 지도자를 단기 대타 공고로 연결하고 현장 평판을 누적합니다.
6. 게시판과 댓글을 통해 시험·자격·현장 정보를 공유합니다.
7. 외부 데이터를 정제·갱신하여 서비스 기능에 안정적으로 제공합니다.

### 주요 사용자

| 사용자 | 주요 요구 | 제공 기능 |
|---|---|---|
| 체육지도자 입문자 | 어떤 종목과 자격을 준비해야 하는가 | 자격 방향 추천, 시험 정보, AI 교재 추천 |
| 자격 보유 지도자 | 어디에서 활동할 수 있는가 | 활동 기관 추천, 프로그램·기관 탐색 |
| 현직·프리랜서 강사 | 상시·단기 활동 기회를 찾고 싶다 | 고용24 일자리, 대타 공고 검색·지원 |
| 체육기관 담당자 | 지역 현황을 보고 강사를 모집하고 싶다 | 데이터 분석, 대타 공고 등록·신청자 관리 |
| 자격 준비생·동료 지도자 | 시험·현장 정보를 나누고 싶다 | 게시판, 댓글, 자료실, Q&A |

### 프로그램 전반의 주요 기능

| 영역 | 기능 | 주요 내용 |
|---|---|---|
| 맞춤 추천 | 자격 방향 추천 | 관심 종목·지역·경험·대상·시간대를 반영한 자격 방향 제시 |
| 맞춤 추천 | 활동 기관 추천 | 보유 자격·종목·이동 범위·요일·시간대 기반 기관 추천 |
| 자격·시험 | 자격 정보 | 9개 자격등급의 응시요건, 과목, 종목, 기관, 합격 기준 |
| 자격·시험 | 시험 일정 | 필기, 실기·구술, 연수, 최종 발표 일정 |
| 자격·시험 | AI 교재 추천 | 선택 자격과 필기 과목 기반 Gemini 교재 추천 |
| 데이터 분석 | 통합 대시보드 | 프로그램·기관·자격·신청 현황 핵심 지표 |
| 데이터 분석 | 지도자 현황 | 연도·지역·종목·자격 종류별 취득 현황 |
| 데이터 분석 | 프로그램 현황 | 운영 상태, 종목 매칭, 제외 사유와 정제 근거 |
| 데이터 분석 | 신청 현황 | 신청률 상·하위, 정원 마감, 종목·기관별 신청률 |
| 데이터 분석 | 수요·공급 비교 | 지역별 프로그램과 자격 취득 현황 비교 |
| 기관 탐색 | 기관 상세 | 운영 프로그램, 신청률, 활동 기회, Kakao 지도 |
| 일자리 | 고용24 채용공고 | 스포츠 직종 채용공고 검색과 원문 연결 |
| 대타 강사 | 공고 검색·지원 | 종목·지역·날짜·급여별 검색과 중복 지원 방지 |
| 대타 강사 | 기관 관리 | 공고 등록·수정·삭제, 신청자 확인, 현장 평가 |
| 커뮤니티 | 게시글·댓글 | 자유게시판, 시험정보, 자료실, 자격증 Q&A |
| 멘토링 | 진입 화면 | 향후 멘토 검색·신청 기능을 위한 출시 예정 화면 |

### 서비스 선순환 구조

~~~mermaid
flowchart LR
    A[관심 종목·지역 입력] --> B[맞춤 진로 추천]
    B --> C{관련 자격 보유}
    C -->|미보유| D[자격·시험 준비]
    D --> E[활동 기관 탐색]
    C -->|보유| E
    E --> F[일자리·대타 활동]
    F --> G[경력과 평판 축적]
    G --> H[커뮤니티 정보 공유]
    H --> B
~~~

<a id="technology"></a>

## 3. 기술 스택

| 영역 | 기술 | 사용 목적 |
|---|---|---|
| Backend | Python 3.13, Django 6.1.1 | 서비스 로직, ORM, 폼 검증, 관리 명령 |
| Frontend | Django Templates, HTML, CSS, JavaScript | 반응형 화면과 사용자 입력 |
| UI·Chart | Bootstrap, Chart.js | 레이아웃과 데이터 시각화 |
| AI | google-genai, Gemini | 자격별 시험 교재 추천 |
| Map | Kakao Maps JavaScript API | 기관 위치 표시 |
| Collection | requests, BeautifulSoup | KSPO·고용24 데이터 수집 |
| Data | pandas, openpyxl, Python csv | 공공데이터 검증·정규화 |
| Database | SQLite, PostgreSQL | 분석 데이터와 커뮤니티 데이터 분리 |
| Scheduling | APScheduler | 외부 데이터 정기 갱신 |
| Deployment | Gunicorn, Render, WhiteNoise | 운영 서버와 정적 파일 제공 |
| Test | Django TestCase, unittest.mock | 기능·파서·정제·예외 검증 |

### 시스템 아키텍처

~~~mermaid
flowchart TB
    User[사용자] --> Web[Django Templates]
    Web --> App[Django 서비스]

    subgraph Service[서비스 모듈]
        Recommend[맞춤 추천]
        Analytics[데이터 분석]
        Exam[자격·시험·AI 교재]
        Jobs[고용24 일자리]
        Substitute[대타 강사]
        Community[커뮤니티]
    end

    App --> Recommend
    App --> Analytics
    App --> Exam
    App --> Jobs
    App --> Substitute
    App --> Community

    Recommend --> SQLite[(SQLite)]
    Analytics --> SQLite
    Exam --> SQLite
    Exam --> Gemini[Gemini API]
    Analytics --> Kakao[Kakao Maps API]
    Jobs --> PostgreSQL[(PostgreSQL)]
    Substitute --> PostgreSQL
    Community --> PostgreSQL

    KSPO[KSPO] --> Pipeline[수집·정제 파이프라인]
    Work24[고용24] --> Pipeline
    PublicCSV[체육 공공데이터] --> Pipeline
    Pipeline --> SQLite
    Pipeline --> PostgreSQL
~~~

### 데이터베이스 구성

| 별칭 | 데이터베이스 | 저장 데이터 |
|---|---|---|
| default | SQLite | 종목, 자격 취득, 기관, 프로그램, 신청 현황, 시험 일정 |
| community | PostgreSQL | 게시글, 댓글, 고용24 공고, 대타 공고·지원·평판 |

Django DB Router가 앱별 저장소를 나누며, 사용자 화면에서는 두 데이터베이스의 결과를 하나의 서비스처럼 제공합니다.

### 프로젝트 구조

~~~text
main/
├─ recommendations/              # 자격·기관 맞춤 추천
│  ├─ forms.py
│  ├─ services.py
│  ├─ views.py
│  └─ templates/recommendations/
├─ analytics/                    # 대시보드·자격·프로그램·시험·수요공급
│  ├─ management/commands/
│  ├─ services/
│  ├─ templates/analytics/
│  └─ tests/
├─ jobs/                         # 고용24 채용공고
│  ├─ management/commands/
│  ├─ services/
│  └─ scheduler.py
├─ substitutes/                  # 대타 공고·지원·평판
├─ community/                    # 게시글·댓글
├─ data/                         # 자격정보와 서비스 데이터
├─ main/
│  ├─ settings.py
│  ├─ urls.py
│  └─ db_routers.py
├─ gunicorn.conf.py
├─ requirements.txt
└─ manage.py
~~~

### 외부 연동 서비스

- [국민체육진흥공단 체육지도자 자격검정](https://sqms.kspo.or.kr/)
- [고용24](https://www.work24.go.kr/)
- [Kakao Maps API](https://apis.map.kakao.com/)
- [Google Gemini API](https://ai.google.dev/)
- [GitHub 저장소](https://github.com/Leesannn/Noanswer3Brothers)

수집 데이터의 저작권과 이용 조건은 각 제공기관 정책을 따릅니다.

<a id="wbs"></a>

## 4. WBS

| 단계 | 작업 | 세부 내용 | 주요 산출물 | 상태 |
|---|---|---|---|:---:|
| 1 | 기획·요구 분석 | 사용자 유형, 진로 흐름, 필요 데이터 정의 | 서비스 기획서, 요구사항 | 완료 |
| 2 | 데이터 분석 | 자격·프로그램·기관·채용 데이터 구조 분석 | 데이터 항목표, 정규화 기준 | 완료 |
| 3 | 데이터 정제 | 지역·종목·기관명 정규화, 오류·중복 처리 | 정제 DB, 검토 CSV | 완료 |
| 4 | 추천 기능 | 자격 미보유·보유 사용자 추천 기준 구현 | 추천 폼, 점수 로직, 결과 화면 | 완료 |
| 5 | 분석 기능 | 대시보드, 지도자·프로그램·신청·수요공급 구현 | 분석 화면과 차트 | 완료 |
| 6 | 자격·시험 | 자격 안내, 시험 일정, AI 교재 추천 구현 | 시험정보 화면 | 완료 |
| 7 | 채용 기능 | 고용24 공고 검색·페이지네이션 구현 | 일자리 화면 | 완료 |
| 8 | 대타 기능 | 공고, 지원, 관리 링크, 평판 구현 | 대타 모집 서비스 | 완료 |
| 9 | 커뮤니티 | 게시글·댓글·비밀번호 확인 구현 | 커뮤니티 화면 | 완료 |
| 10 | 자동 갱신 | KSPO·고용24 수집과 정기 실행 구현 | 수집기, 스케줄러 | 완료 |
| 11 | UI 통합 | 공통 내비게이션, 반응형 디자인, 로고 적용 | 통합 웹 UI | 완료 |
| 12 | 테스트·배포 | 기능·데이터 테스트, 환경 변수, Render 배포 | 테스트 결과, 운영 서비스 | 진행 |

<a id="requirements"></a>

## 5. 요구사항 명세서

### 기능 요구사항

#### 맞춤 추천

| ID | 요구사항 | 구현 내용 |
|---|---|---|
| REC-01 | 자격 미보유 사용자가 관심 조건을 입력할 수 있어야 한다. | 지역, 주요·추가 종목, 경험, 대상, 시간대 입력 |
| REC-02 | 입력 조건에 맞는 자격 방향을 추천해야 한다. | 관심 종목, 지역, 신청률, 공급 부족도 점수화 |
| REC-03 | 자격 보유 사용자가 활동 조건을 입력할 수 있어야 한다. | 자격, 종목, 지역, 이동 범위, 대상, 요일, 시간대 입력 |
| REC-04 | 조건에 맞는 기관을 추천해야 한다. | 종목·지역·대상·신청률·대기자 기반 최대 5곳 |
| REC-05 | 사용자가 추천 근거를 확인할 수 있어야 한다. | 항목별 점수, 추천 이유, 부족 데이터 표시 |
| REC-06 | 같은 입력에 같은 결과를 제공해야 한다. | 결정론적 점수와 동점 정렬 기준 적용 |

#### 자격·시험

| ID | 요구사항 | 구현 내용 |
|---|---|---|
| LIC-01 | 9개 자격등급을 선택할 수 있어야 한다. | 자격등급 탭과 코드별 정보 |
| LIC-02 | 응시요건과 제출서류를 제공해야 한다. | 과정별 응시자격 경로 표시 |
| LIC-03 | 시험 과목과 기관 정보를 제공해야 한다. | 필기, 실기·구술, 검정·연수기관 |
| LIC-04 | 단계별 시험 일정을 제공해야 한다. | 접수·시험·합격 발표 일정 |
| LIC-05 | 선택 자격의 교재를 추천할 수 있어야 한다. | Gemini 추천과 서점 검색 링크 |
| LIC-06 | AI 요청을 제한하고 오류를 분리해야 한다. | IP 기준 분당 제한, JSON·API 오류 응답 |

#### 데이터 분석·탐색

| ID | 요구사항 | 구현 내용 |
|---|---|---|
| ANA-01 | 프로그램·기관·자격 현황을 요약해야 한다. | 통합 대시보드 지표 |
| ANA-02 | 연도·지역·종목·기관 조건으로 필터링해야 한다. | 공통 검색 필터 |
| ANA-03 | 지도자 자격 취득 현황을 시각화해야 한다. | 종목·연도·자격·지역별 차트와 표 |
| ANA-04 | 프로그램 운영 상태를 구분해야 한다. | 운영 중·예정·종료와 제외 사유 |
| ANA-05 | 프로그램 신청률을 비교해야 한다. | 상·하위, 마감, 종목·기관별 평균 |
| ANA-06 | 지역별 프로그램과 자격 취득 현황을 비교해야 한다. | 수요·공급 비교표와 근거 수치 |
| ANA-07 | 기관 상세 정보와 위치를 제공해야 한다. | 프로그램·신청률·활동 기회·Kakao 지도 |
| ANA-08 | 실제 데이터와 합성 데이터를 구분해야 한다. | 시뮬레이션 배지와 안내문 |

#### 일자리·대타 강사

| ID | 요구사항 | 구현 내용 |
|---|---|---|
| JOB-01 | 고용24 공고를 키워드와 지역으로 검색해야 한다. | 제목·기관명·지역 필터 |
| JOB-02 | 원문 공고로 이동할 수 있어야 한다. | 고용24 원문 링크 |
| SUB-01 | 대타 공고를 조건별로 검색해야 한다. | 종목·지역·날짜·급여·키워드·정렬 |
| SUB-02 | 기관 담당자가 대타 공고를 등록해야 한다. | 담당자 확인 후 날짜·시간·급여·자격 입력 |
| SUB-03 | 지도자가 공고에 지원할 수 있어야 한다. | 전화번호 기반 확인과 중복 지원 방지 |
| SUB-04 | 담당자가 신청자를 관리할 수 있어야 한다. | 서명된 관리 링크와 신청자 목록 |
| SUB-05 | 활동 후 평판을 기록할 수 있어야 한다. | 노쇼·컴플레인·긍정 태그·코멘트 |
| SUB-06 | 전화번호 원문을 저장하지 않아야 한다. | 해시와 마스킹 값만 보관 |

#### 커뮤니티

| ID | 요구사항 | 구현 내용 |
|---|---|---|
| COM-01 | 카테고리별 게시글을 제공해야 한다. | 자유, 시험정보, 자료실, 자격증 Q&A |
| COM-02 | 닉네임과 비밀번호로 글을 작성해야 한다. | 회원가입 없는 게시글 작성 |
| COM-03 | 작성자만 글을 수정·삭제해야 한다. | 저장된 비밀번호 해시 검증 |
| COM-04 | 게시글에 댓글을 작성·삭제해야 한다. | 댓글별 닉네임과 비밀번호 |
| COM-05 | 공지를 목록 상단에 고정해야 한다. | 관리자 공지 설정 |

### 비기능 요구사항

| ID | 요구사항 | 구현 |
|---|---|---|
| NFR-01 | 데스크톱과 모바일에서 사용할 수 있어야 한다. | 반응형 템플릿과 Bootstrap |
| NFR-02 | 비밀번호와 전화번호를 안전하게 저장해야 한다. | Django 비밀번호 해시, 전화번호 SHA-256·마스킹 |
| NFR-03 | 추천 결과가 설명 가능해야 한다. | 점수 구성, 추천 이유, 부족 데이터 표시 |
| NFR-04 | 대량 데이터를 페이지 단위로 제공해야 한다. | Django Paginator |
| NFR-05 | 외부 서비스 장애가 전체 화면을 중단시키지 않아야 한다. | DB·API 예외 처리와 빈 결과 화면 |
| NFR-06 | 서로 다른 데이터 저장소를 분리해야 한다. | SQLite·PostgreSQL DB Router |
| NFR-07 | 외부 데이터 실패 시 기존 데이터를 보존해야 한다. | 빈 결과·급감 방어와 트랜잭션 교체 |
| NFR-08 | 민감한 설정을 코드에 저장하지 않아야 한다. | 환경 변수와 .env |
| NFR-09 | 같은 공고에 중복 지원할 수 없어야 한다. | UniqueConstraint |
| NFR-10 | 다중 서버 worker의 중복 수집을 막아야 한다. | advisory lock, max_instances=1 |

<a id="erd"></a>

## 6. ERD

~~~mermaid
erDiagram
    CANONICAL_SPORT ||--o{ QUALIFICATION_AGGREGATE : has
    CANONICAL_SPORT ||--o{ PROGRAM : classifies
    INSTITUTION ||--o{ PROGRAM : operates
    PROGRAM ||--|| PROGRAM_CLEANUP : cleaned_as
    PROGRAM ||--o{ APPLICATION_STATUS : measured_by
    EXAM_FETCH_STATUS ||..o{ EXAM_SCHEDULE : tracks

    CANONICAL_SPORT ||--o{ SUBSTITUTE_POSTING : recruits
    CENTER_CONTACT ||--o{ SUBSTITUTE_POSTING : creates
    SUBSTITUTE_POSTING ||--o{ SUBSTITUTE_APPLICATION : receives
    PHONE_IDENTITY ||--o{ SUBSTITUTE_APPLICATION : applies
    PHONE_IDENTITY ||--o{ REPUTATION_RECORD : accumulates

    COMMUNITY_POST ||--o{ COMMENT : contains
    WORK24_FETCH_STATUS ||..o{ EXTERNAL_JOB_POSTING : tracks

    CANONICAL_SPORT {
        bigint id PK
        string name
        string normalized_name UK
        bigint qualification_count
    }
    QUALIFICATION_AGGREGATE {
        bigint id PK
        int acquisition_year
        string normalized_region
        string normalized_sport
        string qualification_type
        string grade
        int acquisition_count
    }
    INSTITUTION {
        bigint id PK
        string name
        string region
        string normalized_region
        string address
    }
    PROGRAM {
        bigint id PK
        string source_key UK
        bigint institution_id FK
        bigint matched_sport_id FK
        string name
        string target
        date start_date
        date end_date
    }
    PROGRAM_CLEANUP {
        bigint id PK
        bigint program_id FK
        string operating_status
        boolean is_usable
        string exclusion_reason
    }
    APPLICATION_STATUS {
        bigint id PK
        bigint program_id FK
        int capacity
        int applicants
        int waitlist
        boolean is_synthetic
    }
    SUBSTITUTE_POSTING {
        bigint id PK
        bigint manager_id FK
        bigint sport_id FK
        date work_date
        int pay_amount
        string status
    }
    PHONE_IDENTITY {
        bigint id PK
        string phone_hash UK
        string phone_masked
        string password_hash
    }
    REPUTATION_RECORD {
        bigint id PK
        bigint phone_identity_id FK
        boolean is_no_show
        boolean is_complaint
        json positive_tags
    }
    COMMUNITY_POST {
        bigint id PK
        string category
        string title
        string nickname
        string password_hash
    }
    COMMENT {
        bigint id PK
        bigint post_id FK
        string nickname
        string password_hash
    }
~~~

### 데이터 저장 구조

| 데이터베이스 | 주요 엔터티 |
|---|---|
| SQLite | CanonicalSport, QualificationAggregate, Institution, Program, ProgramCleanup, ApplicationStatus, ExamSchedule |
| PostgreSQL | ExternalJobPosting, Work24FetchStatus, Post, Comment, CenterContact, Posting, Application, ReputationRecord |

<a id="procedure"></a>

## 7. 주요 프로시저

### 7-1. 자격 미보유자 추천

~~~mermaid
flowchart LR
    A[지역·관심 종목·경험 입력] --> B[운영 프로그램 조회]
    B --> C[관심 종목 일치 계산]
    C --> D[지역·신청률 계산]
    D --> E[프로그램 공급 부족도 계산]
    E --> F[지도 대상 일치 계산]
    F --> G[총점·추천 이유 생성]
    G --> H[상위 5개 자격 방향]
~~~

| 평가 요소 | 최대 점수 | 기준 |
|---|---:|---|
| 관심 종목 일치 | 35점 | 주요·추가 관심 종목 |
| 지역 일치 | 20점 | 희망 지역 내 운영 프로그램 |
| 지역 평균 신청률 | 20점 | 최근 신청률 구간 |
| 프로그램 공급 부족도 | 15점 | 지역 또는 전국 중앙값과 비교 |
| 지도 대상 일치 | 10점 | 희망 대상 프로그램 존재 |

지역 자료가 없으면 전국 데이터를 사용하고 그 사실을 결과에 표시합니다. 동점은 관심 종목, 지역, 신청률, 종목명 순으로 정렬합니다.

### 7-2. 자격 보유자 기관 추천

~~~mermaid
flowchart LR
    A[자격·종목·활동 조건 입력] --> B[운영 기관 후보 조회]
    B --> C[종목·지역 점수]
    C --> D[지도 대상 점수]
    D --> E[신청률·대기자 점수]
    E --> F[요일·시간 일치 확인]
    F --> G[추천 이유·부족 데이터 생성]
    G --> H[상위 5개 기관]
~~~

| 평가 요소 | 최대 점수 | 기준 |
|---|---:|---|
| 종목 일치 | 40점 | 정확 일치 또는 정규화된 유사 종목 |
| 지역 일치 | 25점 | 시·군·구, 시·도, 지역 무관 |
| 지도 대상 일치 | 10점 | 선택 대상과 프로그램 대상 |
| 최근 평균 신청률 | 15점 | 최근 신청률 구간 |
| 대기자 발생 | 10점 | 최근 대기 인원 발생 여부 |

요일과 시간대는 추천 이유로 추가하며, 값이 없는 항목은 임의로 추정하지 않습니다.

### 7-3. 자격·시험과 AI 교재 추천

1. 사용자가 9개 자격등급 중 하나를 선택합니다.
2. 자격 정의, 응시 경로, 제출서류, 필기 과목과 기관을 불러옵니다.
3. 자격 코드로 단계별 시험 일정을 그룹화합니다.
4. AI 교재 추천 요청 시 자격명과 필기 과목을 Gemini에 전달합니다.
5. 교재 제목·저자·추천 이유를 구조화하여 서점 검색 링크와 표시합니다.
6. IP당 1분 6회로 요청을 제한하고 오류는 JSON 응답으로 처리합니다.

### 7-4. 데이터 분석

1. 연도·지역·종목·기관·대상·검색어 필터를 적용합니다.
2. 프로그램 정리 결과에서 운영 중이고 분석 가능한 항목을 선택합니다.
3. 자격 취득 건수, 프로그램·기관 수, 정원·신청 인원을 집계합니다.
4. 신청률 상·하위와 정원 마감 프로그램을 구합니다.
5. 지역별 프로그램 수와 자격 취득 건수를 비교합니다.
6. 실제 신청 자료가 없으면 합성 데이터임을 표시한 뒤 시연 자료를 사용합니다.

### 7-5. 고용24 일자리

1. 직종 코드 059의 스포츠·레크리에이션 공고를 저장합니다.
2. 사용자의 검색어를 공백 단위로 나누어 제목과 기관명에 적용합니다.
3. 지역 조건을 별도 적용합니다.
4. 결과를 20개 단위로 페이지네이션합니다.
5. 외부 PostgreSQL 장애 시 페이지 전체가 실패하지 않도록 빈 목록을 반환합니다.

### 7-6. 대타 강사 모집

~~~mermaid
flowchart LR
    A[기관 담당자 확인] --> B[대타 공고 등록]
    B --> C[관리 링크 발급]
    C --> D[지도자 검색·지원]
    D --> E{중복·마감·자격 확인}
    E -->|통과| F[신청 저장]
    E -->|실패| G[사유 안내]
    F --> H[담당자 신청자 확인]
    H --> I[활동 후 평판 기록]
~~~

- 담당자와 신청자의 원문 전화번호는 저장하지 않습니다.
- 같은 전화번호는 최초 설정한 비밀번호로 다시 확인합니다.
- 같은 공고와 전화번호 조합의 중복 신청을 DB 제약으로 방지합니다.
- 관리 링크는 공고 ID가 서명된 토큰으로 보호합니다.
- 평판은 노쇼, 컴플레인과 긍정 태그를 기간별로 집계합니다.
- 허위·오류 평판은 삭제하지 않고 관리자 사유와 함께 숨김 처리합니다.
- 현재 자격증 보유 검증은 실제 회원·자격 DB 연동 전 단계의 모의 구현입니다.

### 7-7. 커뮤니티

1. 사용자가 카테고리, 제목, 닉네임, 비밀번호, 내용을 입력합니다.
2. 비밀번호는 Django 해시로 변환해 저장합니다.
3. 게시글 상세 조회 시 조회수를 증가시킵니다.
4. 댓글도 별도 닉네임과 비밀번호로 작성합니다.
5. 글 수정·삭제와 댓글 삭제 시 해당 비밀번호를 검증합니다.
6. 관리자 공지는 일반 글보다 먼저 표시합니다.

### 7-8. 외부 데이터 갱신

~~~mermaid
flowchart LR
    A[KSPO·고용24·공공 CSV] --> B[수집]
    B --> C[형식·결측·중복 검증]
    C --> D[지역·종목·기관명 정규화]
    D --> E[종목 매칭]
    E --> F[SQLite·PostgreSQL 적재]
    F --> G[추천·분석·일자리 화면]
~~~

수집 결과가 비었거나 비정상적으로 줄면 기존 데이터를 유지합니다. 스케줄러는 고용24를 매일 03:00, KSPO 시험 일정을 매일 00:00·12:00에 갱신합니다.

<a id="results"></a>

## 8. 수행결과·테스트·시연 페이지

### 수행결과

2026-09-29 로컬 스냅샷 기준입니다.

| 데이터 | 적재·생성 건수 |
|---|---:|
| 기준 스포츠 종목 | 113개 |
| 자격 취득 집계 | 17,467건 |
| 기관 | 376개 |
| 전체 프로그램 | 204,461건 |
| 운영 중·분석 가능 프로그램 | 9,377건 |
| 운영 종료 프로그램 | 176,619건 |
| 운영 예정 프로그램 | 18,465건 |
| 자격등급 | 9개 |
| 응시자격 경로 | 48건 |
| 시험 일정 | 388건 |
| 고용24 채용공고 | 개발 확인 기준 934건 |

### 시연 페이지

| 기능 | 경로 | 확인 내용 |
|---|---|---|
| 서비스 홈 | /recommendations/ | 서비스 소개와 추천 경로 |
| 자격 방향 추천 | /recommendations/unlicensed/ | 미보유자 조건 입력과 결과 |
| 활동 기관 추천 | /recommendations/licensed/ | 보유자 조건 입력과 결과 |
| 통합 대시보드 | /dashboard/ | 프로그램·기관·신청 핵심 지표 |
| 지도자 현황 | /instructors/ | 자격 취득 차트와 집계표 |
| 자격·시험 정보 | /exam-info/ | 응시요건·일정·AI 교재 |
| 프로그램 현황 | /current-programs/ | 운영 상태와 정제 근거 |
| 신청 현황 | /applications/ | 신청률 분석 |
| 수요·공급 분석 | /demand-supply/ | 지역별 프로그램·자격 비교 |
| 커뮤니티 | /community/ | 게시판·댓글 |
| 고용24 일자리 | /community/jobs/ | 채용공고 검색 |
| 대타 강사 모집 | /community/substitutes/ | 공고·지원·관리 |
| 관리자 | /admin/ | 데이터와 갱신 상태 관리 |

### 실행 방법

명령은 <code>manage.py</code>가 있는 <code>main</code> 디렉터리에서 실행합니다.

#### Windows

~~~powershell
cd main
py -3.13 -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py migrate --database=community
python manage.py runserver
~~~

#### macOS·Linux

~~~bash
cd main
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py migrate --database=community
python manage.py runserver
~~~

#### 주요 환경 변수

~~~dotenv
SECRET_KEY=replace_with_a_random_secret

COMMUNITY_DB_NAME=community_db
COMMUNITY_DB_USER=community_user
COMMUNITY_DB_PASSWORD=replace_with_your_password
COMMUNITY_DB_HOST=127.0.0.1
COMMUNITY_DB_PORT=5432

KAKAO_MAP_APP_KEY=replace_with_your_kakao_javascript_key
GEMINI_API_KEY=replace_with_your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash

ENABLE_APSCHEDULER=false
~~~

### 테스트

~~~powershell
python manage.py check
python manage.py test
~~~

핵심 데이터 처리 테스트:

~~~powershell
python manage.py test analytics.tests.test_kspo_crawler analytics.tests.test_clean_database_builder analytics.tests.test_sport_matching
~~~

확인 항목:

- 추천 점수, 지역·종목 일치, 정렬 결정성
- 추천 페이지 공개 접근과 빈 결과 처리
- 합성 데이터 사용 안내
- 고용24 키워드·지역 필터와 페이지네이션
- 시험 일정·고용24 스케줄 실행 조건
- HTML 파싱과 외부 요청 오류
- CSV 인코딩·필수 컬럼·중복·날짜·숫자
- 프로그램 운영 상태와 종목 매칭
- SQLite 무결성

커뮤니티의 글·댓글 작성과 비밀번호 확인, 대타 공고 등록·지원·관리 링크·평판 기록은 각 화면의 사용자 흐름으로 시연할 수 있습니다.

### 데이터 해석과 현재 제약사항

- 자격 취득 건수는 현재 활동 중인 지도자 수와 같지 않습니다.
- 프로그램 수와 자격 취득 건수만으로 실제 인력 부족을 확정할 수 없습니다.
- 신청 현황의 시연용 합성 데이터는 화면에서 별도로 표시합니다.
- 추천 결과는 현재 적재 데이터에 따른 탐색 보조 정보입니다.
- 대타 지원의 자격 확인은 모의 구현이며 실제 자격 DB 연동이 필요합니다.
- 멘토링은 현재 출시 예정 화면만 제공합니다.
- 고용24 공고의 실제 마감 여부와 조건은 원문에서 다시 확인해야 합니다.

<a id="retrospective"></a>

## 9. 한 줄 회고

| 팀원 | 한 줄 회고 |
|---|---|
| 이종연 | 많은 양의 데이터를 정제하는 일이 생각보다 복잡하고 어려웠지만 매일 일정 시간마다 크롤링을 하는 파이프라인을 구축하는것이 흥미롭고 재미있었다. |
| 황유민 | 첫 프로젝트를 진행하며 처음에 생각했던 대로 되지 않았던 부분들도 많았지만 데이터를 크롤링하고 가져오기도 하고 가져온 데이터를 사용해보고 전체적인 구조를 짜며 웹을 만들어보며 고민해본 경험을 했고 다음 프로젝트때는 더 원활하게 진행될 수 있을 것 같습니다. |
| 유성원 | 데이터를 자동으로 수집하고 적재하는 과정을 배웠습니다. 자동화 기술 뿐만 아니라 이렇게 쌓인 많은 양의 데이터를 정제하고 가공하는 과정 또한 중요하다는 것을 깨닫게 되었습니다. |
