from django.urls import path, re_path, include
from statistics_output.views import itemization, statistics, vector_statistics

'''
urlpatterns = [
    path('<int:year>', year_statistics),
    path('<int:year>/<int:month>/<str:category>', month_statistics),
    path('<int:year>/<int:month>/<str:category>', itemization)
]
'''

mode_and_date_urls = [
    path('<int:year>/', vector_statistics),
    path('<int:year>/<int:month>/', vector_statistics),
    re_path(r'(?P<mode>vector)/(?P<year>\d{4})/$', vector_statistics),
    re_path(r'(?P<mode>vector)/(?P<year>\d{4})/(?P<month>\d{1,2})/$', vector_statistics),
]

urlpatterns = [
    path('', include(mode_and_date_urls)),
    re_path(r'(?P<parent_category>[а-яА-Я]*)/', include(mode_and_date_urls)),
]
