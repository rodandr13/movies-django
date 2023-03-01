from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Movie


class MovieView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movies.html"


class MovieDetailView(DetailView):
    model = Movie
    slug_field = "url"
