from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.ModelSerializer):
    # 보안상의 이유로 클라이언트가 입력은 가능하지만 API응답에는 포함안시키기위해
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ('id', 'nickname', 'email', 'password')

    # 비밀전호를 평문으로 저장하지 않고 해싱해서 저장하기 위해사용
    # 이미 create_user에서 비밀번호 해싱처리되게 저장을함 필요 x
    # def create(self, validated_data):
    #     # pop메소드는 제거한 값을 반환함
    #     password = validated_data.pop('password', None)
    #     if not password:
    #         raise serializers.ValidationError("패스워드를 입력하세요")
    #     user = get_user_model().objects.create_user(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user

class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['pk','nickname','email','password','profile_image']
        READ_ONLY_FIELDS = ['pk','email']

        # 수정할 객체, 클라이언트가 보내는 형식
    def update(self, instance, validated_data):
        user = get_user_model().objects.get(pk=instance.pk)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            user.set_password(password)
        instance.save()
        return instance

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if not email or not password:
#             raise serializers.ValidationError("Email과 Password는 필수 입력 항목입니다")
#
#         user = authenticate(email=email, password=password)
#
#         if not user:
#             raise serializers.ValidationError("올바른 email과 password를 입력하세요.")
#
#         attrs['user'] = user
#
#         return attrs


# authenticate() : 사용자의 자격 증명을 확인하고, 유효한 경우 사용자 객체를 반환하는 함수,
# 인증이 성공하면 해당 사용자 객체(User)를 반환
# 인증이 실패하면 None을 반환
# 📌 self.context란?
# Django REST Framework(DRF)에서 Serializer는 뷰(View)에서 전달된 context를 가질 수 있음.
# self.context.get('request')로 요청 객체를 가져올 수 있음.
# serializer = UserLoginSerializer(data=request.data, context={"request": request})
# ✔ 즉, 기본적으로 attrs에는 email과 password가 있지만,
# ✔ request는 현재 요청을 보낸 사용자에 대한 추가적인 정보를 포함하는 역할을 함.
# Django 기본 인증 방식 중 하나인 **SessionAuthentication**을 사용할 경우, 로그인한 사용자의 세션을 확인할 수 있음.
# request를 전달하면, Django가 현재 세션에서 로그인된 사용자 정보를 확인하는 데 활용할 수 있음.
# ✔ authenticate(request, username, password)를 사용하면, Django가 세션을 유지하며 로그인할 수 있도록 지원

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), **attrs)
            if not user:
                raise serializers.ValidationError(
                    # 오류 메세지 표준화
                    # detail 오류 메시지 전달
                    # code 오류의 종류 지정
                    detail='Unable to log in with provided credentials.', code='authorization'
                )
        else:
            raise serializers.ValidationError(
                detail='Must be Required "email" and "password".', code='authorization'
            )

        attrs['user'] = user
        return attrs

