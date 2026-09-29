"""고용24(워크넷) '일자리 찾기 > 직종별 > 스포츠·레크리에이션' 결과 수집.

흐름: 직종별 목록 화면에서 '스포츠·레크리에이션'을 누르면 실행되는
fn_goSearch(index)를 그대로 재현한다 — GET으로 첫 페이지(occupation=059)를
받아 세션 쿠키를 얻고, 이후 페이지는 같은 세션으로 POST 페이지네이션을
반복한다. 페이지당 10건이며 새 항목이 더 안 나오면 종료한다.
"""
from .work24_client import Work24FetchError, fetch_first_page, fetch_page, new_session
from .work24_parser import parse_listing_page


SPORTS_RECREATION_OCCUPATION_CODE = '059'  # 예술·디자인·방송·스포츠 > 스포츠·레크리에이션
PAGE_SIZE = 10
MAX_PAGES = 150  # 안전장치: 현재 전체 934건 기준 약 94페이지, 여유를 둔 상한


def fetch_sports_job_postings(occupation_code=SPORTS_RECREATION_OCCUPATION_CODE):
    """스포츠·레크리에이션 카테고리 공고를 전부 수집해 dict 리스트로 반환한다.

    네트워크 오류는 Work24FetchError로 전파한다 (호출부가 잡아서 기존 데이터 보존).
    사이트 구조가 바뀌어 파싱이 깨지면 예외 없이 빈 리스트가 반환될 수 있는데,
    그 판단(=재수집 실패로 볼지)은 호출부(management command)의 몫으로 남긴다.
    """
    session = new_session()

    html = fetch_first_page(session, occupation_code)
    page_postings = parse_listing_page(html)

    all_postings = list(page_postings)
    seen_ids = {p['external_id'] for p in page_postings}

    page = 2
    while len(page_postings) >= PAGE_SIZE and page <= MAX_PAGES:
        html = fetch_page(session, occupation_code, page)
        page_postings = parse_listing_page(html)

        new_postings = [p for p in page_postings if p['external_id'] not in seen_ids]
        if not new_postings:
            break

        all_postings.extend(new_postings)
        seen_ids.update(p['external_id'] for p in new_postings)
        page += 1

    return all_postings


__all__ = ['Work24FetchError', 'fetch_sports_job_postings']
