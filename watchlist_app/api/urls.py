from watchlist_app.api.views import (WatchListAV, WatchListDetailAV,
                                     ReviewList,ReviewCreate,StreamPlatformMVS,
                                      ReviewDetail,ReviewUser,WatchListGV)
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatformMVS,basename='streamplatform')

urlpatterns = [
    path('list/',  WatchListAV.as_view(),name='movie-list'),
    path('<int:pk>', WatchListDetailAV.as_view(),name='movie-details'),
    path('newlist/',  WatchListGV.as_view(),name='new-list'),#used for test purpose for searchfilter
    path('', include(router.urls)),
    #path('stream/',StreamPlatformAv.as_view(),name='stream'),
    #path('stream/<int:pk>',StreamPlatformDetailAv.as_view(),name='streamplatform-detail'),
    
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/review/',ReviewList.as_view(),name='review-list'),#to get specific review of specific movie means movie id used
    path('review/<int:pk>/',ReviewDetail.as_view(),name='review-detail'),#to get specific review means review id used
    #path('reviews/<str:username>/',ReviewUser.as_view(),name='review-user'),#Filtering against the URL
    path('reviews/',ReviewUser.as_view(),name='review-user'),#Filtering against query parameters
    #path('review',ReviewList.as_view(),name='review-list'),
    #path('review/<int:pk>',ReviewDetail.as_view(),name='review-detail'),
]