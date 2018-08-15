from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your views here.
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunzhixu import YunZhiXun
from random import choice
from .models import VerifyCode


User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证, 重写authenticate方法，为手机注册登录放行
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    create:
          发送短信验证码
    """
    serializer_class = SmsSerializer

    @staticmethod
    def get_code():
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 字段验证
        mobile = serializer.validated_data['mobile']
        yzx = YunZhiXun()
        code = self.get_code()
        sms_status = yzx.send_sms(mobile, code)
        if sms_status['code'] == "000000":
            verify_code = VerifyCode(code=code, mobile=mobile)
            verify_code.save()
            return Response(data={
                "mobile": sms_status["msg"],
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    create:
          用户注册
    retrieve:
        用户信息
    update：
        全部更新
    partial_update：
        部分更新
    """
    # 为每个方法配置说明，在api文档可见

    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # 配置登录认证方式，暂时配置session了用，方便测试
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated, )
    # 用户注册时，不应该要求登录，因此此时这样配置是不可以的，需要针对每个方法进行权限控制

    def get_serializer_class(self):
        """
        重载该方法，该方法返回serializer_class，根据不同请求返回不同serializer
        :return: 
        """
        if self.action == "create":
            return UserRegSerializer
        else:
            return UserDetailSerializer

    def get_permissions(self):
        """
        重写权限控制方法
        :return: 
        """
        if self.action == "retrieve":
            return [IsAuthenticated()]
        elif self.action == "create":
            # 如果是注册，不验证权限
            return []
        else:
            return []

    # 重载，注册之后生成jwt token 并返回
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data  # 获取数据
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        re_dict['token'] = token
        re_dict['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """
        重写该方法， Retrieve, Destroy都会用到该方法，返回一个对象实例
        实现用户随意传递一个信息，返回的都是用户自身信息
        :return: 
        """
        return self.request.user

    def perform_create(self, serializer):
        """
        重写，将用户序列化数据返回
        :param serializer: 
        :return: 
        """
        return serializer.save()  # UserRegSerializer  model对象
