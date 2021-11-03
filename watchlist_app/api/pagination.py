from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
class WatchlistPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page_no'#http://localhost:8000/watch/newlist/?page_no=4
    last_page_strings='end'#http://localhost:8000/watch/newlist/?page_no=end
    page_size_query_param='size'#For 
    max_page_size = 10          #User customization

class WatchlistLOPagination(LimitOffsetPagination):
    default_limit= 3
    max_limit=10
    limit_query_param='limit'#http://localhost:8000/watch/newlist/?limit=5&start=6
    offset_query_param='start'
class WatchlistCPagination(CursorPagination):
    page_size = 3
    cursor_query_param='ordering'
    ordering='created'#By default='-created'