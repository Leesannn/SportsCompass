# 데이터 모델 전체 명세

현재 Django 소스 모델 기준. 실제 데이터베이스에 연결하지 않고 추출했습니다.

PNG/SVG는 주요 필드 요약이며 아래에는 전체 필드와 복합 고유 제약을 기록합니다. User는 참조 편의를 위해 포함하며 내부 인증 관계는 생략합니다.

## UploadBatch — app_uploadbatch

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| dataset_type | CharField(20) |  | NO |  |
| original_filename | CharField(255) |  | NO |  |
| temporary_file | FileField(100) |  | NO |  |
| sheet_name | CharField(200) |  | NO |  |
| encoding | CharField(30) |  | NO |  |
| status | CharField(20) |  | NO |  |
| row_count | PositiveBigIntegerField |  | NO |  |
| success_count | PositiveBigIntegerField |  | NO |  |
| failure_count | PositiveBigIntegerField |  | NO |  |
| duplicate_count | PositiveBigIntegerField |  | NO |  |
| columns | JSONField |  | NO |  |
| missing_counts | JSONField |  | NO |  |
| preview_rows | JSONField |  | NO |  |
| field_mapping | JSONField |  | NO |  |
| errors | JSONField |  | NO |  |
| created_at | DateTimeField |  | NO |  |
| completed_at | DateTimeField |  | YES |  |

## Institution — app_institution

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| name | CharField(300) |  | NO |  |
| normalized_name | CharField(300) |  | NO |  |
| region | CharField(100) |  | NO |  |
| normalized_region | CharField(100) |  | NO |  |
| address | CharField(500) |  | NO |  |
| normalized_address | CharField(500) |  | NO |  |
| institution_type | CharField(100) |  | NO |  |

- unique_institution_region_address: UNIQUE (normalized_name, normalized_region, normalized_address)

## CanonicalSport — app_canonicalsport

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| name | CharField(150) |  | NO |  |
| normalized_name | CharField(150) | UK | NO |  |
| qualification_count | PositiveBigIntegerField |  | NO |  |
| is_active | BooleanField |  | NO |  |

## DataSource — app_datasource

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| filename | CharField(255) | UK | NO |  |

## ProgramMatchPayload — app_programmatchpayload

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| payload_key | CharField(32) | UK | NO |  |
| rules | JSONField |  | NO |  |
| candidates | JSONField |  | NO |  |

## Program — app_program

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| institution_id | ForeignKey | FK | NO | Institution / CASCADE |
| source_key | CharField(32) | UK | NO |  |
| name | CharField(400) |  | NO |  |
| normalized_name | CharField(400) |  | NO |  |
| sport | CharField(150) |  | NO |  |
| normalized_sport | CharField(150) |  | NO |  |
| target | CharField(300) |  | NO |  |
| weekdays | CharField(100) |  | NO |  |
| start_time | TimeField |  | YES |  |
| end_time | TimeField |  | YES |  |
| start_date | DateField |  | YES |  |
| end_date | DateField |  | YES |  |
| capacity | PositiveIntegerField |  | YES |  |
| status | CharField(50) |  | NO |  |
| source_id | ForeignKey | FK | YES | DataSource / PROTECT |
| program_type | CharField(200) |  | NO |  |
| facility_industry | CharField(200) |  | NO |  |
| matched_sport_id | ForeignKey | FK | YES | CanonicalSport / SET_NULL |
| match_grade | CharField(20) |  | NO |  |
| match_confidence | PositiveSmallIntegerField |  | NO |  |
| match_reason | TextField |  | NO |  |
| match_payload_id | ForeignKey | FK | YES | ProgramMatchPayload / PROTECT |
| match_is_manual | BooleanField |  | NO |  |

## ProgramCleanupDetail — app_programcleanupdetail

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| detail_key | CharField(32) | UK | NO |  |
| evidence | TextField |  | NO |  |
| rules | JSONField |  | NO |  |

## ProgramCleanup — app_programcleanup

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| program_id | OneToOneField | FK | NO | Program / CASCADE |
| cleaned_name | CharField(400) |  | NO |  |
| matched_sport_id | ForeignKey | FK | YES | CanonicalSport / SET_NULL |
| operating_status | CharField(20) |  | NO |  |
| is_usable | BooleanField |  | NO |  |
| exclusion_reason | CharField(30) |  | NO |  |
| detail_id | ForeignKey | FK | YES | ProgramCleanupDetail / PROTECT |
| reference_date | DateField |  | NO |  |

## QualificationAggregate — app_qualificationaggregate

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| acquisition_year | PositiveSmallIntegerField |  | YES |  |
| region | CharField(100) |  | NO |  |
| normalized_region | CharField(100) |  | NO |  |
| sport | CharField(150) |  | NO |  |
| normalized_sport | CharField(150) |  | NO |  |
| qualification_type | CharField(200) |  | NO |  |
| grade | CharField(100) |  | NO |  |
| acquisition_count | PositiveIntegerField |  | NO |  |
| source_filename | CharField(255) |  | NO |  |

- unique_qualification_aggregate: UNIQUE (acquisition_year, normalized_region, normalized_sport, qualification_type, grade, source_filename)

## ApplicationStatus — app_applicationstatus

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| program_id | ForeignKey | FK | NO | Program / CASCADE |
| source_key | CharField(32) | UK | NO |  |
| reference_date | DateField |  | YES |  |
| capacity | PositiveIntegerField |  | YES |  |
| applicants | PositiveIntegerField |  | YES |  |
| waitlist | PositiveIntegerField |  | YES |  |
| is_synthetic | BooleanField |  | NO |  |

- unique_program_application_period: UNIQUE (program, reference_date)

## ExamSchedule — app_examschedule

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| grade_code | CharField(10) |  | NO |  |
| grade_name | CharField(100) |  | NO |  |
| phase | CharField(30) |  | NO |  |
| season | CharField(30) |  | NO |  |
| course_type | CharField(30) |  | NO |  |
| milestone | CharField(50) |  | NO |  |
| start_at | DateTimeField |  | YES |  |
| end_at | DateTimeField |  | YES |  |
| raw_text | CharField(200) |  | NO |  |
| fetched_at | DateTimeField |  | NO |  |

## ExamScheduleFetchStatus — app_examschedulefetchstatus

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| grade_code | CharField(10) | UK | NO |  |
| last_success_at | DateTimeField |  | YES |  |
| last_checked_at | DateTimeField |  | YES |  |
| last_error | TextField |  | NO |  |

## PhoneIdentity — substitutes_phoneidentity

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| phone_hash | CharField(64) | UK | NO |  |
| phone_masked | CharField(20) |  | NO |  |
| password_hash | CharField(128) |  | NO |  |
| first_seen_at | DateTimeField |  | NO |  |

## CenterContact — substitutes_centercontact

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| phone_hash | CharField(64) | UK | NO |  |
| phone_masked | CharField(20) |  | NO |  |
| password_hash | CharField(128) |  | NO |  |
| institution_id | ForeignKey | FK | YES | Institution / SET_NULL |
| institution_name | CharField(200) |  | NO |  |
| business_reg_no | CharField(20) |  | NO |  |
| verified_at | DateTimeField |  | NO |  |

## Posting — substitutes_posting

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| manager_id | ForeignKey | FK | NO | CenterContact / PROTECT |
| sport_id | ForeignKey | FK | NO | CanonicalSport / PROTECT |
| work_date | DateField |  | NO |  |
| start_time | TimeField |  | NO |  |
| end_time | TimeField |  | NO |  |
| region | CharField(100) |  | NO |  |
| normalized_region | CharField(100) |  | NO |  |
| address | CharField(300) |  | NO |  |
| required_certifications | JSONField |  | NO |  |
| pay_amount | PositiveIntegerField |  | NO |  |
| pay_unit | CharField(10) |  | NO |  |
| headcount | PositiveSmallIntegerField |  | NO |  |
| description | TextField |  | NO |  |
| status | CharField(20) |  | NO |  |
| created_at | DateTimeField |  | NO |  |

## Application — substitutes_application

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| posting_id | ForeignKey | FK | NO | Posting / CASCADE |
| phone_identity_id | ForeignKey | FK | NO | PhoneIdentity / PROTECT |
| phone_masked | CharField(20) |  | NO |  |
| certification_verified | BooleanField |  | NO |  |
| applied_at | DateTimeField |  | NO |  |

- unique_posting_application: UNIQUE (posting, phone_identity)

## ReputationRecord — substitutes_reputationrecord

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| phone_identity_id | ForeignKey | FK | NO | PhoneIdentity / CASCADE |
| posting_id | ForeignKey | FK | YES | Posting / SET_NULL |
| is_no_show | BooleanField |  | NO |  |
| is_complaint | BooleanField |  | NO |  |
| positive_tags | JSONField |  | NO |  |
| comment | TextField |  | NO |  |
| occurred_at | DateTimeField |  | NO |  |
| created_by_id | ForeignKey | FK | YES | CenterContact / SET_NULL |
| is_hidden | BooleanField |  | NO |  |
| hidden_reason | TextField |  | NO |  |
| hidden_at | DateTimeField |  | YES |  |
| hidden_by_id | ForeignKey | FK | YES | User / SET_NULL |

## Post — community_post

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| category | CharField(20) |  | NO |  |
| title | CharField(200) |  | NO |  |
| nickname | CharField(30) |  | NO |  |
| password_hash | CharField(128) |  | NO |  |
| content | TextField |  | NO |  |
| view_count | PositiveIntegerField |  | NO |  |
| is_notice | BooleanField |  | NO |  |
| created_at | DateTimeField |  | NO |  |
| updated_at | DateTimeField |  | NO |  |

## Comment — community_comment

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | BigAutoField | PK | NO |  |
| post_id | ForeignKey | FK | NO | Post / CASCADE |
| nickname | CharField(30) |  | NO |  |
| password_hash | CharField(128) |  | NO |  |
| content | TextField |  | NO |  |
| created_at | DateTimeField |  | NO |  |

## User — auth_user

| 컬럼 | Django 타입 | 키 | NULL | 참조 / 삭제 정책 |
|---|---|---|---|---|
| id | AutoField | PK | NO |  |
| password | CharField(128) |  | NO |  |
| last_login | DateTimeField |  | YES |  |
| is_superuser | BooleanField |  | NO |  |
| username | CharField(150) | UK | NO |  |
| first_name | CharField(150) |  | NO |  |
| last_name | CharField(150) |  | NO |  |
| email | CharField(254) |  | NO |  |
| is_staff | BooleanField |  | NO |  |
| is_active | BooleanField |  | NO |  |
| date_joined | DateTimeField |  | NO |  |
