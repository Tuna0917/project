Ctrl + Shift + P으로 Python Interpreter 지정

$ django-admin startproject myblog

settings.py
```python
TEMPLATES = [ ...
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    ...
]

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ko-kr'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

#USE_TZ = True
USE_TZ = False
```

$ python manage.py migrate <br>
$ python manage.py createsuperuser <br>
$ python manage.py startapp bookmark

```python
INSTALLED_APPS += ['bookmark.apps.BookmarkConfig',]
```

static 사용하려면

```python
STATIC_URL = '/static/'

STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, "static"),
]

```

```python
#settings.py
INSTALLED_APPS += [
    'taggit.apps.TaggitAppConfig',
    'taggit_templatetags2',
    ]
    
# For taggit
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TAGGIT_CASE_INSENSITIVE = True
TAGGIT__LIMIT = 50

#models.py
from taggit.managers import TaggableManager
```

---
login

django에서 제공하는 기능

```python
#setting.py
'''
설정해야하는거
LOGIN_URL 
LOGIN_REDIRECT_URL 
LOGOUT_REDIRECT_URL 로그아웃은 리다이렉트가 필요없을수도
'''

# LOGIN_URL = '/account/login/' 디폴트
# LOGIN_REDIRECT_URL = '/account/profile/' 디폴트
LOGIN_REDIRECT_URL = '/' #home으로
INSTALLED_APPS += [
    'widget_tweaks',
]
```
