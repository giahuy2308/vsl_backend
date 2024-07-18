from django.contrib.auth import get_user_model, authenticate, login, logout

from django.shortcuts import redirect

from .models import Notification
from .serializers import UserSerializer,NotificationSerializer

from rest_framework.views import APIView, Response, status
from rest_framework import viewsets,permissions


def isexistlower(li):
    if li[0].islower():
        return True
    try:
        return isexistlower([li[i] for i in range(1,len(li))])
    except IndexError:
        return False
def isexistupper(li):
    if li[0].isupper():
        return True
    try:
        return isexistupper([li[i] for i in range(1,len(li))])
    except IndexError:
        return False
    
def isexistspecial(li):
    if not li[0].isupper() and not li[0].islower() and not li[0].isdigit():
        return True
    try:
        return isexistspecial([li[i] for i in range(1,len(li))])
    except IndexError:
        return False
    

class SignUpView(APIView):

    def post(self, request):
        passconf = request.data['password']
        passconf_list = list(passconf)
        if len(passconf) < 8:
            return Response({"status":"Mật khẩu phải chứa ít nhất 8 kí tự"})
        if passconf.isdigit():
            return Response({"status":"Mật khẩu không thể hoàn toàn đều là số"})
        if not isexistlower(passconf_list):
            return Response({"status":"Mật khẩu cần chứa kí tự viết thường"})
        if not isexistupper(passconf_list):
            return Response({"status":"Mật khẩu cần chứa kí tự viết hoa"})
        if not isexistspecial(passconf_list):
            return Response({"status":"Mật khẩu cần chứa kí tự đặc biệt"})
        
        if request.data['re_password'] != request.data['password']:
            return Response({"status": "Mật khẩu không khớp"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if '@' in username:       
            try:
                user = get_user_model().objects.get(email=username)
                username = user.username
            except get_user_model().DoesNotExist:
                return Response({"status":"Email or password incorrect"})
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request=request,user=user)    
            return Response({"status":"Sign in successfully"})
        
        return Response({"status":"Username or password incorrect"})
    
class LogOutView(APIView):

    def get(self,request):
        logout(request)
        return redirect('login')
    

class NotificationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)         