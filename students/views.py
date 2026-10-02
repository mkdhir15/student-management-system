from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import Student
from .forms import StudentForm


def student_list(request):

    search = request.GET.get("search", "")
    course = request.GET.get("course", "")

    students = Student.objects.all()

    # Search
    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search)
        )

    # Filter
    if course:
        students = students.filter(course=course)

    courses = Student.objects.values_list(
        "course",
        flat=True
    ).distinct()

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "courses": courses,
            "search": search,
            "selected_course": course,
        }
    )


def student_add(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Add Student"
        }
    )


def student_edit(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Edit Student"
        }
    )


def student_delete(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(
        request,
        "students/student_delete.html",
        {
            "student": student
        }
    )