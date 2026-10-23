from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from salon.forms import AppointmentForm
from salon.models import Service, Specialist


def home(request):
    return render(request, 'salon/intro.html', {
        'services': Service.objects.all(),
    })


def catalog(request):
    return render(request, 'salon/home.html', {
        'services': Service.objects.all(),
        'specialists': Specialist.objects.prefetch_related('services'),
    })


def service_list(request):
    return render(request, 'salon/service_list.html', {
        'services': Service.objects.prefetch_related('specialists'),
    })


def specialist_detail(request, pk):
    specialist = get_object_or_404(
        Specialist.objects.prefetch_related('services'),
        pk=pk,
    )
    return render(request, 'salon/specialist_detail.html', {
        'specialist': specialist,
    })


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Запис збережено. Ми зателефонуємо для підтвердження.'))
            return redirect('appointment_done')
    else:
        form = AppointmentForm(initial={
            'service': request.GET.get('service'),
            'specialist': request.GET.get('specialist'),
        })
    return render(request, 'salon/appointment_form.html', {'form': form})


def appointment_done(request):
    return render(request, 'salon/appointment_done.html')
