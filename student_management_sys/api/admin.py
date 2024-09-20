from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
admin.site.register(Student)
admin.site.register(SubjectClass)
admin.site.register(ItemCategory)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['id', 'item_name', 'image_tag', 'category', 'status']
    readonly_fields = ['id', 'image_tag']

    class Meta:
        model = Item
    
    def image_tag(self, obj):
        return format_html('<img src="{}" width="600" height="600"/>'.format(obj.qr_code_img.url))
    
@admin.register(ItemBorrow)
class ItemBorrowAdmin(admin.ModelAdmin):
    fields = ['id', 'get_student_code', 'get_item_name', 'date', 'borrow_time', 'return_time', 'status']
    list_display = ['id', 'get_student_code', 'get_item_name', 'date', 'status']
    readonly_fields = ['id', 'get_student_code', 'get_item_name', 'date', 'borrow_time', 'return_time']

    class Meta:
        model = ItemBorrow
    
    def get_student_code(self, obj):
        return obj.student.student_code
    
    def get_item_name(self, obj):
        return obj.item.item_name

# @admin.register(SubjectClass)
class SubjectClassInlineAdmin(admin.TabularInline):
    model = SubjectClass
    readonly_fields = ["start_time", "end_time", "date", "admin_link"]
    extra = 1
    show_change_link = True

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,  
                                              instance._meta.module_name),
                      args=(instance.id,))
        return format_html(u'<a href="{}">Edit</a>', url)
        # … or if you want to include other fields:
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)

class StudentInlineAdmin(admin.TabularInline):
    model = Subject.students.through
    extra = 1

class ItemInlineAdmin(admin.TabularInline):
    model = Subject.items.through
    extra = 1
    list_display = ["item_name"]

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [SubjectClassInlineAdmin, StudentInlineAdmin, ItemInlineAdmin]
    list_display = ["subject_name"]
    fields = ["id" , "subject_name"]
    readonly_fields = ["id"]