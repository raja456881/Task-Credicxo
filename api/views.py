from.searilizers import *
from rest_framework.response import Response
from  rest_framework import status
from rest_framework import viewsets
from .models import User, student
from rest_framework_simplejwt.authentication import JWTAuthentication
from.permission import teacherpermission, studentpermission, adminpermission
from django.utils.encoding import smart_bytes,smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import utils
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from rest_framework.generics import GenericAPIView


# Api for student resgister
class studentresgister(viewsets.ViewSet):
    def create(self, request):
        searilizers=studentsearilizers(data=request.data)
        if searilizers.is_valid(raise_exception=True):
            searilizers.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(searilizers.errors, status=status.HTTP_400_BAD_REQUEST)

# Request for teacher resgister
class teacheresgister(viewsets.ViewSet):
    def create(self, request):
        searilizers=teachersearilizers(data=request.data)
        if searilizers.is_valid(raise_exception=True):
            searilizers.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(searilizers.errors, status=status.HTTP_400_BAD_REQUEST)

# Api all user Details , Jwt authentication and access only superuser
class UserList(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [adminpermission]
    def list(self, request):
        queryset=User.objects.all()
        serializer_class = userseariizers(queryset, many=True)
        return  Response(serializer_class.data, status=status.HTTP_200_OK)

    def create(self, request):
        searilizers=userseariizers(data=request.data)
        if searilizers.is_valid():
           searilizers.save()
           return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



# Api for all student Details , Add student , access only teacher and teacher must authentication
class teacherlist(viewsets.ViewSet):
    permission_classes = [teacherpermission]
    def list(self, request):
        queryset = student.objects.all()
        serializer = studentlistsearilizers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self , request):
        searilizers=studentsearilizers(data=request.data)
        if searilizers.is_valid():
           searilizers.save()
           return Response(searilizers.data, status=status.HTTP_201_CREATED)
        return  Response(searilizers.errors, status=status.HTTP_400_BAD_REQUEST)

# Api for get student details (only for student) and  must authentication
class studentlist(viewsets.ViewSet):
    permission_classes = [studentpermission]
    def list(self, request):
        user=request.user
        try:
            snippte=student.objects.all().get(user=user)
            serializer = studentlistsearilizers(snippte)
            return Response(serializer.data)

        except:
              return Response({"error": 'user is not exit'}, status=status.HTTP_401_UNAUTHORIZED)


# Api for forgotpassword first need to be enter email id and then check this email id if user exits then next process
class Resetpasswordview(GenericAPIView):
    serializer_class = Restpasswordsearilizers

    def post(self, request):

        seralizers=self.serializer_class(data=request.data)
        email=request.data['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current=get_current_site(request).domain
            realtivelinj = reverse('password-rest-confirm', kwargs={'uidb64':uidb64, 'token':token})
            url = 'http://' + current + realtivelinj
            body='Hello \n Use link below toreset your password \n'+url
            data={"email_body":body, 'to_email':user.email  ,'subject':'Reset for password'}
            utils.send_mail(data)

        return Response({'success':'We have send you a link  to rest you password'}, status=status.HTTP_200_OK)

# Api for send link on email id to forgot password
class PasswordTokenCheckApi(GenericAPIView):
    def get(self, request,uidb64,token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not  PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'Token is not vaild, please request a new one'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'success':True, 'messages':'Credentails Valid','uidb64':uidb64, 'token':token}, status=status.HTTP_201_CREATED)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator():
                return Response({'error':'Token is not vaild, please request a new one'}, status=status.HTTP_406_NOT_ACCEPTABLE)



# Api for set new password but first entry token id , new password, uidb64
class setnewpassword(GenericAPIView):
    serializer_class = setnewpasswordsearilizers
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, "messages":"Password reset success"},status=status.HTTP_200_OK)

