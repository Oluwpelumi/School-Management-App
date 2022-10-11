from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404
from .forms import LearnerSignUpForm, InstructorSignUpForm, LearnerInterestsForm, LearnerCourse, UserForm, ProfileForm, PostForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import auth
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage

# Create your views here.


def home(request):
    return render (request, 'home.html')

def about(request):
    return render (request, 'about.html')

def contact(request):
    return render (request, 'contact.html')

def service(request):
    return render (request, 'service.html')

def register(request):
    return render (request, 'register.html')

def LogoutView(request):
    logout(request)
    return redirect('home')



def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,  username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_instructor:
                return redirect('instructor')
            elif user.is_learner:
                return redirect('learner')
            else:
                return redirect('login')
        else:
            messages.info(request, "Invalid Username and Password")
            return redirect('login')
    else:
        return render(request, 'login.html')



#Admin Views

def dashboard(request):
    learner = User.objects.filter(is_learner = True).count()
    instructor = User.objects.filter(is_instructor = True).count()
    course = Course.objects.all().count()
    users = User.objects.all().count()
    context = {'learner':learner, 'instructor':instructor, 'course':course, 'users':users}
    return render(request, 'dashboard/admin/home.html', context)


class InstructorSignUpView(CreateView):
    model = User
    form_class = InstructorSignUpForm
    template_name = 'dashboard/admin/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'instructor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'New Instructor Was Added Successfully')
        return redirect('isign')



class AdminLearner(CreateView):
    model = User
    form_class = LearnerSignUpForm
    template_name = 'dashboard/admin/learner_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'learner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'New Leraner Was Added Successfully')
        return redirect('addlearner')



def course(request):
    if request.method == 'POST':
        name = request.POST['name']
        color = request.POST['color']

        a = Course.objects.create(name=name, color=color)
        a.save()
        messages.success(request, 'A New course was registred successfully')
        return redirect('course')
    else:
        return render(request, 'dashboard/admin/course.html')



class AdminCreatePost(CreateView):
    model = Announcement
    form_class = PostForm
    template_name = 'dashboard/admin/post_form.html'
    success_url = reverse_lazy('alpost')

    # def get_initial(self, *args, **kwargs):
    #     initial = super().get_initial(**kwargs)
    #     initial['content'] = 'Announcement!!!'
    #     return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)




class AdminListPost(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/admin/tise_list.html' 

    def get_queryset(self):
        return Announcement.objects.order_by('-posted_at')



class AdminListAllPost(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/admin/list_tises.html'
    context_object_name = 'tises'
    paginate_by = 10


    def get_queryset(self):
        return Announcement.objects.order_by('-id')



class AdminDeletePost(SuccessMessageMixin, DeleteView):
    model = Announcement
    template_name  = 'dashboard/admin/confirm_delete.html'
    success_url = reverse_lazy('alistallpost')
    success_message = 'Announcement Was Successfully Deleted'



class AdminListAllUser(LoginRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/admin/list_users.html'
    context_object_name = 'users'
    paginate_by = 10
    # queryset = User.objects.all()[:3]

    def get_queryset(self):
        return User.objects.order_by('-id')


class AdminDeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name  = 'dashboard/admin/confirm_delete2.html'
    success_url = reverse_lazy('aluser')
    success_message = 'User Was Successfully Deleted'


def create_user_form(request):
    return render(request, 'dashboard/admin/add_user.html')


def create_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        a = User.objects.create(first_name = first_name, last_name = last_name, email = email, username = username, password = password, is_admin = True)
        a.save()
        messages.success(request, 'Admin User was created Successfully')
        return redirect('aluser')
    else:
        messages.error(request, 'Admin User was not created Successfully')
        return redirect('create_user_form')

    
def acreate_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        bio = request.POST['bio']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        birth_date = request.POST['birth_date']
        hobby = request.POST['hobby']
        avatar = request.FILES['avatar']
        favorite_animal = request.POST['favorite_animal']

        current_user = request.user
        user_id = current_user.id
        

        a = Profile.objects.filter(id = user_id).create(user_id=user_id, first_name = first_name, last_name = last_name, email = email, 
        favorite_animal = favorite_animal, phonenumber = phonenumber, bio = bio, city = city, state = state, 
        country = country, birth_date = birth_date, hobby = hobby, avatar = avatar)
        a.save()
        messages.success(request, 'Your Profile was created Successfully')
        return redirect('auser_profile')
    else:
        current_user = request.user
        user_id = current_user.id
        users = Profile.objects.filter(user_id = user_id)
        return render(request, 'dashboard/admin/create_profile.html', {'users':users})

    

def auser_profile(request):
    current_user = request.user
    user_id = current_user.id
    users = Profile.objects.filter(user_id = user_id)
    return render(request, 'dashboard/admin/user_profile.html', {'users':users})




#Instructor Views

def home_instructor(request):
    learner = User.objects.filter(is_learner = True).count()
    instructor = User.objects.filter(is_instructor = True).count()
    course = Course.objects.all().count()
    users = User.objects.all().count()
    context = {'learner':learner, 'instructor':instructor, 'course':course, 'users':users}
    return render(request, 'dashboard/instructor/home.html', context)



# class QuizCreateView(CreateView):
#     model = Quiz
#     fields = ('name', 'course')
#     template_name = 'dashboard/instructor/quiz_add_form.html'

#     def form_valid(self, form):
#         quiz = form.save(commit=False)
#         quiz.owner = self.request.user
#         quiz.save()
#         messages.success(self.request, 'Quiz Created Successfully; Go A Head And Add Questions')
#         return redirect('quiz_change_list')


# class QuizUpdateView(UpdateView):
#     model = Quiz
#     fields = ('name', 'course')
#     template_name = 'dashboard/instructor/quiz_change_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['questions'] = self.get_object().questions.annotate(answers_count = Count('answers'))
#         return super().get_context_data(**kwargs)

#     def get_queryset(self):
#         return self.request.user.quizzes.all()

#     def get_success_url(self):
#         return reverse('quiz_change', kwargs = {'pk':self.request.pk})



# def question_add(request, pk):
#     quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)
    
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.quiz = quiz
#             question.save()
#             messages.success(request, 'You may now add answers/options to the question.')
#             return redirect('question_change', quiz.pk, question.pk)
#     else:
#         form = QuestionForm()

#     return render(request, 'dashboard/instructor/question_add_form.html', {'quiz': quiz, 'form': form})




# def question_change(request, quiz_pk, question_pk):
#     quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
#     question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

#     AnswerFormatSet = inlineformset_factory (
#         Question,
#         Answer,
#         formset = BaseAnswerInlineFormSet,
#         fields = ('text', 'is_correct'),
#         min_num = 2,
#         validate_min = True,
#         max_num = 10,
#         validate_max = True
#         )

#     if request.method == 'POST':
#         form = QuestionForm(request.POST, instance=question)
#         formset = AnswerFormatSet(request.POST, instance=question)
#         if form.is_valid() and formset.is_valid():
#             with transaction.atomic():
#                 formset.save()
#                 formset.save()
#             messages.success(request, 'Question And Answers Saved Successfully')
#             return redirect('quiz_change', quiz.pk)
#     else:
#         form = QuestionForm(instance=question)
#         formset = AnswerFormatSet(instance=question)
#     return render(request, 'dashboard/instructor/question_change_form.html', {
#         'quiz':quiz,
#         'question':question,
#         'form':form,
#         'formset':formset
#         })  



# class QuestionDeleteView(DeleteView):
#     model = Question
#     context_object_name = 'question'
#     template_name = 'dashboard/instructor/question_delete_confirm.html'
#     pk_url_kwarg = 'question_pk'

#     def get_context_data(self, **kwargs):
#         question = self.get_object()
#         kwargs['quiz'] = question.quiz
#         return super().get_context_data(**kwargs)


#     def delete(self, request, *args, **kwargs):
#         question = self.get_object()
#         messages.success(request, 'The Question Was Deleted Successfully')
#         return super().delete(request, *args, **kwargs)


#     def get_queryset(self):
#         return Question.objects.filter(quiz__owner=self.request.user)



# class QuizListView(ListView):
#     model = Quiz
#     ordering = ('name', )
#     context_object_name = 'quizzes'
#     template_name = 'dashboard/instructor/quiz_change_list.html'

#     def get_queryset(self):
#         queryset = self.request.user.quizzes \
#         .select_related('course') \
#         .annotate(questions_count = Count('questions', distinct=True)) \
#         .annotate(taken_count = Count('taken_quizzes', distinct=True))
#         return queryset    



# class QuizResultsView(DeleteView):
#     model = Quiz
#     context_object_name = 'quiz'
#     template_name = 'dashboard/instructor/quiz_results.html'


#     def get_context_data(self, **kwargs):
#         quiz = self.get_object()
#         taken_quizzes =quiz.taken_quizzes.select_related('learner__user').order_by('-date')
#         total_taken_quizzes = taken_quizzes.count()
#         quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
#         extra_context = {
#         'taken_quizzes': taken_quizzes,
#         'total_taken_quizzes': total_taken_quizzes,
#         'quiz_score':quiz_score
#         }

#         kwargs.update(extra_context)
#         return super().get_context_data(**kwargs)


#     def get_queryset(self):
#         return self.request.user.quizzes.all()    



# class QuizDeleteView(DeleteView):
#     model = Quiz
#     context_object_name = 'quiz'
#     template_name = 'dashboard/instructor/quiz_delete_confirm.html'
#     success_url = reverse_lazy('quiz_change_list')

#     def delete(self, request, *args, **kwargs):
#         quiz = self.get_object()
#         messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
#         return super().delete(request, *args, **kwargs)

#     def get_queryset(self):
#         return self.request.user.quizzes.all()



def tutorial(request):
    courses = Course.objects.only('id','name')
    context = {'courses':courses}
    return render(request, 'dashboard/instructor/tutorial.html' , context)


def publish_tutorial(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        thumb = request.FILES['thumb']
        course_id = request.POST['course_id']
        current_user = request.user
        author_id = current_user.id
        print(author_id)
        print(current_user)

        a = Tutorial.objects.create(user_id=author_id, title=title, content=content, thumb=thumb, course_id=course_id)
        a.save()
        messages.success(request, 'Tutorial Was Published Successfully!')
        return redirect('tutorial')
    else:
        messages.error(request, 'Tutorial Was Not Published Successfully!')
        return redirect('tutorial')


def itutorial(request):
    tutorials = Tutorial.objects.all().order_by('-created_at')
    tutorials = {'tutorials':tutorials}
    return render(request, 'dashboard/instructor/list_tutorial.html', tutorials)



class ITutorialDetail(LoginRequiredMixin, DetailView):
    model = Tutorial
    template_name = 'dashboard/instructor/tutorial_detail.html'



class LNotesList(ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = "dashboard/instructor/list_notes.html"
    paginate_by = 4


def iadd_notes(request):
    courses = Course.objects.only('id','name')
    context = {'courses':courses}
    return render(request, 'dashboard/instructor/add_notes.html' , context)


def publish_notes(request):
    if request.method == 'POST':
        title = request.POST['title']
        file = request.FILES['file']
        cover = request.FILES['cover']
        course_id = request.POST['course_id']
        current_user = request.user
        user_id = current_user.id
        print(user_id)
        print(current_user)

        a = Notes.objects.create(user_id=user_id, title=title, file=file, cover=cover, course_id=course_id)
        a.save()
        messages.success(request, 'Notes Was Published Successfully!')
        return redirect('lnotes')
    else:
        messages.error(request, 'Notes Was Not Published Successfully!')
        return redirect('iadd_notes')


def update_file(request, pk):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = file.name

        fs = FileSystemStorage()
        file = fs.save(file_name, file)
        # fileurl = fs.url(file)

        Notes.objects.filter(id=pk).update(file = file)
        messages.success(request, 'Notes Was Updated Succesfully')
        return redirect('lnotes')
    else:
        return render(request, 'dashboard/instructor/update.html')



class CreatePost(CreateView):   
    model = Announcement
    form_class = PostForm
    template_name = 'dashboard/instructor/post_form.html'
    success_url = reverse_lazy('ilchat')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class InstructorListPost(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'dashboard/instructor/tise_list.html'

    def get_queryset(self):
        return Announcement.objects.all().order_by('-posted_at')



def icreate_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        bio = request.POST['bio']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        birth_date = request.POST['birth_date']
        hobby = request.POST['hobby']
        avatar = request.FILES['avatar']
        favorite_animal = request.POST['favorite_animal']

        current_user = request.user
        user_id = current_user.id
        

        a = Profile.objects.filter(id = user_id).create(user_id=user_id, first_name = first_name, last_name = last_name, email = email, 
        favorite_animal = favorite_animal, phonenumber = phonenumber, bio = bio, city = city, state = state, 
        country = country, birth_date = birth_date, hobby = hobby, avatar = avatar)
        a.save()
        messages.success(request, 'Your Profile was created Successfully')
        return redirect('user_profile')
    else:
        current_user = request.user
        user_id = current_user.id
        users = Profile.objects.filter(user_id = user_id)
        return render(request, 'dashboard/instructor/create_profile.html', {'users':users})

 

def iuser_profile(request):
    current_user = request.user
    user_id = current_user.id
    users = Profile.objects.filter(user_id = user_id)
    return render(request, 'dashboard/instructor/user_profile.html', {'users':users})




# Learner Views
class LearnerSignUpView(CreateView):
    model = User
    form_class = LearnerSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'learner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def learner(request):
    course = Course.objects.all().count()
    learner = User.objects.all().filter(is_learner = True).count()
    instructor = User.objects.all().filter(is_instructor = True).count()
    users = User.objects.all().count()
    context = {'course':course, 'learner':learner, 'instructor':instructor, 'users':users}
    return render(request, 'dashboard/learner/home.html', context)


def ltutorial(request):
    tutorials = Tutorial.objects.all().order_by('-created_at')
    context = {'tutorials':tutorials}
    return render(request, 'dashboard/learner/list_tutorial.html' , context)

class LTutorialDetail(LoginRequiredMixin, DetailView):
    model = Tutorial
    template_name = 'dashboard/learner/tutorial_detail.html'


class LearnerInterestsView(UpdateView):
    model = Learner
    form_class = LearnerInterestsForm
    template_name = 'dashboard/learner/interests_form.html'
    success_url = reverse_lazy('interests')

    def get_object(self):
        return self.request.user.learner

    def form_valid(self, form):
        messages.success(self.request, 'Course Was Successfully Updated!')
        return super().form_valid(form)

    
class LLNotesView(ListView):
    model = Notes
    template_name = 'dashboard/learner/list_notes.html'
    context_object_name = 'notes'
    paginate_by = 4

    def get_queryset(self):
        return Notes.objects.all().order_by('-id')


class LLPostView(ListView):
    model = Announcement
    template_name = 'dashboard/learner/tise_list.html'

    def get_queryset(self):
        return Announcement.objects.all().order_by('-posted_at')


def lcreate_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        bio = request.POST['bio']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        birth_date = request.POST['birth_date']
        hobby = request.POST['hobby']
        avatar = request.FILES['avatar']
        favorite_animal = request.POST['favorite_animal']

        current_user = request.user
        user_id = current_user.id
        

        a = Profile.objects.filter(id = user_id).create(user_id=user_id, first_name = first_name, last_name = last_name, email = email, 
        favorite_animal = favorite_animal, phonenumber = phonenumber, bio = bio, city = city, state = state, 
        country = country, birth_date = birth_date, hobby = hobby, avatar = avatar)
        a.save()
        messages.success(request, 'Your Profile was created Successfully')
        return redirect('user_profile')
    else:
        current_user = request.user
        user_id = current_user.id
        users = Profile.objects.filter(user_id = user_id)
        return render(request, 'dashboard/learner/create_profile.html', {'users':users})

 

def luser_profile(request):
    current_user = request.user
    user_id = current_user.id
    users = Profile.objects.filter(user_id = user_id)
    return render(request, 'dashboard/learner/user_profile.html', {'users':users})



def listC(request):
    courses = Course.objects.all()
    return render(request, 'dashboard/admin/listC.html', {'courses':courses})

def listLL(request):
    learners = User.objects.all().filter(is_learner = True)
    return render(request, 'dashboard/admin/listLL.html', {'learners':learners})

def listII(request):
    Instructors = User.objects.all().filter(is_instructor = True)
    return render(request, 'dashboard/admin/listII.html', {'Instructors':Instructors})