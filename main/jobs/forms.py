from django import forms

from analytics.models import CanonicalSport

from .models import JobPosting


CERTIFICATION_CHOICES = [
    ('생활스포츠지도사 2급', '생활스포츠지도사 2급'),
    ('생활스포츠지도사 1급', '생활스포츠지도사 1급'),
    ('유소년스포츠지도사', '유소년스포츠지도사'),
    ('노인스포츠지도사', '노인스포츠지도사'),
    ('장애인스포츠지도사', '장애인스포츠지도사'),
    ('인명구조자격', '인명구조자격'),
]


def _apply_widget_classes(fields):
    for field in fields.values():
        widget = field.widget
        if isinstance(widget, (forms.CheckboxSelectMultiple, forms.RadioSelect, forms.CheckboxInput)):
            continue
        css_class = 'form-select' if isinstance(widget, forms.Select) else 'form-control'
        widget.attrs['class'] = f"{widget.attrs.get('class', '')} {css_class}".strip()


class ManagerVerifyForm(forms.Form):
    institution_name = forms.CharField(label='기관명', max_length=200)
    business_reg_no = forms.CharField(label='사업자등록번호', max_length=20, required=False, help_text='선택 입력입니다.')
    phone = forms.CharField(label='담당자 휴대폰 번호', max_length=20)
    password = forms.CharField(
        label='비밀번호', widget=forms.PasswordInput, min_length=4, max_length=20,
        help_text='같은 번호로 다시 공고를 등록할 때 필요하니 잊지 마세요.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)


class JobPostingForm(forms.ModelForm):
    required_certifications = forms.MultipleChoiceField(
        label='필요 자격증', choices=CERTIFICATION_CHOICES, widget=forms.CheckboxSelectMultiple, required=False,
    )

    class Meta:
        model = JobPosting
        fields = [
            'title', 'sport', 'employment_type', 'work_start_date', 'work_end_date',
            'region', 'address', 'career_requirement', 'required_certifications',
            'pay_type', 'pay_amount', 'pay_negotiable', 'headcount',
            'application_deadline', 'description',
        ]
        labels = {
            'title': '공고 제목', 'sport': '종목', 'employment_type': '고용 형태',
            'work_start_date': '근무 시작일', 'work_end_date': '근무 종료일(정규직은 비워두세요)',
            'region': '지역', 'address': '근무지 주소', 'career_requirement': '경력 조건',
            'pay_type': '급여 단위', 'pay_amount': '급여액', 'pay_negotiable': '면접 후 협의',
            'headcount': '모집 인원', 'application_deadline': '지원 마감일(상시모집은 비워두세요)',
            'description': '상세 내용',
        }
        widgets = {
            'work_start_date': forms.DateInput(attrs={'type': 'date'}),
            'work_end_date': forms.DateInput(attrs={'type': 'date'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'career_requirement': forms.TextInput(attrs={'placeholder': '예: 경력 2년 이상, 신입 가능 등'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sport'].queryset = CanonicalSport.objects.filter(is_active=True).order_by('name')
        _apply_widget_classes(self.fields)

    def clean_region(self):
        return self.cleaned_data['region'].strip()

    def clean(self):
        cleaned = super().clean()
        pay_negotiable = cleaned.get('pay_negotiable')
        pay_amount = cleaned.get('pay_amount')
        if not pay_negotiable and not pay_amount:
            self.add_error('pay_amount', '급여액을 입력하거나 "면접 후 협의"를 선택해주세요.')
        work_start = cleaned.get('work_start_date')
        work_end = cleaned.get('work_end_date')
        if work_start and work_end and work_end < work_start:
            self.add_error('work_end_date', '근무 종료일은 시작일보다 빠를 수 없습니다.')
        return cleaned


class PostingDeleteForm(forms.Form):
    phone = forms.CharField(label='담당자 휴대폰 번호', max_length=20, help_text='공고 등록 시 입력했던 번호를 입력해 주세요.')
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)


class ApplyForm(forms.Form):
    name = forms.CharField(label='이름', max_length=50)
    phone = forms.CharField(label='휴대폰 번호', max_length=20)
    password = forms.CharField(
        label='비밀번호', widget=forms.PasswordInput, min_length=4, max_length=20,
        help_text='같은 번호로 다시 지원할 때 본인 확인에 사용됩니다.',
    )
    message = forms.CharField(
        label='지원 메시지', required=False, widget=forms.Textarea(attrs={'rows': 4}),
        help_text='경력, 자기소개 등을 자유롭게 적어주세요. (선택)',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_widget_classes(self.fields)
