from django.urls import path
from . import views


urlpatterns = [

    #Shared URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('service/', views.service, name='service'),
    # path('login_form/', views.login_form, name='login_form'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    

    #Admin URLs
    path('isign/', views.InstructorSignUpView.as_view(), name='isign'),
    path('addlearner/', views.AdminLearner.as_view(), name='addlearner'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('listC/', views.listC, name='listcourse'),
    path('listLL/', views.listLL, name='listlearner'),
    path('listII/', views.listII, name='listinstructor'),

    path('course/', views.course, name='course'),

    path('apost/', views.AdminCreatePost.as_view(), name='apost'),
    path('alpost/', views.AdminListPost.as_view(), name='alpost'),
    path('alistallpost/', views.AdminListAllPost.as_view(), name='alistallpost'),  
    path('adpost/<int:pk>/', views.AdminDeletePost.as_view(), name='adpost'),  

    path('aluser/', views.AdminListAllUser.as_view(), name='aluser'),
    path('aduser/<int:pk>/', views.AdminDeleteUser.as_view(), name='aduser'),

    path('create_user_form/', views.create_user_form, name='create_user_form'),
    path('create_user/', views.create_user, name='create_user'),
    
    path('acreate_profile/', views.acreate_profile, name='acreate_profile'),
    path('auser_profile/', views.auser_profile, name='auser_profile'),




    #Instructor Views
    path('instructor/', views.home_instructor, name ='instructor'),
    
    # path('quiz_add/', views.QuizCreateView.as_view(), name ='quiz_add'),
    # path('quiz_update/<int:pk>/', views.QuizUpdateView.as_view(), name ='quiz_change'),
    # path('question_add/<int:pk>/', views.question_add, name ='question_add'),
    # path('quiz/<int:quiz_pk>/<int:question_pk>/', views.question_change, name ='question_change'),
    # path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    # path('quiz_change_list/', views.QuizListView.as_view(), name='quiz_change_list'),
    # path('quiz/<int:pk>/results/', views.QuizResultsView.as_view(), name='quiz_results'),
    # path('quiz/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='quiz_delete'),

    path('tutorial/', views.tutorial, name='tutorial'),
    path('publish_tutorial/', views.publish_tutorial, name='publish_tutorial'),
    path('itutorial/', views.itutorial, name='itutorial'),
    path('itutorial/<int:pk>/', views.ITutorialDetail.as_view(), name='itutorial-detail'),

    path('listnotes/', views.LNotesList.as_view(), name='lnotes'),
    path('iadd_notes/', views.iadd_notes, name='iadd_notes'),
    path('publish_notes/', views.publish_notes, name='publish_notes'),
    path('update_file/<int:pk>/', views.update_file, name='update_file'),

    path('ipost/', views.CreatePost.as_view(), name='ipost'),
    path('ilchat', views.InstructorListPost.as_view(), name='ilchat'),

    path('create_profile/', views.icreate_profile, name='create_profile'),
    path('iuser_profile/', views.iuser_profile, name='iuser_profile'),



#Learners URLs
    path('lsign/', views.LearnerSignUpView.as_view(), name='lsign'),

    path('learner/', views.learner, name='learner'),

    path('ltutorial/', views.ltutorial, name='ltutorial'),
    path('tutorial_detail/<int:pk>/', views.LTutorialDetail.as_view(), name='tutorial_detail'),

    path('interests/', views.LearnerInterestsView.as_view(), name='interests'),

    path('llistnotes/', views.LLNotesView.as_view(), name='llistnotes'),
    path('llistposts/', views.LLPostView.as_view(), name='llistposts'),

    path('lcreate_profile/', views.lcreate_profile, name='lcreate_profile'),
    path('luser_profile/', views.luser_profile, name='luser_profile'),
    
]
