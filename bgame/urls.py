from django.urls import path

from .views import IndexView, ListView, CreateView, UpdateView, DeleteView, signupfunc, loginfunc, logoutfunc, comment_create, wantplayfunc, interestfunc, detailfunc

app_name = 'bgame'

urlpatterns = [
    path('', IndexView.as_view(), name='welcome'),
    path('list/', ListView.as_view(), name='list'),
    path('<int:pk>', detailfunc, name='detail'),
    path('create/', CreateView.as_view(), name='create'),
    path('update/<int:pk>', UpdateView.as_view(), name='update'),
    path('delete/<int:pk>', DeleteView.as_view(), name='delete'),
    path('wantplay/<int:pk>', wantplayfunc, name='wantplay'),
    path('interest/<int:pk>', interestfunc, name='interest'),

    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),

    #コメント作成
    path('comment/<int:pk>', comment_create, name='comment'),
]
