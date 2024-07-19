from django.contrib.auth import get_user_model, authenticate, login, logout

from django.shortcuts import redirect

from .models import Notification
from .serializers import UserSerializer,NotificationSerializer

from rest_framework.views import APIView, Response, status
from rest_framework import viewsets, permissions, generics


def isexistlower(li):
    if li[0].islower():
        return True
    try:
        return isexistlower([li[i] for i in range(1,len(li))])
        # return isexistlower(li[1,])
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
    

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        pas = request.data['password']
        pas_list = pas
        
        if request.data["username"] == "":
            return Response({"status":"Hãy nhập tên"}, status=status.HTTP_400_BAD_REQUEST)
        if "@" in request.data["username"]:
            return Response({"status":"Tên đăng nhập không thể chứa kí tự @"}, status=status.HTTP_400_BAD_REQUEST)
        if get_user_model().objects.filter(username=request.data["username"]):
            return Response({"status":"Đã có tài khoản đăng ký với tên này"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data["email"] == "":
            return Response({"status":"Hãy nhập email"}, status=status.HTTP_400_BAD_REQUEST)
        if not "@" in request.data["email"]:
            return Response({"status":"Email phải chứa kí tự @"}, status=status.HTTP_400_BAD_REQUEST)
        if get_user_model().objects.filter(email=request.data["email"]):
            return Response({"status":"Đã có tài khoản đăng ký với email này"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if len(pas) < 8:
            return Response({"status":"Mật khẩu phải chứa ít nhất 8 kí tự"}, status=status.HTTP_400_BAD_REQUEST)
        if pas.isdigit():
            return Response({"status":"Mật khẩu không thể hoàn toàn đều là số"}, status=status.HTTP_400_BAD_REQUEST)
        if not isexistlower(pas_list):
            return Response({"status":"Mật khẩu cần chứa kí tự viết thường"}, status=status.HTTP_400_BAD_REQUEST)
        if not isexistupper(pas_list):
            return Response({"status":"Mật khẩu cần chứa kí tự viết hoa"}, status=status.HTTP_400_BAD_REQUEST)
        if not isexistspecial(pas_list):
            return Response({"status":"Mật khẩu cần chứa kí tự đặc biệt"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data['re_password'] != request.data['password']:
            return Response({"status": "Mật khẩu không khớp"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Đăng ký thành công"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogInView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if '@' in username:       
            try:
                user = get_user_model().objects.get(email=username)
                username = user.username
            except get_user_model().DoesNotExist:
                return Response({"status":"Email hoặc mật khẩu sai"}, status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request=request,user=user)    
            return Response({"status":"Đăng nhập thành công"},status=status.HTTP_200_OK)
        
        return Response({"status":"Tên đăng nhập hoặc mật khẩu sai"}, status=status.HTTP_404_NOT_FOUND)
    
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