from .base import *
print('*' * 100)
print('loacl')
print('*' * 100)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRET["DB"]["NAME"],         # 데이터베이스 이름
        'USER': SECRET["DB"]["USER"],            # MySQL 사용자 이름
        'PASSWORD': SECRET["DB"]["PASSWORD"],    # MySQL 비밀번호
        'HOST': SECRET["DB"]["HOST"],                  # MySQL 서버 주소 (기본: localhost)
        'PORT': SECRET["DB"]["PORT"],
    }
}