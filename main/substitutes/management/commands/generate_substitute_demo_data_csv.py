import csv
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from analytics.models import CanonicalSport
from analytics.services.normalizers import normalize_region, normalize_sport
from substitutes.models import CenterContact, Posting
from substitutes.services.phone import hash_phone, mask_phone

CSV_PATH = settings.BASE_DIR / 'data' / 'substitute_postings_demo.csv'
INSTITUTION_PREFIX = '데모-'


def _day(offset):
    return timezone.localdate() + timedelta(days=int(offset))


class Command(BaseCommand):
    help = f'단기 대타 공고 목록을 {CSV_PATH.name}의 더미 데이터로 채웁니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--refresh', action='store_true',
            help='기존 더미 공고를 먼저 삭제하고 다시 생성합니다.',
        )

    def handle(self, *args, **options):
        already_exists = Posting.objects.filter(
            manager__institution_name__startswith=INSTITUTION_PREFIX,
        ).exists()
        if already_exists and not options['refresh']:
            self.stdout.write('더미 공고가 이미 존재합니다. 다시 생성하려면 --refresh 옵션을 사용하세요.')
            return

        if not CSV_PATH.exists():
            self.stderr.write(f'{CSV_PATH} 파일이 없습니다.')
            return

        with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
            rows = list(csv.DictReader(f))

        if already_exists:
            deleted, _ = Posting.objects.filter(
                manager__institution_name__in={row['institution_name'] for row in rows},
            ).delete()
            self.stdout.write(f'기존 더미 공고 {deleted}건을 삭제했습니다.')

        sport_cache = {}

        def get_sport(name):
            if name not in sport_cache:
                normalized = normalize_sport(name)
                sport_cache[name], _ = CanonicalSport.objects.get_or_create(
                    normalized_name=normalized, defaults={'name': name, 'is_active': True},
                )
            return sport_cache[name]

        manager_cache = {}

        def get_manager(institution_name, phone):
            if institution_name not in manager_cache:
                manager_cache[institution_name], _ = CenterContact.objects.update_or_create(
                    phone_hash=hash_phone(phone),
                    defaults={
                        'phone_masked': mask_phone(phone),
                        'institution_name': institution_name,
                        'verified_at': timezone.now(),
                    },
                )
            return manager_cache[institution_name]

        created = 0
        for row in rows:
            manager = get_manager(row['institution_name'], row['manager_phone'])
            certs = [value.strip() for value in row['required_certifications'].split('|') if value.strip()]
            Posting.objects.create(
                manager=manager, sport=get_sport(row['sport']),
                work_date=_day(row['work_date_offset_days']),
                start_time=row['start_time'], end_time=row['end_time'],
                region=row['region'], normalized_region=normalize_region(row['region']),
                address=row['address'], required_certifications=certs,
                pay_amount=int(row['pay_amount']), pay_unit=row['pay_unit'],
                headcount=int(row['headcount']), description=row['description'],
                status=row['status'],
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f'더미 대타 공고 {created}건을 생성했습니다.'))
