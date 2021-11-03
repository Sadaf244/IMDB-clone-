from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly 
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle                                        
from watchlist_app.api.pagination import WatchlistPagination,WatchlistLOPagination,WatchlistCPagination
class ReviewUser(generics.ListAPIView):
    serializer_class = ReviewSerializer
     
    # def get_queryset(self):
    #     username=self.kwargs['username']#Filtering against the URL
    #     return Review.objects.filter(reviewer__username=username)#foreign key that why we specify __username unless we directly use
    
    def get_queryset(self):
        username = self.request.query_params.get('username',None)#Filtering against query parameters
        return Review.objects.filter(reviewer__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle,AnonRateThrottle]
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):#create review of particular that movie
        
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
             
        reviewer=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,reviewer=reviewer)
        if review_queryset.exists():
            raise ValidationError("you have already give your review")
        
        if watchlist.number_of_rating == 0:
            watchlist.avg_of_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_of_rating=(watchlist.avg_of_rating + serializer.validated_data['rating'])/2
        watchlist.number_of_rating=watchlist.number_of_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist,reviewer=reviewer)
        
class ReviewList(generics.ListAPIView):#concrete view class #The following classes are the concrete generic views.
                                             # If you're using generic views this is normally the level you'll be working 
                                             # at unless you need heavily customized behavior.
                                            #The view classes can be imported from rest_framework.generics.
    #queryset = Review.objects.all()
    
    serializer_class = ReviewSerializer
    #throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    #filter_backends = [DjangoFilterBackend]#Filterinng
    #filterset_fields = ['reviewer__username', 'active']
    # filter_backends = [filters.OrderingFilter]#Ordering
    # ordering_fields = ['rating']
    #permission_classes = [IsAuthenticated]# Object Level Permissions
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)#filter object according to movie
    
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]#Authenticate user can edit but other can only view the review
    throttle_classes = [ScopedRateThrottle]
    throttle_scope='review-detail'
# class ReviewDetail(mixins.RetrieveModelMixin,
#                     generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
        
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformMVS(viewsets.ModelViewSet):#Model Viewset-Because ModelViewSet extends GenericAPIView,
    
    queryset = StreamPlatform.objects.all() #you'll normally need to provide at least the queryset and serializer_class
    serializer_class = StreamPlatformSerializer#ReadOnlyModelViewSet -only provides the 'read-only' actions, .list() and .retrieve()
    permission_classes = [AdminOrReadOnly]
# class StreamPlatformVS(viewsets.ViewSet):#Viewset and Router
    # def list(self, request):
    #     queryset = StreamPlatform.objects.all()
    #     serializer = StreamPlatformSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = StreamPlatform.objects.all()
    #     watchlist = get_object_or_404(queryset, pk=pk)
    #     serializer = StreamPlatformSerializer(watchlist)
    #     return Response(serializer.data)
    # def create(self,request):
    #     serializer = StreamPlatformSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
    # def delete(self,request,pk):
    #     platform = StreamPlatform.objects.get(pk=pk)
    #     platform.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)




# class StreamPlatformAv(APIView):
#     def get(self,request):
#         platform=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(platform,many=True,context={'request': request})# Add when working with HyperlinkedRelatedField--->context={'request': request}
#         return Response(serializer.data)  
#     def post(self,request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)

# class StreamPlatformDetailAv(APIView):
    
#     def get(self,request,pk):
#         try:
#             platform=StreamPlatform.objects.get(pk=pk)
#             serializer=StreamPlatformSerializer(platform,context={'request': request})
#             return Response(serializer.data)
#         except:
#             StreamPlatform.DoesNotExist()
#             return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)

#     def put(self,request,pk):
        
#         platform=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self,request,pk):
#         platform=StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class WatchListGV(generics.ListAPIView):#SearchFilter
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title', 'platform__name']#'^' Starts-with search,'=' Exact matches.,'@' Full-text search. (Currently only supported Django's PostgreSQL backend.),'$' Regex search..
    pagination_class = WatchlistCPagination
class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request):
        movies=WatchList.objects.all()
        serializer=WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
            serializer=WatchListSerializer(movie)
            return Response(serializer.data)
        except:
            WatchList.DoesNotExist()
            return Response({'error':'Not found'},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):
        
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





