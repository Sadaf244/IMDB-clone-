from rest_framework.authtoken.views import obtain_auth_token# obtain_auth_token-this gives acess to token if we pass username and password
from user_app.api.views import registration_view,logout_view
from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('login/', obtain_auth_token ,name='login'),
    path('registration/',registration_view,name='registration'),
    path('logout/', logout_view,name='logout'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]