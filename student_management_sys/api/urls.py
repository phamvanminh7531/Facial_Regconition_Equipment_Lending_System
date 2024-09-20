from django.urls import path
from .views import student_borrow_by_student_code, return_item_by_id, ItemBorrowViewSet, index, item_borrow_list_fe
from .views import student_list, delete_student, add_student, item_list, add_item_category, delete_item_category
from .views import delete_item, add_item, subject_list, add_subject, delete_subject, subject_detail, delete_item_subject_detail
from .views import add_item_subject_detail, add_student_subject_detail, delete_student_subject_detail, add_class_subject_detail
from .views import delete_class_subject_detail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("post", ItemBorrowViewSet, basename="post")


urlpatterns = [
    path('student-borrow/<str:code>', student_borrow_by_student_code),
    path('item-return/<str:item_id>', return_item_by_id),
    path('', index),
    path('item-borrow-list/', item_borrow_list_fe, name="item-borrow-list"),
    path('student-list/', student_list, name="student-list"),
    path('delete-student/<str:pk>', delete_student, name="delete-student"),
    path('add-student/', add_student, name="add-student"),
    path('item-list/', item_list, name="item-list"),
    path('add-item-category/', add_item_category, name="add-item-category"),
    path('delete-item-category/<str:pk>', delete_item_category, name="delete-item-category"),
    path('delete-item/<str:pk>', delete_item, name="delete-item"),
    path('add-item/', add_item, name="add-item"),

    path('subject-list/', subject_list, name="subject-list"),
    path('delete-subject/<str:pk>', delete_subject, name="delete-subject"),
    path('add-subject/', add_subject, name="add-subject"),
    path('subject-detail/<str:pk>', subject_detail, name="subject-detail"),
    path('add-item-subject-detail/<str:subject_id>', add_item_subject_detail, name="add-item-subject-detail"),
    path('delete-item-subject-detail/<str:subject_id>/<str:item_category_id>/', delete_item_subject_detail, name="delete-item-subject-detail"),
    path('add-student-subject-detail/<str:subject_id>', add_student_subject_detail, name="add-student-subject-detail"),
    path('delete-student-subject-detail/<str:subject_id>/<str:student_id>/', delete_student_subject_detail, name="delete-student-subject-detail"),
    path('add-class-subject-detail/<str:subject_id>', add_class_subject_detail, name="add-class-subject-detail"),
    path('delete-class-subject-detail/<str:subject_class_id>', delete_class_subject_detail, name="delete-class-subject-detail"),
    
]

urlpatterns += router.urls