"""work24.go.kr 직종별 검색 결과 HTML 파싱.

목록 페이지는 서버사이드에서 정적으로 렌더링되므로 BeautifulSoup만으로
충분하다 (JS 실행/헤드리스 브라우저 불필요). 사이트가 구조를 바꾸면 이
파서가 0건을 반환할 수 있는데, 그 경우 호출부(management command)가
'파싱 실패'로 간주해 기존 데이터를 보존하도록 되어 있다.
"""
import re
from urllib.parse import urljoin, urlparse, parse_qs

from bs4 import BeautifulSoup

from .work24_client import BASE_URL


def _clean_text(text):
    return re.sub(r'\s+', ' ', text or '').strip()


def parse_listing_page(html):
    """검색 결과 한 페이지(HTML)를 파싱해 공고 dict 리스트를 반환한다.

    사이트 구조 변경 등으로 항목을 하나도 못 찾으면 빈 리스트를 반환한다
    (예외를 던지지 않음 — '이 페이지가 마지막 페이지라 0건'인 경우와
    '파싱이 깨져서 0건'인 경우를 호출부가 함께 취급해도 되기 때문).
    """
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('tr[id^="list"]')

    postings = []
    for row in rows:
        link_tag = row.select_one('a[data-emp-detail]')
        if not link_tag or not link_tag.get('href'):
            continue

        href = link_tag['href']
        query = parse_qs(urlparse(href).query)
        external_id = (query.get('wantedAuthNo') or [''])[0]
        if not external_id:
            continue

        company_tag = row.select_one('.cp_name')
        pay_tag = row.select_one('li.dollar')
        career_tag = row.select_one('li.member')
        region_tag = row.select_one('li.site')
        period_parts = [p.get_text(' ', strip=True) for p in row.select('td p.s1_r')]

        postings.append({
            'external_id': external_id,
            'title': _clean_text(link_tag.get_text(' ', strip=True)),
            'company_name': _clean_text(company_tag.get_text(' ', strip=True)) if company_tag else '',
            'pay_text': _clean_text(pay_tag.get_text(' ', strip=True)) if pay_tag else '',
            'career_text': _clean_text(career_tag.get_text(' ', strip=True)) if career_tag else '',
            'region_text': _clean_text(region_tag.get_text(' ', strip=True)) if region_tag else '',
            'period_text': _clean_text(' · '.join(period_parts)),
            'source_url': urljoin(BASE_URL, href),
        })
    return postings
