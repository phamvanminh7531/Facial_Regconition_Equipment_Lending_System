from django.db import models
import unidecode
import uuid
from django.utils.html import mark_safe
import qrcode
from io import BytesIO
from django.core.files import File
import datetime


def upload_path(instance, filename):
    name = unidecode.unidecode(instance.name).replace(" ", "-").lower()
    return 'qr_code_img/{0}'.format(name)

# Create your models here.
class Student(models.Model):
    email = models.EmailField(default = '')
    student_code = models.CharField(max_length=8, unique = True)
    full_name = models.CharField(max_length = 50)

    def __str__(self):
        return self.full_name

class ItemCategory(models.Model):
    category_name = models.CharField(max_length = 50)

    def __str__(self) -> str:
        return self.category_name

class Item(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete = models.CASCADE, default = None, blank = True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_name = models.CharField(max_length = 50)
    qr_code_img = models.FileField(upload_to='qr_code_img/', blank=True, null= True)
    status = models.CharField(max_length = 20, default = 'ready')
    

    def __str__(self) -> str:
        return self.item_name
    
    #Tao va luu anh QR code vao model
    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.id)
        file_name = f'{self.id}.png'
        stream = BytesIO()
        qr_image.save(stream, 'PNG')
        self.qr_code_img.save(file_name, File(stream), save=False)
        super(Item, self).save(*args, **kwargs)


class Subject(models.Model):
    subject_name = models.CharField(max_length = 50, null = False)
    students = models.ManyToManyField(Student, blank=True, symmetrical=False, related_name="student_list")
    items = models.ManyToManyField(ItemCategory, blank=True, symmetrical=False)

    def __str__(self):
        return self.subject_name

class SubjectClass(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f'{self.date} {self.subject.subject_name} {self.start_time}-{self.end_time}'
    
    


class ItemBorrow(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    date = models.DateField(auto_now_add = True)
    borrow_time = models.TimeField(auto_now_add = True)
    return_time = models.TimeField()
    status = models.CharField(max_length = 20, default = 'borrowed')

    def __str__(self) -> str:
        return f'{self.student.student_code} {self.item.item_name} {self.date} {self.borrow_time}-{self.return_time} {self.status}'





