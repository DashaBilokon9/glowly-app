from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from salon.models import Appointment, Service, Specialist


class AppointmentForm(forms.ModelForm):
    starts_at = forms.DateTimeField(
        label=_('Дата і час'),
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Appointment
        fields = ['service', 'specialist', 'client_name', 'client_phone', 'starts_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].label = _('Послуга')
        self.fields['specialist'].label = _('Майстер')
        self.fields['client_name'].label = _("Ім'я")
        self.fields['client_phone'].label = _('Телефон')
        self.fields['service'].label_from_instance = lambda obj: obj.localized_name
        self.fields['specialist'].label_from_instance = lambda obj: obj.localized_name
        self.fields['service'].queryset = Service.objects.all()
        self.fields['specialist'].queryset = Specialist.objects.all()

    def clean_client_phone(self):
        phone = self.cleaned_data['client_phone'].strip()
        digits = ''.join(character for character in phone if character.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError(_('Вкажіть номер щонайменше з 10 цифр.'))
        return phone

    def clean_starts_at(self):
        starts_at = self.cleaned_data['starts_at']
        if starts_at <= timezone.now():
            raise forms.ValidationError(_('Оберіть час у майбутньому.'))
        return starts_at

    def clean(self):
        cleaned = super().clean()
        service = cleaned.get('service')
        specialist = cleaned.get('specialist')
        if service and specialist and not specialist.services.filter(pk=service.pk).exists():
            raise forms.ValidationError(_('Цей майстер не виконує обрану послугу.'))
        return cleaned
