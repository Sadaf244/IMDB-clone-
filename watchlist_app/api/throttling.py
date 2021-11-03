from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope='review-create'

class ReviewListThrottle(UserRateThrottle):
    scope='review-list'
#Throttling is used whenever we used any limitaion on rquest that we can give
#  user to acess any request 2-3 time time and the another condition gave to user