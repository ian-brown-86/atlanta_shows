from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Venue, Photo
from .forms import ShowsForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'atlanta-shows-52'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def venues_index(request):
    venues = Venue.objects.all()
    return render(request, 'venues/index.html', {'venues': venues})

@login_required
def venues_detail(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    shows_form = ShowsForm()
    return render(request, 'venues/detail.html', {
        'venue': venue,
        'shows_form': shows_form
    })

@login_required
def add_shows(request, venue_id):
    print(request.POST)
    form = ShowsForm(request.POST)
    if form.is_valid():
        new_shows = form.save(commit=False)
        new_shows.venue_id = venue_id
        new_shows.save()
    return redirect('detail', venue_id=venue_id)

@login_required
def add_photo(request, venue_id):
    photo_file = request.FILES.get('photo-file')
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, venue_id=venue_id)
            photo.save()
        except:
            print('An error occured uploading file')
    return redirect('detail', venue_id=venue_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class VenueCreate(LoginRequiredMixin, CreateView):
  model = Venue
  fields = '__all__'
  success_url = '/venues/'

class VenueUpdate(LoginRequiredMixin, UpdateView):
  model = Venue
  fields = '__all__'

class VenueDelete(LoginRequiredMixin, DeleteView):
  model = Venue
  success_url = '/venues/'