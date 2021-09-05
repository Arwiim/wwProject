from django.contrib.sites import requests
from django.shortcuts import render
from pynytimes import NYTAPI
from blog.settings import NYC_KEY
from django.views.generic import CreateView, DetailView, ListView, UpdateView

# Create your views here.

nyt = NYTAPI(NYC_KEY, parse_dates=True)


# class WorldViewList(ListView):
    
#     # data_title = top_science_stories[0]['title']
#     # data_description = top_science_stories[0]['url']
#     # data_image_post = top_science_stories[0]['multimedia'][0]['url']
#     # data_image_post_description = top_science_stories[0]['multimedia'][0]['caption']
#     # data_url = top_science_stories[0]['short_url']
#     template_name = 'nytnews/lists_news.html'
    
    
#     def get_context_data(self, **kwargs):
        
#         top_science_stories = nyt.top_stories(section="world")[:1]
#         context = super().get_context_data(**kwargs)
#         context['top_science_stories'] = top_science_stories
#         return context
    
def WorldViewList(requests):
    
    top_world_stories = nyt.top_stories(section="world")[:1]
    return render(requests, 'nycnews/lists_news.html', context={'world': top_world_stories})
    

