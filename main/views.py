from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Subject, Note, Notice, ClassResult, TeacherMessage, BCAPaper, Topper
from collections import defaultdict

@login_required(login_url='login')
def notes_dashboard(request):
    subjects_by_sem = {}
    for sem in range(1, 7):
        subjects = Subject.objects.filter(semester=sem)
        subjects_by_sem[sem] = subjects
    return render(request, 'notes_dashboard.html', {'subjects_by_sem': subjects_by_sem})

def subject_notes(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    notes = Note.objects.filter(subject=subject).first()
    return render(request, 'subject_notes.html', {'subject': subject, 'notes': notes})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def courses(request):
    return render(request, 'courses.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def test(request):
    return render(request, 'test.html')    
    
def events(request):
    return render(request, 'events.html')  

@login_required(login_url='login')
def bca_papers(request):
    papers = BCAPaper.objects.all()

    semester = request.GET.get('semester')
    year = request.GET.get('year')
    search = request.GET.get('search')

    if semester:
        papers = papers.filter(semester=semester)

    if year:
        papers = papers.filter(year=year)

    if search:
        papers = papers.filter(subject_name__icontains=search)

    papers = papers.order_by('semester', '-year')

    data = defaultdict(list)
    for paper in papers:
        data[paper.semester].append(paper)

    # For dropdowns
    semesters = BCAPaper.objects.values_list('semester', flat=True).distinct()
    years = BCAPaper.objects.values_list('year', flat=True).distinct()

    return render(request, 'bca_papers.html', {
        'data': dict(data),
        'semesters': semesters,
        'years': years,
    })    

@login_required(login_url='login')
def notice_page(request):
    notices = Notice.objects.all().order_by('-date')
    return render(request, 'notice.html', {'notices': notices}) 


@login_required(login_url='login')
def results_page(request):
    classes = ['1st Year', '2nd Year', '3rd Year']
    data = {}

    for cls in classes:
        students = Topper.objects.filter(class_name=cls).order_by('-percentage')

        ranked_students = []
        prev_percentage = None
        rank = 0

        for student in students:
            if student.percentage != prev_percentage:
                rank += 1   # ✅ increment only when new percentage
            prev_percentage = student.percentage

            ranked_students.append({
                'student': student,
                'rank': rank
            })

        full_result = ClassResult.objects.filter(class_name=cls).first()

        data[cls] = {
            'toppers': ranked_students[:5],
            'result_image': full_result
        }

    return render(request, 'results.html', {'data': data})

# def results_page(request):
#     classes = ['1st Year', '2nd Year', '3rd Year']
#     data = {}

#     for cls in classes:
#         toppers = Result.objects.filter(class_name=cls, is_topper=True)[:3]
#         image = Result.objects.filter(class_name=cls).first()
#         data[cls] = {
#             'toppers': toppers,
#             'image': image
#         }

#     return render(request, 'results.html', {'data': data})



@login_required(login_url='login')
def teacher_messages(request):
    messages = TeacherMessage.objects.all()
    return render(request, 'teacher_messages.html', {'messages': messages})
