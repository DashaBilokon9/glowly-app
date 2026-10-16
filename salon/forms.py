from django import forms
from django.utils import timezone

from salon.models import Appointment


class AppointmentForm(forms.ModelForm):
    starts_at = forms.DateTimeField(
        label='Дата і час',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Appointment
        fields = ['service', 'specialist', 'client_name', 'client_phone', 'starts_at']

    def clean_client_phone(self):
        phone = self.cleaned_data['client_phone'].strip()
        digits = ''.join(character for character in phone if character.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Вкажіть номер щонайменше з 10 цифр.')
        return phone

    def clean_starts_at(self):
        starts_at = self.cleaned_data['starts_at']
        if starts_at <= timezone.now():
            raise forms.ValidationError('Оберіть час у майбутньому.')
        return starts_at

    def clean(self):
        cleaned = super().clean()
        service = cleaned.get('service')
        specialist = cleaned.get('specialist')
        if service and specialist and not specialist.services.filter(pk=service.pk).exists():
            raise forms.ValidationError('Цей майстер не виконує обрану послугу.')
        return cleaned
