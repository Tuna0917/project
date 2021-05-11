import os
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile

# image-kit, sorl-thumbnail, easy-thumbnails을 사용해볼까?

class ThumbnailImageFieldFile(ImageFieldFile): #ImageFieldFile 상속받음
    def _add_thumb(self, s):
        parts = s.split(".")
        parts.insert(-1, "thumb")
        if parts[-1].lower() not in ['jpeg', 'jpg']:
            parts[-1] = 'jpg'
        return ".".join(parts)

    #@property를 사용해서 메서드를 멤버변수처럼 사용할 수 있음.
    #웜본 파일의 경로 path속성에 썸네일의 경로 thumb_path를 추가할 수 있음.
    @property
    def thumb_path(self):
        return self._add_thumb(self.path)

    #웜본 파일의 URL인 url속성에 썸네일의 URL인 thumb_url을 추가할 수 있음.
    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    def save(self, name, content, save=True): #파일시스템에 파일을 저장하고 생성하는 메서드
        super().save(name, content, save) #부모 ImageFieldFile클래스의 save()메서드를 호출해서 원본 이미지를 저장.

        img = Image.open(self.path)
        size = (self.field.thumb_width, self.field.thumb_height)
        img.thumbnail(size) #PIL 라이브러리의 썸네일 만드는 함수임. Image.thumbnail()이라는 함수를 이용하여 썸네일 제작.
        background = Image.new('RGB', size, (255, 255, 255))
        box = (int((size[0]- img.size[0]) / 2), int((size[1] - img.size[1]) / 2))
        background.paste(img, box)
        background.save(self.thumb_path, 'JPEG') #img와 box를 함쳐 만든 최종 썸네일을 JPEG형식으로 thumb_path 경로에 저장.

    def delete(self, save=True): #원본과 썸네일을 모두 삭제.
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)

class ThumbnailImageField(ImageField): #ImageField를 상속, models.py에서 사용하는 메서드.
    #새로운 FileField클래스를 정의할 때는 그에 상응하는 File처리 클래스를 attr_class 속성에 꼭 지정해줘야함.
    #line5에서 만들어둔 ThumbnailImageFieldFile 클래스로 지정.
    attr_class = ThumbnailImageFieldFile 

    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs): #디폴트가 128px
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)