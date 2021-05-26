from .models import User, student, teacher
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import  force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed



class studentsearilizers(serializers.ModelSerializer):

	class Meta:
		model=User
		fields=('email', 'username', 'password')

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		user=User.objects.create_user(**validated_data, is_student=True, is_teacher=False)
		stu1=student.objects.create(user=user, username=username, email=email)
		return user


class teachersearilizers(serializers.ModelSerializer):

	class Meta:
		model=User
		fields=('email', 'username', 'password' )

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		user=User.objects.create_user(**validated_data, is_student=False, is_teacher=True)
		stu1=teacher.objects.create(user=user, username=username, email=email)
		return stu1


class userseariizers(serializers.ModelSerializer):
	class Meta:
		model=User
		fields = ('email', 'username', 'password', 'is_student', 'is_teacher')


class studentlistsearilizers(serializers.ModelSerializer):
	class Meta:
		model=student
		fields=('email', 'username')



class Restpasswordsearilizers(serializers.Serializer):
    email=serializers.EmailField(max_length=34)

    class Meta:
        fields=['email']




class setnewpasswordsearilizers(serializers.Serializer):
    password=serializers.CharField(min_length=6, max_length=68, write_only=True)
    token=serializers.CharField(min_length=1, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields=['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password=attrs.get('password', '')
            token=attrs.get('token', '')
            uidb64=attrs.get('uidb64', '')
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            print(user)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invaild', 401)
            user.set_password(password)
            user.save()
            return user
        except  Exception as e:
            AuthenticationFailed('The reset link is invaild', 401)
        return super().validate(attrs)
