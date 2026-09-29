"""work24.go.kr(고용24/워크넷) 요청 공통 처리.

공공기관 사이트이므로 매 요청 사이 딜레이를 두고, User-Agent를 명시하며,
실패 시 예외로 알려 호출부(관리 명령어)가 기존 캐시를 보존하도록 한다.
페이지네이션은 최초 목록 조회로 얻은 세션 쿠키가 있어야 동작하므로
requests.Session을 재사용한다.
"""
import time

import requests

USER_AGENT = 'Mozilla/5.0 (compatible; SportsCareerCompassBot/1.0)'
REQUEST_TIMEOUT = 15
REQUEST_DELAY_SECONDS = 1.5

BASE_URL = 'https://www.work24.go.kr'
LIST_URL = f'{BASE_URL}/wk/a/b/1200/retriveDtlEmpSrchList.do'
LIST_PAGE_URL = f'{BASE_URL}/wk/a/b/1200/retriveDtlEmpSrchListInPost.do'


class Work24FetchError(Exception):
    """work24.go.kr에서 데이터를 가져오거나 파싱하지 못했을 때."""


def new_session():
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    return session


def fetch_first_page(session, occupation_code, *, delay=REQUEST_DELAY_SECONDS):
    """직종별 목록에서 '검색' 클릭 시 이동하는 첫 페이지(GET)를 가져온다. 세션 쿠키가 여기서 생성된다."""
    if delay:
        time.sleep(delay)
    try:
        response = session.get(
            LIST_URL,
            params={'webIsOut': 'job', 'isEmptyHeader': '', 'isChkLocCall': '', 'occupation': occupation_code},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise Work24FetchError(f'{LIST_URL} 첫 페이지 요청 실패: {exc}') from exc
    response.encoding = response.apparent_encoding or 'utf-8'
    return response.text


def fetch_page(session, occupation_code, page_index, *, delay=REQUEST_DELAY_SECONDS):
    """두 번째 페이지부터는 mForm이 쓰는 POST 엔드포인트를 재현한다. 최초 GET으로 얻은 세션 쿠키가 필요하다."""
    if delay:
        time.sleep(delay)
    try:
        response = session.post(
            LIST_PAGE_URL,
            data={
                'occupation': occupation_code,
                'pageIndex': page_index,
                'currentPageNo': page_index,
            },
            headers={'Referer': LIST_URL},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise Work24FetchError(f'{LIST_PAGE_URL} {page_index}페이지 요청 실패: {exc}') from exc
    response.encoding = response.apparent_encoding or 'utf-8'
    return response.text
