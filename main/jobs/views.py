from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from analytics.services.normalizers import normalize_region

from . import selectors
from .forms import ApplyForm, JobPostingForm, ManagerVerifyForm, PostingDeleteForm
from .models import Application, CenterContact, JobPosting, PhoneIdentity
from .services.certification import has_required_certification
from .services.phone import hash_phone, mask_phone
from .services.tokens import generate_management_token, verify_management_token


MANAGER_SESSION_KEY = 'jobs_manager_phone_hash'


def job_list(request):
    postings = selectors.apply_job_filters(request.GET)
    page_obj = Paginator(postings, 20).get_page(request.GET.get('page'))
    context = selectors.filter_options()
    context.update({'page_obj': page_obj, 'current': request.GET})
    return render(request, 'jobs/list.html', context)


def job_detail(request, pk):
    posting = get_object_or_404(JobPosting.objects.select_related('sport', 'manager'), pk=pk)
    return render(request, 'jobs/detail.html', {'posting': posting})


def job_delete_request(request, pk):
    posting = get_object_or_404(JobPosting.objects.select_related('manager'), pk=pk)
    if request.method == 'POST':
        form = PostingDeleteForm(request.POST)
        if form.is_valid():
            phone_hash = hash_phone(form.cleaned_data['phone'])
            password = form.cleaned_data['password']
            if phone_hash != posting.manager.phone_hash or not check_password(password, posting.manager.password_hash):
                form.add_error(None, '담당자 휴대폰 번호 또는 비밀번호가 일치하지 않습니다.')
            else:
                posting.delete()
                messages.success(request, '공고를 삭제했습니다.')
                return redirect('jobs:job_list')
    else:
        form = PostingDeleteForm()
    return render(request, 'jobs/delete_confirm.html', {'posting': posting, 'form': form})


def application_apply(request, pk):
    posting = get_object_or_404(JobPosting, pk=pk)
    if posting.status != JobPosting.Status.RECRUITING:
        messages.error(request, '이미 마감되었거나 완료된 공고입니다.')
        return redirect('jobs:job_detail', pk=posting.pk)

    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            phone_hash = hash_phone(form.cleaned_data['phone'])
            phone_masked = mask_phone(form.cleaned_data['phone'])
            password = form.cleaned_data['password']
            existing = PhoneIdentity.objects.filter(phone_hash=phone_hash).first()
            if existing and not check_password(password, existing.password_hash):
                form.add_error('password', '이전에 이 번호로 지원할 때 등록한 비밀번호와 일치하지 않습니다.')
            elif not has_required_certification(phone_hash, posting.required_certifications):
                messages.error(request, '이 공고에 필요한 자격증 보유자만 지원할 수 있습니다.')
            elif Application.objects.filter(job_posting=posting, phone_identity__phone_hash=phone_hash).exists():
                messages.error(request, '이미 지원한 공고입니다.')
            else:
                phone_identity = existing or PhoneIdentity.objects.create(
                    phone_hash=phone_hash, phone_masked=phone_masked,
                    password_hash=make_password(password),
                )
                application = Application.objects.create(
                    job_posting=posting, phone_identity=phone_identity,
                    phone_masked=phone_masked, message=form.cleaned_data['message'],
                    certification_verified=True,
                )
                return render(request, 'jobs/apply_complete.html', {
                    'posting': posting, 'application': application,
                })
    else:
        form = ApplyForm()
    return render(request, 'jobs/apply.html', {'posting': posting, 'form': form})


def job_create(request):
    manager_phone_hash = request.session.get(MANAGER_SESSION_KEY)
    manager = None
    if manager_phone_hash:
        manager = CenterContact.objects.filter(phone_hash=manager_phone_hash).first()

    if manager is None:
        if request.method == 'POST':
            verify_form = ManagerVerifyForm(request.POST)
            if verify_form.is_valid():
                phone_hash = hash_phone(verify_form.cleaned_data['phone'])
                password = verify_form.cleaned_data['password']
                existing = CenterContact.objects.filter(phone_hash=phone_hash).first()
                if existing and not check_password(password, existing.password_hash):
                    verify_form.add_error('password', '이전에 이 번호로 등록한 비밀번호와 일치하지 않습니다.')
                else:
                    manager, _ = CenterContact.objects.update_or_create(
                        phone_hash=phone_hash,
                        defaults={
                            'phone_masked': mask_phone(verify_form.cleaned_data['phone']),
                            'institution_name': verify_form.cleaned_data['institution_name'],
                            'business_reg_no': verify_form.cleaned_data['business_reg_no'],
                            'password_hash': existing.password_hash if existing else make_password(password),
                            'verified_at': timezone.now(),
                        },
                    )
                    request.session[MANAGER_SESSION_KEY] = phone_hash
                    return redirect('jobs:job_create')
        else:
            verify_form = ManagerVerifyForm()
        return render(request, 'jobs/create_verify.html', {'form': verify_form})

    if request.method == 'POST':
        posting_form = JobPostingForm(request.POST)
        if posting_form.is_valid():
            posting = posting_form.save(commit=False)
            posting.manager = manager
            posting.normalized_region = normalize_region(posting.region)
            posting.save()
            management_url = request.build_absolute_uri(
                reverse('jobs:applicant_manage', args=[posting.pk, generate_management_token(posting.pk)]),
            )
            messages.success(
                request,
                f'공고가 등록되었습니다. 아래 관리 링크로 지원자 확인을 할 수 있으니 보관해주세요.\n{management_url}',
            )
            return redirect('jobs:job_detail', pk=posting.pk)
    else:
        posting_form = JobPostingForm()
    return render(request, 'jobs/create.html', {'form': posting_form, 'manager': manager})


def job_manager_reset(request):
    request.session.pop(MANAGER_SESSION_KEY, None)
    return redirect('jobs:job_create')


def _get_posting_for_token(pk, token):
    posting_id = verify_management_token(token)
    if posting_id != pk:
        raise Http404('관리 링크가 올바르지 않습니다.')
    return get_object_or_404(JobPosting.objects.select_related('sport', 'manager'), pk=pk)


def applicant_manage(request, pk, token):
    posting = _get_posting_for_token(pk, token)
    applications = posting.applications.select_related('phone_identity').order_by('-applied_at')
    return render(request, 'jobs/manage.html', {
        'posting': posting, 'applications': applications, 'token': token,
    })


def job_delete(request, pk, token):
    posting = _get_posting_for_token(pk, token)
    if request.method == 'POST':
        posting.delete()
        messages.success(request, '공고를 삭제했습니다.')
        return redirect('jobs:job_list')
    return redirect('jobs:applicant_manage', pk=posting.pk, token=token)
