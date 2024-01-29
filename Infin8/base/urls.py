from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginPage, name="login"), 
    path('logout/', views.logoutUser, name="logout"), 
    path('register/', views.registerPage, name="register"),
    path('',views.participant_home,name="participant_home"),
    # path('verify/<token>/<email>/<username>/<phone_number>/<path: password>',views.verify,name="verify"),
    # path('verify/<token>/<email>/<username>/<path:password>/<int:phone_number>',views.verify,name="verify"),
    path('verify/<token>/<email>',views.verify,name="verify"),

    path('playGame/',views.playGame,name="playGame"),
    path('playGame/<str:game_link>/', views.confirmGame, name="confirmGame"),
    path('playGame/<str:game_link>/game', views.Game, name="Game"),
    path('playGame/<str:game_link>/status', views.GameStatus, name="statusGame"),
    path('dummy', views.dummy, name = "dummy"),
    path('playGame/<str:game_link>/dummy', views.dummygame, name = 'dummygame'),
    
    
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
]