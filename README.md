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

## 나침이란?

**나침**은 스포츠 분야에서 다음 진로를 찾는 사람에게 방향을 제시하는 커리어 나침반입니다.

관심 종목은 있지만 어떤 자격을 준비해야 할지 모르는 사람에게는 **자격 취득 방향**을, 이미 자격을 가진 지도자에게는 **활동할 기관과 프로그램**을 추천합니다. 이후 시험 준비, 지역 현황 분석, 일자리 탐색, 대타 강사 지원, 동료와의 정보 교류까지 하나의 서비스 안에서 이어집니다.

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

## 목차

1. [팀 소개](#team)
2. [프로젝트 개요](#overview)
3. [주요 기능](#features)
4. [사용자별 이용 흐름](#user-flow)
5. [맞춤 추천 기준](#recommendation)
6. [기술 스택과 아키텍처](#technology)
7. [데이터 구조](#data)
8. [실행 방법](#run)
9. [데이터 수집과 운영](#pipeline)
10. [테스트와 현재 제약사항](#quality)
- [프로젝트 구조와 출처](#appendix)

---

<a id="team"></a>

## 1. 팀 소개

**팀명: 오답삼형제**

| 팀원 | GitHub | 주요 담당 |
|---|---|---|
| Leesannn | [@Leesannn](https://github.com/Leesannn) | 서비스 통합, PostgreSQL·배포, 고용24 연동 |
| HYM010219 | [@HYM010219](https://github.com/HYM010219) | 자격·시험 정보, 채용 기능, 화면 구성 |
| ericsw2727 | [@ericsw2727](https://github.com/ericsw2727) | 공공데이터 정제, 분석 기능, 문서·UI 개선 |

<a id="overview"></a>

## 2. 프로젝트 개요

### 해결하려는 문제

체육지도자를 준비하거나 활동 중인 사용자는 자격제도, 시험 일정, 지역 프로그램, 채용공고를 서로 다른 사이트에서 찾아야 합니다. 자격을 취득한 뒤에도 어떤 기관에서 자신의 종목을 운영하는지, 어느 지역에 기회가 있는지 파악하기 어렵습니다.

기관 역시 갑작스러운 강사 공백이 생겼을 때 자격과 활동 이력을 확인하면서 빠르게 대타를 구할 수단이 부족합니다.

나침은 다음 정보를 하나의 흐름으로 연결합니다.

- 체육지도자 자격 종류와 시험 일정
- 종목·지역별 프로그램과 운영 기관
- 자격 취득 현황과 프로그램 공급 비교
- 고용24 스포츠 채용공고
- 단기 대타 강사 모집과 지원
- 시험·자격·현장 경험을 나누는 커뮤니티

### 핵심 사용자

| 사용자 | 필요한 정보 | 나침이 제공하는 기능 |
|---|---|---|
| 체육지도자 입문자 | 어떤 자격과 종목을 준비할지 | 관심 종목 기반 자격 방향 추천, 시험 정보, AI 교재 추천 |
| 자격 보유 지도자 | 어디에서 활동할 수 있을지 | 조건 기반 기관 추천, 프로그램·기관 상세, 채용공고 |
| 현직·프리랜서 강사 | 단기·상시 활동 기회 | 고용24 일자리 검색, 대타 공고 검색·지원 |
| 체육기관 담당자 | 프로그램 현황과 강사 수급 | 지역 분석, 대타 공고 등록, 신청자 관리·평가 |
| 자격 준비생·동료 지도자 | 실제 정보와 자료 공유 | 시험정보·자료실·Q&A·자유게시판 |

### 서비스가 연결하는 데이터

| 데이터 | 서비스 활용 |
|---|---|
| 체육 프로그램 | 운영 기관 추천, 프로그램 탐색, 지역별 공급 분석 |
| 자격 취득 집계 | 종목별 지도자 현황, 자격 방향 추천, 수요·공급 비교 |
| KSPO 자격·시험 정보 | 응시요건, 시험 과목, 일정, 결격사유 안내 |
| 프로그램 신청 현황 | 추천 점수, 신청률 분석, 증설·개선 판단 참고 |
| 고용24 채용공고 | 스포츠 일자리 검색과 원문 연결 |
| 대타 공고·평판 | 단기 강사 연결, 신청 이력과 현장 평가 |
| 게시글·댓글 | 시험·자격·현장 정보 교류 |

<a id="features"></a>

## 3. 주요 기능

### 3-1. 맞춤 진로 추천

서비스 첫 화면에서 자격 보유 상태에 맞는 경로를 선택합니다.

#### 자격이 없는 사용자

거주·활동 희망 지역, 주요 관심 종목, 추가 관심 종목, 운동 경험, 지도 대상, 활동 시간대를 입력합니다.

추천 결과는 다음 내용을 제공합니다.

- 취득을 고려할 종목 최대 5개
- 종목별 100점 기준 적합도와 세부 점수
- 관심 종목·지역·신청률·공급 부족도를 반영한 추천 이유
- 연결 가능한 자격 종류와 등급
- 자격 취득 후 살펴볼 기관
- 지역 데이터가 부족할 때 전국 데이터로 보완했다는 안내
- 신청 현황에 합성 데이터가 포함됐는지 여부

종목 상세 화면에서는 연결된 자격 정보와 실제 활동을 살펴볼 기관을 함께 확인할 수 있습니다.

#### 자격을 보유한 사용자

보유 자격 종류, 지도 종목, 활동 지역, 세부 지역, 이동 가능 범위, 희망 지도 대상, 요일, 시간대를 입력합니다.

추천 결과는 다음 기준으로 활동 기관 최대 5곳을 보여줍니다.

- 선택 종목과 기관 프로그램의 일치 정도
- 시·도 또는 시·군·구 일치 여부
- 희망 지도 대상과 프로그램 대상의 일치 여부
- 최근 프로그램 평균 신청률
- 대기자 발생 여부
- 활동 가능한 요일과 운영 요일
- 선호 시간대와 프로그램 운영 시간

각 결과에서 총점뿐 아니라 **왜 추천됐는지**, **어떤 데이터가 부족한지**를 함께 표시합니다.

### 3-2. 자격증·시험 정보

9개 체육지도자 자격등급을 선택해 다음 정보를 확인합니다.

- 자격 정의와 관련 근거
- 응시자격 과정과 제출서류
- 필기시험 과목
- 실기·구술 종목
- 검정기관과 연수기관
- 합격 기준과 결격사유
- 필기, 실기·구술, 연수, 최종 발표 일정
- 시험 일정의 마지막 갱신 상태

### 3-3. AI 추천 교재

시험정보 화면에서 선택한 자격과 필기 과목을 기준으로 Gemini가 교재를 추천합니다.

- 가장 적합한 교재 1권과 대안 교재 목록
- 추천 이유와 저자 정보
- 온라인 서점 검색 링크
- 새 추천 요청을 위한 캐시 갱신
- IP 기준 분당 요청 제한
- API 오류 시 시험정보 화면과 분리된 오류 처리

<code>GEMINI_API_KEY</code>가 설정된 환경에서 사용할 수 있습니다.

### 3-4. 통합 데이터 대시보드

지역, 종목, 기관, 지도 대상, 프로그램 상태, 검색어 조건을 조합하여 체육 데이터를 탐색합니다.

- 자격 취득, 프로그램, 기관, 신청 관련 핵심 지표
- 최신 기준월의 정원·신청·대기 현황
- 프로그램별 최근 6개월 평균 신청률
- 신청률에 따른 증설·유지·개선 검토 안내
- 실제 신청 데이터가 없을 때 시연용 데이터 사용 여부 표시

### 3-5. 지도자 자격 취득 현황

연도·지역·종목 조건으로 체육지도자 자격 취득 현황을 분석합니다.

- 전체 취득 건수
- 집계된 종목·지역·자격 종류 수
- 종목별 취득 건수 상위 20개
- 연도별 취득 추이
- 자격 종류·등급별 현황
- 지역별 현황
- 정렬과 페이지네이션을 적용한 원본 집계표

### 3-6. 프로그램·기관 탐색

정제된 공공체육 프로그램을 검색하고 현재 운영 여부와 분석 사용 가능 여부를 확인합니다.

- 운영 중·예정·종료 프로그램 구분
- 프로그램명, 종목, 기관, 지역, 대상 검색
- 종목 매칭 결과와 정제 근거 확인
- 제외된 프로그램의 제외 사유 확인
- 기관별 운영 프로그램 목록
- 기관의 정원·신청·신청률 집계
- 유지·개선·증설 검토 프로그램 분류
- 해당 지역에서 새로 살펴볼 종목 기회
- Kakao Maps 기반 기관 위치 확인

### 3-7. 프로그램 신청 현황

프로그램별 정원, 신청 인원, 대기 인원과 신청률을 확인합니다.

- 신청률 상위·하위 프로그램
- 정원 마감 프로그램
- 종목별 평균 신청률
- 기관별 평균 신청률
- 프로그램명·정원·신청 인원 기준 정렬
- 실제 데이터와 시뮬레이션 데이터를 명확히 구분

### 3-8. 지역별 수요·공급 분석

지역·종목별 운영 프로그램과 자격 취득 현황을 나란히 비교합니다.

- 지역별 운영 프로그램 수
- 종목별 자격 취득 건수
- 전체 정원·신청 인원과 평균 신청률
- 프로그램 수 대비 자격 취득 규모
- 데이터 근거를 함께 표시하는 규칙 기반 진단

분석 결과는 미래 수요 예측이 아니라 현재 적재된 데이터의 비교 지표입니다.

### 3-9. 고용24 스포츠 일자리

고용24의 스포츠·레크리에이션 직종 채용공고를 서비스에서 검색합니다.

- 채용 제목과 기관명 키워드 검색
- 지역 검색
- 20개 단위 페이지네이션
- 공고 제목, 회사, 지역, 고용형태, 마감일 확인
- 고용24 원문 공고 연결
- 외부 PostgreSQL 장애 시 빈 목록으로 안전하게 처리

### 3-10. 대타 강사 모집

체육기관의 갑작스러운 강사 공백과 프리랜서 지도자의 단기 활동 기회를 연결합니다.

#### 강사

- 종목·지역·근무일·급여 범위·키워드 검색
- 최신순, 근무일 임박순, 급여순 정렬
- 근무 날짜와 시간, 장소, 급여, 필요 자격 확인
- 이름·휴대폰 번호·비밀번호로 지원
- 같은 공고에 중복 지원 방지
- 마감 공고 지원 차단

#### 기관 담당자

- 휴대폰 번호와 비밀번호로 담당자 확인
- 기관명과 사업자등록번호 저장
- 종목, 날짜, 시간, 장소, 필요 자격, 급여, 인원을 포함한 공고 등록
- 등록 시 발급되는 관리 링크로 신청자 확인
- 공고 상태 변경·수정·삭제
- 신청자별 현장 평가 등록

#### 평판과 개인정보 보호

- 원문 전화번호는 저장하지 않고 해시와 마스킹 값만 보관
- 노쇼, 컴플레인, 성실함, 시간엄수, 전문성, 친절함 기록
- 최근 6개월, 6개월~1년, 1년 이상으로 평판 기간 구분
- 활동 기록 3건 미만은 신규 사용자로 표시
- 관리자만 허위·오류 기록을 사유와 함께 숨김 처리

> 현재 대타 지원의 자격증 보유 확인은 실제 회원·자격 DB 연동 전 단계의 모의 구현입니다.

### 3-11. 커뮤니티

회원가입 없이 닉네임과 비밀번호로 글과 댓글을 작성합니다.

- 자유게시판
- 시험정보 공유
- 기출문제·자료실
- 자격증 Q&A
- 게시글 목록·상세·조회수
- 댓글 작성과 삭제
- 작성 비밀번호를 이용한 글 수정·삭제
- 관리자 공지 상단 고정

비밀번호는 평문으로 저장하지 않고 Django 비밀번호 해시를 사용합니다.

### 3-12. 멘토링

커뮤니티 메뉴에 멘토링 진입 화면이 준비되어 있으며 현재는 출시 예정 기능으로 안내됩니다.

<a id="user-flow"></a>

## 4. 사용자별 이용 흐름

### 자격을 준비하는 사용자

~~~mermaid
flowchart LR
    A[관심 종목·지역 선택] --> B[자격 방향 추천]
    B --> C[종목 상세·연결 자격 확인]
    C --> D[응시요건·시험 일정 확인]
    D --> E[AI 교재 추천]
    E --> F[커뮤니티 자료·Q&A]
    F --> G[자격 취득 후 기관 탐색]
~~~

### 자격을 보유한 지도자

~~~mermaid
flowchart LR
    A[자격·종목·활동 조건 입력] --> B[기관 추천]
    B --> C[기관 프로그램·위치 확인]
    C --> D{활동 형태}
    D -->|상시| E[고용24 일자리]
    D -->|단기| F[대타 강사 공고]
    E --> G[현장 활동]
    F --> G
    G --> H[경력·평판 축적]
~~~

### 체육기관 담당자

~~~mermaid
flowchart LR
    A[대시보드·지역 분석] --> B[프로그램 운영 판단]
    B --> C[강사 공백 발생]
    C --> D[대타 공고 등록]
    D --> E[신청자 확인]
    E --> F[강사 선정·활동]
    F --> G[평판 기록]
~~~

<a id="recommendation"></a>

## 5. 맞춤 추천 기준

나침의 추천은 사용자가 결과를 이해할 수 있도록 규칙 기반 점수와 근거를 함께 제공합니다.

### 활동 기관 추천

| 평가 요소 | 최대 점수 | 기준 |
|---|---:|---|
| 종목 일치 | 40점 | 정확 일치 또는 정규화된 유사 종목 |
| 지역 일치 | 25점 | 시·군·구, 시·도, 지역 무관 범위 |
| 지도 대상 일치 | 10점 | 유아·아동, 청소년, 성인, 어르신, 장애인 |
| 최근 평균 신청률 | 15점 | 최근 프로그램 신청률 구간 |
| 대기자 발생 | 10점 | 최근 대기 인원 발생 여부 |

요일과 시간대는 추천 이유에 추가로 표시합니다. 데이터가 없는 항목은 점수를 추정하지 않고 부족한 데이터로 안내합니다.

### 자격 방향 추천

| 평가 요소 | 최대 점수 | 기준 |
|---|---:|---|
| 관심 종목 일치 | 35점 | 주요·추가 관심 종목 |
| 지역 일치 | 20점 | 희망 지역 내 운영 프로그램 |
| 지역 평균 신청률 | 20점 | 분석 대상 프로그램의 최근 신청률 |
| 프로그램 공급 부족도 | 15점 | 지역 또는 전국 중앙값과 공급 규모 비교 |
| 지도 대상 일치 | 10점 | 희망 대상 프로그램 존재 여부 |

지역 자료가 없으면 전국 데이터를 사용하고 그 사실을 결과에 표시합니다. 동점일 때는 관심 종목, 지역, 신청률, 종목명 순으로 정렬하여 같은 입력에 같은 결과를 제공합니다.

<a id="technology"></a>

## 6. 기술 스택과 아키텍처

### 기술 스택

| 영역 | 기술 | 역할 |
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

    subgraph Modules[서비스 모듈]
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
    Jobs --> PostgreSQL[(PostgreSQL)]
    Substitute --> PostgreSQL
    Community --> PostgreSQL
    Analytics --> Kakao[Kakao Maps]

    KSPO[KSPO] --> Pipeline[수집·정제 파이프라인]
    Work24[고용24] --> Pipeline
    PublicCSV[체육 공공데이터] --> Pipeline
    Pipeline --> SQLite
    Pipeline --> PostgreSQL
~~~

### 데이터베이스 분리

| 별칭 | 저장소 | 주요 데이터 |
|---|---|---|
| default | SQLite | 종목, 자격 취득, 기관, 프로그램, 신청 현황, 시험 일정 |
| community | PostgreSQL | 게시글, 댓글, 고용24 공고, 대타 공고·지원·평판 |

Django DB Router가 앱별 저장소를 나누며, 화면에서는 두 데이터베이스의 결과를 하나의 서비스처럼 제공합니다.

<a id="data"></a>

## 7. 데이터 구조

~~~mermaid
erDiagram
    CANONICAL_SPORT ||--o{ QUALIFICATION_AGGREGATE : has
    CANONICAL_SPORT ||--o{ PROGRAM : classifies
    INSTITUTION ||--o{ PROGRAM : operates
    PROGRAM ||--|| PROGRAM_CLEANUP : cleaned_as
    PROGRAM ||--o{ APPLICATION_STATUS : measured_by

    CANONICAL_SPORT ||--o{ SUBSTITUTE_POSTING : recruits
    CENTER_CONTACT ||--o{ SUBSTITUTE_POSTING : creates
    SUBSTITUTE_POSTING ||--o{ SUBSTITUTE_APPLICATION : receives
    PHONE_IDENTITY ||--o{ SUBSTITUTE_APPLICATION : applies
    PHONE_IDENTITY ||--o{ REPUTATION_RECORD : accumulates

    COMMUNITY_POST ||--o{ COMMENT : contains
    WORK24_FETCH_STATUS ||..o{ EXTERNAL_JOB_POSTING : tracks
    EXAM_FETCH_STATUS ||..o{ EXAM_SCHEDULE : tracks

    CANONICAL_SPORT {
        bigint id PK
        string name
        string normalized_name UK
        bigint qualification_count
    }
    INSTITUTION {
        bigint id PK
        string name
        string region
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
    COMMUNITY_POST {
        bigint id PK
        string category
        string title
        string nickname
        string password_hash
    }
~~~

### 현재 데이터 규모

2026-09-29 로컬 스냅샷 기준입니다.

| 데이터 | 건수 |
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

<a id="run"></a>

## 8. 실행 방법

### 환경 준비

명령은 <code>manage.py</code>가 있는 <code>main</code> 디렉터리에서 실행합니다.

#### Windows

~~~powershell
cd main
py -3.13 -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
~~~

#### macOS·Linux

~~~bash
cd main
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
~~~

### 환경 변수

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

### 데이터베이스와 서버 실행

~~~powershell
python manage.py migrate
python manage.py migrate --database=community
python manage.py runserver
~~~

브라우저에서 <http://127.0.0.1:8000/>에 접속합니다.

### 주요 화면

| 기능 | 경로 |
|---|---|
| 서비스 홈·맞춤 추천 | /recommendations/ |
| 자격 보유자 기관 추천 | /recommendations/licensed/ |
| 미보유자 자격 방향 추천 | /recommendations/unlicensed/ |
| 통합 대시보드 | /dashboard/ |
| 지도자 자격 취득 현황 | /instructors/ |
| 자격·시험 정보 | /exam-info/ |
| 운영 프로그램 | /current-programs/ |
| 신청 현황 | /applications/ |
| 수요·공급 분석 | /demand-supply/ |
| 커뮤니티 | /community/ |
| 고용24 일자리 | /community/jobs/ |
| 대타 강사 모집 | /community/substitutes/ |
| 관리자 | /admin/ |

<a id="pipeline"></a>

## 9. 데이터 수집과 운영

서비스 기능에 필요한 최신 데이터를 다음 파이프라인으로 관리합니다.

~~~mermaid
flowchart LR
    A[KSPO·고용24·공공 CSV] --> B[수집]
    B --> C[형식·결측·중복 검증]
    C --> D[지역·종목·기관명 정규화]
    D --> E[종목 매칭]
    E --> F[SQLite·PostgreSQL 적재]
    F --> G[추천·분석·일자리 화면]
~~~

### 수동 갱신

~~~bash
# KSPO 자격제도 안내
python manage.py crawl_license_info

# KSPO 전체 시험 일정
python manage.py refresh_exam_schedule

# 특정 자격등급 시험 일정
python manage.py refresh_exam_schedule --grade LSC2

# 고용24 스포츠 채용공고
python manage.py sync_work24_jobs
~~~

### 정기 갱신

<code>ENABLE_APSCHEDULER=true</code>인 운영 환경에서 다음 작업을 실행합니다.

| 데이터 | 실행 시간 |
|---|---|
| 고용24 채용공고 | 매일 03:00 KST |
| KSPO 시험 일정 | 매일 00:00·12:00 KST |

수집 결과가 비었거나 비정상적으로 줄면 기존 데이터를 유지합니다. 마지막 성공 시각과 건수, 오류는 관리자 화면의 수집 상태에서 확인할 수 있습니다.

<a id="quality"></a>

## 10. 테스트와 현재 제약사항

### 테스트

~~~powershell
python manage.py check
python manage.py test
~~~

핵심 데이터 처리 테스트만 실행하려면 다음 명령을 사용합니다.

~~~powershell
python manage.py test analytics.tests.test_kspo_crawler analytics.tests.test_clean_database_builder analytics.tests.test_sport_matching
~~~

자동 테스트가 확인하는 주요 범위:

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

### 데이터 해석 시 유의사항

- 자격 취득 건수는 현재 활동 중인 지도자 수와 같지 않습니다.
- 프로그램 수와 자격 취득 건수만으로 실제 인력 부족을 확정할 수 없습니다.
- 신청 현황의 시연용 합성 데이터는 화면에서 별도로 표시합니다.
- 추천 결과는 현재 적재 데이터에 따른 탐색 보조 정보이며 취업이나 자격 취득을 보장하지 않습니다.
- 고용24 공고의 실제 마감 여부와 세부 조건은 원문에서 다시 확인해야 합니다.

### 현재 제약사항과 개선 방향

| 현재 상태 | 영향 | 개선 방향 |
|---|---|---|
| 대타 지원 자격 확인이 모의 구현 | 실제 자격 소유 여부를 검증하지 못함 | 회원·자격증 DB 또는 공인 조회 API 연동 |
| 멘토링은 출시 예정 화면 | 멘토 검색·신청 기능 없음 | 지도자 경력 기반 멘토 매칭 구현 |
| 일부 신청 현황은 합성 데이터 | 실제 수요로 해석할 수 없음 | 기관별 실제 신청 데이터 연계 |
| 외부 사이트 HTML 구조 의존 | 구조 변경 시 수집 실패 가능 | 구조 변경 감지와 운영 알림 강화 |
| 규칙 기반 추천 | 사용자의 장기 성과를 학습하지 않음 | 실제 선택·활동 결과를 반영한 추천 개선 |
| 전화번호 기반 간편 신원 | 계정 복구와 다중 기기 관리 제한 | 회원 계정과 본인인증 도입 |

<a id="appendix"></a>

## 프로젝트 구조와 출처

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

### 데이터·외부 서비스 출처

- [국민체육진흥공단 체육지도자 자격검정](https://sqms.kspo.or.kr/)
- [고용24](https://www.work24.go.kr/)
- [Kakao Maps API](https://apis.map.kakao.com/)
- [Google Gemini API](https://ai.google.dev/)
- [GitHub 저장소](https://github.com/Leesannn/Noanswer3Brothers)

수집 데이터의 저작권과 이용 조건은 각 제공기관 정책을 따릅니다. 나침은 검색·분석에 필요한 구조화 항목과 원문 링크를 제공합니다.
