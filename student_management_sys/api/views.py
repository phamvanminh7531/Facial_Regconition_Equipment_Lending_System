from django.shortcuts import render, redirect
import datetime
from .models import SubjectClass, Subject, ItemBorrow, Student, Item, ItemCategory
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ItemBorrowSerializer

# Create your views here.

def get_curr_subject_class():
    today = datetime.date.today()
    current_time = datetime.datetime.now()
    today_sub_class_list = SubjectClass.objects.filter(
        date = today,
        start_time__lte = current_time,
        end_time__gte = current_time
        )
    if len(today_sub_class_list)>0:
        return today_sub_class_list, today_sub_class_list[0].end_time
    else:
        return None, None

def get_subject_student_in(student_code):
    curr_subject_class_list, end_time = get_curr_subject_class()
    
    if curr_subject_class_list:
        subject = Subject.objects.filter(
            students__student_code  = student_code,
            subjectclass__in = curr_subject_class_list
        )

        if len(subject) > 0:
            return subject[0], end_time
        else:
            return None, None
    else:
            return None, None


@api_view(['GET'])
def student_borrow_by_student_code(request, code):
    subject, end_time = get_subject_student_in(code)

    if subject:
        student = Student.objects.get(student_code = code)
        item_category_list = subject.items.all()
        
        for category in item_category_list:
            item = Item.objects.filter(
                category = category,
                status = 'ready'
            )

            if (len(item)>0):
                item[0].status = 'not ready'
                item[0].save()
                ItemBorrow.objects.create(
                student = student,
                item = item[0],
                return_time = end_time
                )
            else:
                return Response({
                        'result': 'Device Not Ready For All'
                    })        
        else:
            return Response({
                'result': 'Authoreize'
            })
    else:
        return Response({
            'result': 'Access Denied 0'
        })


@api_view(['GET'])
def return_item_by_id(request, item_id):
    try:
        item = Item.objects.get(id = item_id)
        item.status = 'ready'
        item.save()

        item_borrow = ItemBorrow.objects.get(
            item_id = item_id,
            status = 'borrowed'
        )
        item_borrow.status = 'returned'
        item_borrow.save()

        return Response({
            'result': 'Returned Item'
        })
    except:
        return Response({
            'result': 'Item Already Returned'
        })

class ItemBorrowViewSet(viewsets.ModelViewSet):
    queryset = ItemBorrow.objects.all()
    serializer_class = ItemBorrowSerializer()

def index(request):
    return redirect("item-borrow-list")

def item_borrow_list_fe(request):
    return render(request, "api/item-borrow-list.html")

def student_list(request):
    student_list = Student.objects.all()
    context = {
        "student_list" : student_list
    }
    return render(request, "api/student-list.html", context=context)

def delete_student(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        email = request.POST.get("email")
        Student(full_name = name, student_code = code, email = email).save()
        return redirect("student-list")

def item_list(request):
    item_category_list = ItemCategory.objects.all()
    item_list = Item.objects.all()
    context = {
        "item_category_list" : item_category_list,
        "item_list" : item_list,
    }
    return render(request, "api/item-list.html", context=context)

def add_item_category(request):
    if request.method == "POST":
        category_name = request.POST.get("category-name")
        ItemCategory(category_name = category_name).save()
        return redirect("item-list")

def delete_item_category(request, pk):
    item_category = ItemCategory.objects.get(id=pk)
    item_category.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def delete_item(request, pk):
    item = Item.objects.get(id=pk)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        type = request.POST.get("type")
        item_category = ItemCategory.objects.get(id=type)
        Item(item_name = name, category = item_category).save()
        return redirect("item-list") 

def subject_list(request):
    subject_list = Subject.objects.all()
    context = {
        "subject_list" : subject_list
    }

    return render(request, "api/subject-list.html", context=context)

def add_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject-name")
        Subject(subject_name = subject_name).save()
        return redirect("subject-list") 

def delete_subject(request, pk):
    subject = Subject.objects.get(id=pk)
    subject.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def subject_detail(request, pk):
    subject = Subject.objects.get(id = pk)
    subject_item_list = subject.items.all()
    subject_student_list = subject.students.all()

    subject_class_list = SubjectClass.objects.filter(subject = subject)

    item_option_input_list = ItemCategory.objects.all()

    student_list = Student.objects.all()

    student_option_input_list = [stu for stu in student_list if stu not in subject_student_list]

    context = {
        "subject":subject,
        "subject_item_list" : subject_item_list,
        "subject_student_list" : subject_student_list,
        "subject_class_list" : subject_class_list,
        "item_option_input_list" : item_option_input_list,
        "student_option_input_list" : student_option_input_list,
    }

    return render(request, "api/subject-detail.html", context=context)

def add_item_subject_detail(request, subject_id):
    if request.method == "POST":
        item_category = ItemCategory.objects.get(id = request.POST.get("item-category-id"))
        subject = Subject.objects.get(id = subject_id)

        subject.items.add(item_category)
        return redirect(request.META.get('HTTP_REFERER'))

def delete_item_subject_detail(request, subject_id, item_category_id):
    subject = Subject.objects.get(id = subject_id)
    item_category = ItemCategory.objects.get(id = item_category_id)
    subject.items.remove(item_category)
    return redirect(request.META.get('HTTP_REFERER'))

def add_student_subject_detail(request, subject_id):
    if request.method == "POST":
        student = Student.objects.get(id = request.POST.get("student-id"))
        subject = Subject.objects.get(id = subject_id)

        subject.students.add(student)
        return redirect(request.META.get('HTTP_REFERER'))

def delete_student_subject_detail(request, subject_id, student_id):
    subject = Subject.objects.get(id = subject_id)
    student = Student.objects.get(id = student_id)
    subject.students.remove(student)
    return redirect(request.META.get('HTTP_REFERER'))

def add_class_subject_detail(request, subject_id):
    if request.method == "POST":
        subject = Subject.objects.get(id = subject_id)
        date = request.POST.get("date")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")
        SubjectClass(subject = subject, date = date, start_time = start_time, end_time = end_time).save()
        return redirect(request.META.get('HTTP_REFERER'))

def delete_class_subject_detail(request, subject_class_id):
    subject_class = SubjectClass.objects.get(id = subject_class_id)
    subject_class.delete()
    return redirect(request.META.get('HTTP_REFERER'))