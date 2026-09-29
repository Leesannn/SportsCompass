# 나침 - 스포츠 커리어 나침반

> 체육 공공데이터를 자동으로 수집·전처리·적재하고, 예비·현직 체육지도자의 진로 탐색과 활동 기회 연결을 돕는 데이터 서비스

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-community_DB-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLite](https://img.shields.io/badge/SQLite-analysis_DB-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

- 저장소: [github.com/Leesannn/Noanswer3Brothers](https://github.com/Leesannn/Noanswer3Brothers)
- 권장 환경: Python 3.13
- 기준 시간대: Asia/Seoul
- 데이터 스냅샷 기준일: 2026-07-31

## 평가 대상 범위

이번 단위 프로젝트의 평가 대상은 기존 웹 서비스 화면이 아니라 다음 **데이터 파이프라인 구현**입니다.

1. 국민체육진흥공단 체육지도자 자격·시험 일정 수집
2. 고용24 스포츠·레크리에이션 채용공고 수집
3. 공공데이터 CSV의 검증·정규화·중복 제거·종목 매칭
4. SQLite·PostgreSQL 적재 및 적재 건수 검증
5. APScheduler 기반 정기 실행, 누락 보충, 중복 실행 방지
6. 오류·빈 결과·사이트 구조 변경 시 기존 데이터 보존

맞춤 추천, 대시보드, 대타 모집, 커뮤니티 등 웹 서비스 기능은 파이프라인 결과를 확인하는 시연 화면으로 활용합니다.

## 평가용 핵심 요약

| 확인 항목 | 내용 | 근거 위치 |
|---|---|---|
| 수집 | KSPO 자격제도·시험 일정, 고용24 직종 코드 059 공고 | analytics/services/kspo_*.py, jobs/services/work24_*.py |
| 전처리 | 인코딩 감지, NFKC·공백·지역명 정규화, 필수 컬럼·날짜·정원 검증, 결정론적 종목 매칭 | analytics/services/clean_database_builder.py |
| 적재 | 분석 데이터는 SQLite, 고용24 공고·수집 상태는 PostgreSQL | main/settings.py, main/db_routers.py |
| 스케줄 | 고용24 매일 03:00, 시험 일정 매일 00:00·12:00 | jobs/scheduler.py |
| 로그 | 로컬 콘솔 또는 Render Logs, 마지막 성공·실패는 상태 테이블에 저장 | Work24FetchStatus, ExamScheduleFetchStatus |
| 장애 대응 | 요청 실패·0건·급격한 건수 감소 시 기존 데이터 유지 | sync_work24_jobs, refresh_exam_schedule |
| 중복 방지 | 고유 제약, 원본 키, PostgreSQL advisory lock, max_instances=1 | 모델·스케줄러 코드 |
| 검증 결과 | 파이프라인 핵심 테스트 30건 통과 | 아래 검증 절 참고 |

### 현재 적재 결과

2026-09-29 로컬 스냅샷과 생성 산출물을 직접 집계한 값입니다.

| 데이터 | 적재·생성 건수 | 비고 |
|---|---:|---|
| 기준 스포츠 종목 | 113개 | CanonicalSport |
| 자격 취득 집계 | 17,467건 | QualificationAggregate |
| 기관 | 376개 | Institution |
| 프로그램 | 204,461건 | Program |
| 프로그램 정리 결과 | 204,461건 | 원본 프로그램과 1:1 |
| 운영 중·분석 가능 프로그램 | 9,377건 | 기준일 2026-07-31 |
| 운영 종료 프로그램 | 176,619건 | 분석 대상 제외 |
| 운영 예정 프로그램 | 18,465건 | 분석 대상 제외 |
| 자격등급 요약 | 9건 | data/kspo_license_grades.csv |
| 응시자격 경로 | 48건 | data/kspo_license_eligibility_paths.csv |
| 시험 일정 | 388건 | 9개 자격등급, ExamSchedule |
| 고용24 채용공고 | 934건 | 개발 확인 기준, 운영 DB의 last_success_count로 최종 확인 |

고용24 운영 DB는 외부 PostgreSQL이므로 제출 시점의 최종 건수는 관리자 화면의 **외부 채용정보 갱신 상태** 또는 Work24FetchStatus.last_success_count를 기준으로 확인합니다.

## 목차

1. [팀 소개](#1-팀-소개)
2. [프로젝트 개요](#2-프로젝트-개요)
3. [기술 스택](#3-기술-스택)
4. [WBS](#4-wbs)
5. [요구사항 명세서](#5-요구사항-명세서)
6. [ERD](#6-erd)
7. [주요 프로시저](#7-주요-프로시저)
8. [수행 결과](#8-수행-결과)
9. [한 줄 회고](#9-한-줄-회고)

## 1. 팀 소개

### 오답삼형제

| 팀원 | GitHub | 커밋 기준 주요 기여 |
|---|---|---|
| Leesannn | [@Leesannn](https://github.com/Leesannn) | 서비스 통합, PostgreSQL·배포 구성, 고용24 수집·APScheduler |
| HYM010219 | [@HYM010219](https://github.com/HYM010219) | KSPO 자격정보, 고용24 검색·수집, UI·시연 데이터 |
| ericsw2727 | [@ericsw2727](https://github.com/ericsw2727) | 공공데이터 정제·구조 개편, 분석 화면, 문서·UI 개선 |

역할 표는 저장소 커밋 이력을 기준으로 요약했습니다.

## 2. 프로젝트 개요

### 프로젝트명

**나침 - 스포츠 커리어 나침반**

- 프로젝트 주제: **자동 학습 데이터 파이프라인 구축**
- 세부 주제: **체육 공공데이터 기반 자동 수집·전처리·적재 파이프라인**

### 프로젝트 소개

스포츠 프로그램, 체육지도자 자격 취득 현황, 시험 일정, 채용공고처럼 서로 흩어진 데이터를 하나의 파이프라인으로 수집·정리합니다. 정리된 데이터는 지도자의 자격 취득 방향과 활동 기관 탐색, 지역별 프로그램·지도자 현황 비교에 사용합니다.

### 필요성

- 체육 프로그램·자격·채용 정보가 여러 기관과 사이트에 분산되어 있습니다.
- 사이트별 형식과 지역·종목 표현이 달라 그대로 비교하기 어렵습니다.
- 외부 사이트 장애나 구조 변경이 서비스 데이터 전체를 비우지 않도록 안전한 갱신 방식이 필요합니다.
- 수동 갱신은 누락 가능성이 있어 정기 실행과 실행 상태 기록이 필요합니다.

### 목표

1. 공개된 체육 데이터를 반복 가능한 방식으로 자동 수집합니다.
2. 결측·중복·형식 오류를 검증하고 종목·지역 표현을 표준화합니다.
3. 검증을 통과한 데이터만 저장소에 적재합니다.
4. 수집 실패 시 기존 데이터를 보존하고 실패 원인을 기록합니다.
5. 정해진 시간에 실행하고, 서버 휴면으로 놓친 작업은 자동 보충합니다.
6. 웹 서비스와 분리된 관리 명령으로 독립 실행·검증할 수 있게 합니다.

### 데이터 출처

| 출처 | 수집 대상 | 수집 방식 | 저장 위치 |
|---|---|---|---|
| 국민체육진흥공단 체육지도자 자격검정 | 9개 등급 자격 정의·응시요건·시험 과목·기관 | requests + BeautifulSoup | CSV·TXT |
| 국민체육진흥공단 체육지도자 자격검정 | 9개 등급 연간 시험 일정 | requests + BeautifulSoup | SQLite ExamSchedule |
| 고용24 | 스포츠·레크리에이션 직종 공고 | 세션 기반 GET·POST 페이지네이션 + BeautifulSoup | PostgreSQL ExternalJobPosting |
| 체육 공공데이터 CSV | 자격 취득 집계·시설 프로그램 | 스트리밍 CSV 전처리 | 정제 SQLite·서비스 SQLite |

수집기는 브라우저 자동화에 의존하지 않습니다. 서버가 반환한 HTML을 파싱하므로 배포 환경에서도 동일하게 실행할 수 있습니다.

## 3. 기술 스택

| 구분 | 기술 | 사용 목적 |
|---|---|---|
| 언어 | Python 3.13 | 수집·전처리·적재·웹 서비스 |
| 웹 프레임워크 | Django 6.1.1 | ORM, 관리 명령, 관리자, 서비스 화면 |
| 수집 | requests 2.32.3 | 세션·타임아웃을 적용한 HTTP 요청 |
| 파싱 | BeautifulSoup 4.12.3 | KSPO·고용24 HTML 파싱 |
| 데이터 처리 | Python csv, pandas 3.0.5, openpyxl 3.1.5 | CSV·XLSX 입력과 검증 |
| 스케줄링 | APScheduler 3.x | Cron·보충 작업 실행 |
| 데이터베이스 | SQLite, PostgreSQL | 분석 데이터와 외부 공고 분리 저장 |
| 운영 | Gunicorn, Render, WhiteNoise | 웹 서비스 실행·로그·정적 파일 제공 |
| UI | Django Templates, Bootstrap, Chart.js | 결과 조회·시연 |
| 테스트 | Django TestCase, unittest.mock | 파서·정제·저장·예외 흐름 검증 |

## 4. WBS

| 단계 | 작업 | 주요 산출물 | 상태 |
|---|---|---|---|
| 1. 요구 분석 | 출처·갱신 주기·저장 항목·실패 정책 정의 | 요구사항, 데이터 항목표 | 완료 |
| 2. 수집 설계 | KSPO 등급 URL, 고용24 직종 코드·페이지 흐름 분석 | 수집 모듈 설계 | 완료 |
| 3. 수집 구현 | 세션, 타임아웃, 요청 간격, 페이지네이션 구현 | kspo_*.py, work24_*.py | 완료 |
| 4. 전처리 구현 | 인코딩·필수 컬럼·날짜·정원 검증, 정규화 | clean_database_builder.py | 완료 |
| 5. 품질 관리 | 미매칭·오류 CSV, 중복·무결성 검사 | unmatched_programs.csv, invalid_rows.csv | 완료 |
| 6. 적재 구현 | 임시 DB 생성 후 교체, DB 라우팅, 트랜잭션 | SQLite·PostgreSQL 모델 | 완료 |
| 7. 자동화 | Cron 작업, 보충 실행, advisory lock | jobs/scheduler.py | 완료 |
| 8. 검증 | 파서·정제·장애 시나리오 테스트 | 테스트 코드·실행 로그 | 완료 |
| 9. 시연 | 관리자 상태, 시험 정보, 일자리 목록에서 결과 확인 | 서비스 화면 | 완료 |

## 5. 요구사항 명세서

### 기능 요구사항

| ID | 요구사항 | 구현 |
|---|---|---|
| DP-01 | KSPO의 9개 자격등급 정보를 수집해야 한다. | crawl_license_info |
| DP-02 | KSPO 연간 시험 일정을 등급별로 수집해야 한다. | refresh_exam_schedule |
| DP-03 | 고용24 스포츠·레크리에이션 공고 전체를 페이지 단위로 수집해야 한다. | sync_work24_jobs |
| DP-04 | HTTP 요청에 User-Agent, 지연, 타임아웃을 적용해야 한다. | kspo_client.py, work24_client.py |
| DP-05 | CSV 인코딩과 필수 컬럼을 검사해야 한다. | detect_encoding, open_csv |
| DP-06 | 공백·유니코드·기관명·지역명을 정규화해야 한다. | clean_database_builder.py |
| DP-07 | 프로그램을 자격 기준 종목에 결정론적으로 연결해야 한다. | sport_matching.py, 규칙 JSON |
| DP-08 | 미매칭·오류 행을 적재 대상에서 분리하고 사유를 남겨야 한다. | 검토 CSV·요약 로그 |
| DP-09 | 중복과 무결성을 검사한 데이터만 최종 DB로 교체해야 한다. | 임시 SQLite + PRAGMA integrity_check |
| DP-10 | 수집 결과가 비었거나 급감하면 기존 데이터를 보존해야 한다. | 빈 결과·직전 대비 30% 미만 방어 |
| DP-11 | 작업 성공·실패 시각, 건수, 오류를 조회할 수 있어야 한다. | 상태 모델·Django 관리자 |
| DP-12 | 정해진 시간에 자동 실행하고 누락 작업을 보충해야 한다. | APScheduler Cron·Interval 작업 |

### 비기능 요구사항

| ID | 요구사항 | 구현 |
|---|---|---|
| NFR-01 | 수집 모듈은 기존 웹 화면과 분리해 단독 실행할 수 있어야 한다. | Django management command |
| NFR-02 | 여러 Gunicorn worker가 같은 작업을 중복 실행하지 않아야 한다. | PostgreSQL advisory lock |
| NFR-03 | 한 번에 대량 데이터를 메모리에 모두 올리지 않아야 한다. | iterator, fetchmany, bulk_create |
| NFR-04 | 동일 원본을 재처리해도 중복 레코드가 생기지 않아야 한다. | source key·UniqueConstraint |
| NFR-05 | 외부 DB 장애가 전체 웹 요청을 장시간 차단하지 않아야 한다. | PostgreSQL 연결 제한·예외 처리 |
| NFR-06 | 스케줄과 저장 결과를 운영 로그와 DB 상태로 확인할 수 있어야 한다. | 콘솔 로그·상태 테이블 |

## 6. ERD

평가 대상 파이프라인의 핵심 엔터티만 표시했습니다. ExamSchedule·ExternalJobPosting의 관계는 외래키가 아닌 grade_code·source 기준의 논리적 연결입니다.

~~~mermaid
erDiagram
    CANONICAL_SPORT ||--o{ QUALIFICATION_AGGREGATE : aggregates
    CANONICAL_SPORT ||--o{ PROGRAM : classifies
    INSTITUTION ||--o{ PROGRAM : operates
    PROGRAM ||--|| PROGRAM_CLEANUP : cleaned_as
    PROGRAM ||--o{ APPLICATION_STATUS : measured_by
    DATA_SOURCE ||--o{ PROGRAM : imported_from

    EXAM_SCHEDULE_FETCH_STATUS ||..o{ EXAM_SCHEDULE : grade_code
    WORK24_FETCH_STATUS ||..o{ EXTERNAL_JOB_POSTING : source

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
        string normalized_region
        string normalized_address
    }
    PROGRAM {
        bigint id PK
        string source_key UK
        bigint institution_id FK
        bigint matched_sport_id FK
        string normalized_name
        date start_date
        date end_date
    }
    PROGRAM_CLEANUP {
        bigint id PK
        bigint program_id FK
        string operating_status
        boolean is_usable
        string exclusion_reason
        date reference_date
    }
    EXAM_SCHEDULE {
        bigint id PK
        string grade_code
        string phase
        string milestone
        datetime start_at
        datetime end_at
    }
    EXAM_SCHEDULE_FETCH_STATUS {
        bigint id PK
        string grade_code UK
        datetime last_checked_at
        datetime last_success_at
        text last_error
    }
    EXTERNAL_JOB_POSTING {
        bigint id PK
        string source
        string external_id
        string title
        string company_name
        string source_url
        datetime fetched_at
    }
    WORK24_FETCH_STATUS {
        bigint id PK
        string source UK
        datetime last_checked_at
        datetime last_success_at
        int last_success_count
        text last_error
    }
~~~

## 7. 주요 프로시저

### 전체 파이프라인

~~~mermaid
flowchart LR
    A[공공데이터·외부 사이트] --> B[수집]
    B --> C{응답·형식 검증}
    C -->|정상| D[정규화·중복 제거·종목 매칭]
    C -->|실패| H[오류 기록·기존 데이터 유지]
    D --> E{무결성 검사}
    E -->|통과| F[SQLite·PostgreSQL 적재]
    E -->|실패| H
    F --> G[상태·건수 기록]
    G --> I[서비스 조회·시연]
    J[APScheduler] --> B
~~~

### KSPO 자격제도 수집

1. 9개 등급 코드를 순회합니다.
2. 등급별 자격제도 안내 HTML을 요청합니다.
3. 자격 정의, 근거, 필기 과목, 종목, 검정·연수기관, 합격 기준을 파싱합니다.
4. 응시자격 경로와 제출서류를 행 단위로 변환합니다.
5. 등급 요약 CSV, 응시자격 CSV, 결격사유 TXT를 UTF-8로 저장합니다.
6. 모든 등급이 실패하면 기존 파일을 덮어쓰지 않습니다.

### KSPO 시험 일정 갱신

1. 등급별 연간일정 페이지를 요청합니다.
2. 필기, 실기·구술, 연수, 최종 발표 단계와 일시를 구조화합니다.
3. 해당 등급의 새 결과가 비어 있으면 실패로 기록하고 기존 캐시를 유지합니다.
4. 정상 결과만 트랜잭션 안에서 기존 등급 데이터와 교체합니다.
5. ExamScheduleFetchStatus에 확인 시각, 성공 시각, 오류를 기록합니다.

### 고용24 공고 갱신

1. 직종 코드 059의 첫 페이지를 GET으로 요청해 세션 쿠키를 얻습니다.
2. 같은 세션으로 다음 페이지를 POST 요청합니다.
3. wantedAuthNo를 외부 고유 ID로 사용하고 중복 공고를 제거합니다.
4. 새 ID가 없거나 마지막 페이지에 도달하면 수집을 종료합니다.
5. 결과가 0건이거나 직전 성공 건수의 30% 미만이면 구조 변경으로 판단해 기존 데이터를 유지합니다.
6. 정상 결과는 PostgreSQL 트랜잭션에서 일괄 교체합니다.
7. 성공 시각·건수 또는 오류를 Work24FetchStatus에 기록합니다.

### 공공데이터 정제 DB 생성

1. UTF-8-SIG, UTF-8, CP949, EUC-KR 순으로 인코딩을 판별합니다.
2. 필수 컬럼, 취득 연도, 운영 기간, 정원 값을 검증합니다.
3. 텍스트를 NFKC로 정규화하고 공백·기관명·지역명을 표준화합니다.
4. 자격 종목을 기준 taxonomy로 만들고 프로그램 종목을 규칙 기반으로 매칭합니다.
5. 미매칭 행과 오류 행을 별도 CSV로 기록합니다.
6. 임시 SQLite에 적재한 뒤 중복·빈 이름·날짜 역전·음수·FK 무결성을 검사합니다.
7. 모든 검사를 통과했을 때만 os.replace로 최종 DB를 교체합니다.

## 실행 방법

명령은 manage.py가 있는 main 디렉터리에서 실행합니다.

### 1. 로컬 환경 준비

#### Windows

~~~powershell
cd main
"C:/Users/<사용자명>/AppData/Local/Programs/Python/Python313/python.exe" -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py migrate --database=community
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
~~~

.env에서 COMMUNITY_DB_* 값을 실제 PostgreSQL 접속 정보로 변경해야 고용24 수집과 커뮤니티 기능을 사용할 수 있습니다. 비밀키와 비밀번호가 들어간 .env는 Git에 커밋하지 않습니다.

### 2. 파이프라인 수동 실행

~~~bash
# KSPO 자격제도 안내 -> CSV·TXT
python manage.py crawl_license_info

# KSPO 9개 등급 시험 일정 -> SQLite
python manage.py refresh_exam_schedule

# 특정 등급만 갱신
python manage.py refresh_exam_schedule --grade LSC2

# 고용24 스포츠·레크리에이션 공고 -> PostgreSQL
python manage.py sync_work24_jobs
~~~

### 3. 원본 CSV로 정제 DB 재구축

원본 파일은 개인정보·용량 정책에 따라 저장소에 포함하지 않을 수 있습니다. 실제 파일 경로를 인수로 전달합니다.

~~~bash
python manage.py build_clean_database +  data/KS_PTDRCTOR_PSEXAM_INFO_202607.csv +  data/KS_PUBLIC_ALSFC_PROGRM_INFO_202607.csv +  --output-dir exports/rebuilt_202607 +  --reference-date 2026-07-31 +  --replace
~~~

생성 결과:

~~~text
exports/rebuilt_202607/
├─ sports_clean_202607.sqlite3  # 검증 완료 정제 DB
├─ cleaning_summary.txt         # 입력·성공·제외·오류·무결성 건수
├─ unmatched_programs.csv       # 종목 미매칭 검토 목록
└─ invalid_rows.csv             # 형식 오류·필수값 누락 목록
~~~

빈 서비스 DB에 연결할 때만 다음 명령을 실행합니다.

~~~bash
python manage.py load_clean_service_database +  exports/rebuilt_202607/sports_clean_202607.sqlite3 +  --reference-date 2026-07-31
~~~

### 4. 웹 서비스 실행

~~~bash
python manage.py runserver
~~~

- 홈·맞춤 추천: <http://127.0.0.1:8000/recommendations/>
- 프로그램 현황: <http://127.0.0.1:8000/dashboard/>
- 시험 정보: <http://127.0.0.1:8000/exam-info/>
- 고용24 일자리: <http://127.0.0.1:8000/community/jobs/>
- 관리자: <http://127.0.0.1:8000/admin/>

## 스케줄 설정

운영 환경에서는 .env 또는 Render 환경 변수에 다음 값을 추가합니다.

~~~dotenv
ENABLE_APSCHEDULER=true
~~~

Gunicorn 시작 명령:

~~~bash
gunicorn -c gunicorn.conf.py main.wsgi:application
~~~

| 작업 ID | 실행 시간 | 보충 실행 | 중복 방지 |
|---|---|---|---|
| work24_daily_sync | 매일 03:00 KST | 기동 30초 후 확인, 이후 1시간마다 | advisory lock + max_instances=1 |
| exam_schedule_twice_daily_sync | 매일 00:00·12:00 KST | 기동 60초 후 확인, 이후 1시간마다 | advisory lock + max_instances=1 |

보충 작업은 해당 실행 구간에 이미 성공한 기록이 있으면 수집을 건너뜁니다. 실패 직후에는 한 시간 동안 재시도하지 않아 외부 사이트에 과도한 요청을 보내지 않습니다.

## 로그 위치와 상태 확인

별도 로컬 로그 파일은 생성하지 않습니다. 실행 환경에 따라 다음 위치에서 확인합니다.

| 구분 | 위치 | 확인 내용 |
|---|---|---|
| 로컬 수동 실행 | 명령을 실행한 터미널의 stdout·stderr | 등급별 성공, 적재 건수, 오류 |
| 로컬 서버 | runserver·Gunicorn 콘솔 | APScheduler 시작·실행·예외 |
| Render | 서비스 Dashboard의 Logs | 운영 스케줄 실행 로그 |
| 고용24 상태 | 관리자 외부 채용정보 갱신 상태 | 마지막 확인·성공 시각, 성공 건수, 오류 |
| 시험 일정 상태 | 관리자 연간일정계획 갱신 상태 | 등급별 마지막 확인·성공 시각, 오류 |
| CSV 정제 결과 | exports/rebuilt_202607/cleaning_summary.txt | 원본·성공·제외·오류·무결성 건수 |

상태를 콘솔에서 확인하는 예:

~~~bash
python manage.py shell -c "from jobs.models import Work24FetchStatus; print(list(Work24FetchStatus.objects.values()))"
python manage.py shell -c "from analytics.models import ExamScheduleFetchStatus; print(list(ExamScheduleFetchStatus.objects.values()))"
~~~

## 검증

### 시스템·전체 테스트

~~~bash
python manage.py check
python manage.py test
~~~

### 평가 대상 파이프라인 핵심 테스트

~~~bash
python manage.py test +  analytics.tests.test_kspo_crawler +  analytics.tests.test_clean_database_builder +  analytics.tests.test_sport_matching
~~~

2026-09-29 실행 결과:

~~~text
Ran 30 tests in 0.629s
OK
~~~

검증 범위에는 HTML 파싱, 타임아웃·HTTP 오류, 인코딩, 필수 컬럼, 중복 제거, 운영 상태, 종목 매칭, SQLite 무결성 검사가 포함됩니다. 외부 사이트를 직접 호출하는 테스트는 mock 응답을 사용해 재현 가능하게 구성했습니다.

## 8. 수행 결과

### 실행 결과 확인 경로

| 화면 | 경로 | 확인 내용 |
|---|---|---|
| 맞춤 추천 시작 | /recommendations/ | 정제 프로그램·종목·기관 집계 |
| 프로그램 현황 | /dashboard/ | 기관·프로그램·지역 통계 |
| 운영 프로그램 | /current-programs/ | 운영 상태, 제외 사유, 판정 근거 |
| 수요·공급 분석 | /demand-supply/ | 지역별 프로그램·자격 취득 비교 |
| 시험 정보 | /exam-info/ | KSPO 일정 캐시·자격 안내 |
| 일자리 공고 | /community/jobs/ | 고용24 수집 공고 검색·페이지네이션 |
| 관리자 | /admin/ | 수집 상태·오류·적재 데이터 확인 |

### 품질 검증 기준

- 필수 컬럼 누락 시 즉시 중단하고 누락 컬럼명을 출력합니다.
- 날짜 역전, 음수 정원·취득 건수, 빈 프로그램명은 오류로 분리합니다.
- 기관·프로그램·운영 기간의 중복을 고유 키로 차단합니다.
- 미매칭 프로그램을 임의 종목에 연결하지 않고 검토 CSV로 분리합니다.
- SQLite integrity_check, FK 검사, 중복 집계를 모두 통과해야 최종 DB를 생성합니다.
- 서비스 DB 적재 후 원본 정제 DB와 종목·기관·자격·프로그램 건수를 다시 비교합니다.
- 외부 수집 실패 시 기존 정상 데이터를 삭제하지 않습니다.

### 데이터 해석 시 유의사항

- 자격 취득 건수는 현재 활동 중인 지도자 수와 같지 않습니다.
- 프로그램 수와 자격 취득 건수만으로 실제 인력 부족을 확정할 수 없습니다.
- ApplicationStatus.is_synthetic=True인 신청 현황은 화면 시연용이며 실제 운영 실적이 아닙니다.
- 고용24 공고는 수집 시점의 공개 목록이며 실제 마감 여부는 원문에서 다시 확인해야 합니다.
- 추천 결과는 진로 탐색을 위한 참고 정보이며 채용이나 자격 취득을 보장하지 않습니다.

## 9. 한 줄 회고

| 팀원 | 회고 |
|---|---|
| Leesannn | 수집 성공보다 실패했을 때 기존 데이터를 지키고 다시 실행할 수 있는 구조가 운영에서 더 중요하다는 점을 배웠다. |
| HYM010219 | 사이트마다 다른 HTML 구조를 데이터 항목으로 바꾸는 과정에서 파싱 규칙과 검증 기준을 함께 설계해야 함을 배웠다. |
| ericsw2727 | 많은 공공데이터를 서비스에 연결하려면 화면보다 먼저 정규화 기준과 재현 가능한 정제 결과가 필요하다는 점을 배웠다. |

## 프로젝트 구조

~~~text
main/
├─ analytics/
│  ├─ management/commands/       # 자격 수집·시험 갱신·정제 DB 생성·적재
│  ├─ services/                  # KSPO 수집, 정규화, 종목 매칭, 정제
│  ├─ tests/                     # 파서·정제·분석 테스트
│  ├─ program_cleanup_rules.json # 운영 프로그램 정리 규칙
│  └─ sport_matching_rules.json  # 종목 동의어·상위 종목·문맥 규칙
├─ jobs/
│  ├─ management/commands/       # 고용24 수동 동기화
│  ├─ services/                  # HTTP 요청·페이지 수집·HTML 파싱
│  ├─ scheduler.py               # Cron·누락 보충·중복 실행 방지
│  └─ models.py                  # 공고·수집 상태
├─ data/                         # 생성된 자격정보 CSV·TXT와 시연 데이터
├─ main/
│  ├─ settings.py                # DB·시간대·환경 설정
│  └─ db_routers.py              # SQLite·PostgreSQL 라우팅
├─ gunicorn.conf.py              # worker 시작·종료 시 스케줄러 제어
├─ requirements.txt
└─ manage.py
~~~

## 라이선스·출처

수집 데이터의 저작권과 이용 조건은 각 원 제공기관 정책을 따릅니다. 서비스는 원문 전체를 재배포하기보다 검색·분석에 필요한 구조화 항목과 원문 링크를 제공합니다.

- 국민체육진흥공단 체육지도자 자격검정: <https://sqms.kspo.or.kr/>
- 고용24: <https://www.work24.go.kr/>
