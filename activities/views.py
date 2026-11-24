from datetime import date as today_date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Run


def check_run(date, distance, hours, minutes, seconds):
    # Used by add_run and edit_run so the rules are only written once.
    # Returns a list of error messages (empty list = everything is fine).
    errors = []

    if not date:
        errors.append('Pick the date of your run.')

    try:
        if float(distance) <= 0:
            errors.append('Distance must be more than 0 miles.')
    except ValueError:
        errors.append('Enter the distance as a number, like 3.1.')

    if not (hours.isdigit() and minutes.isdigit() and seconds.isdigit()):
        errors.append('Hours, minutes and seconds must be whole numbers.')
    elif int(minutes) > 59 or int(seconds) > 59:
        errors.append('Minutes and seconds must be 59 or less.')
    elif int(hours) + int(minutes) + int(seconds) == 0:
        errors.append('Enter how long your run took.')

    return errors


# Show the logged-in user's runs (not everyone's)
@login_required
def run_list(request):
    runs = request.user.runs.all()

    return render(request, 'activities/run_list.html', {'runs': runs})


@login_required
def add_run(request):
    errors = []
    # Start the form with today's date and empty boxes
    title = ''
    date = today_date.today().isoformat()
    distance = ''
    hours = minutes = seconds = '0'
    notes = ''

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date = request.POST.get('date', '').strip()
        distance = request.POST.get('distance', '').strip()
        # An empty time box counts as 0
        hours = request.POST.get('hours', '').strip() or '0'
        minutes = request.POST.get('minutes', '').strip() or '0'
        seconds = request.POST.get('seconds', '').strip() or '0'
        notes = request.POST.get('notes', '').strip()

        errors = check_run(date, distance, hours, minutes, seconds)

        if not errors:
            Run.objects.create(user=request.user, title=title, date=date, distance=distance,
                               hours=hours, minutes=minutes, seconds=seconds, notes=notes)
            return redirect('run_list')

    # GET, or POST with errors: show the form and keep what they typed
    return render(request, 'activities/add_run.html', {
        'errors': errors,
        'title': title,
        'date': date,
        'distance': distance,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'notes': notes,
    })


@login_required
def edit_run(request, run_id):
    # user=request.user means you can only open your own runs (anyone else's gives a 404)
    run = get_object_or_404(Run, id=run_id, user=request.user)
    errors = []

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        date = request.POST.get('date', '').strip()
        distance = request.POST.get('distance', '').strip()
        hours = request.POST.get('hours', '').strip() or '0'
        minutes = request.POST.get('minutes', '').strip() or '0'
        seconds = request.POST.get('seconds', '').strip() or '0'
        notes = request.POST.get('notes', '').strip()

        errors = check_run(date, distance, hours, minutes, seconds)

        if not errors:
            run.title = title
            run.date = date
            run.distance = distance
            run.hours = hours
            run.minutes = minutes
            run.seconds = seconds
            run.notes = notes
            run.save()
            return redirect('run_list')
    else:
        # GET: fill the form with the run's current details
        title = run.title
        date = run.date.isoformat()  # the date box needs "YYYY-MM-DD"
        distance = run.distance
        hours = run.hours
        minutes = run.minutes
        seconds = run.seconds
        notes = run.notes

    return render(request, 'activities/edit_run.html', {
        'run': run,
        'errors': errors,
        'title': title,
        'date': date,
        'distance': distance,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'notes': notes,
    })


@login_required
def delete_run(request, run_id):
    run = get_object_or_404(Run, id=run_id, user=request.user)

    # GET: show an "are you sure?" page. POST: delete it.
    if request.method == 'POST':
        run.delete()
        return redirect('run_list')

    return render(request, 'activities/delete_run.html', {'run': run})
