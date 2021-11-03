from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from user_app import models

@api_view(['POST',])
def logout_view(request):

    if request.method=='POST':
        request.user.auth_token.delete()#request.user-current logged in user and auth token to obtain token of that user
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):

    if request.method=='POST':
        serializer=RegistrationSerializer(data=request.data)
        
        data={}
        

        if serializer.is_valid():
            account=serializer.save()#serializer save function call here
            
            data['response']="Registration Successful"
            data['username']=account.username#storing data 
            data['email']=account.email

            token=Token.objects.get(user=account).key#fetching token 
            data['token']=token
        else:
            data = serializer.errors
        return Response(data,status.HTTP_201_CREATED)#username and email is sent here because password is writeonly
    
