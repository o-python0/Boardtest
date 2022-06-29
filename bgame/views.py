from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView

from .models import Bgame
from django.contrib.auth.models import User

from .forms import CommentForm, WantPlayForm




#ウェルカムページ
class IndexView(TemplateView):
    template_name = 'bgame/welcome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["top_object"] = Bgame.objects.order_by('?')[0]
        context["bgame_list"] = Bgame.objects.order_by('-title')[:3]

        return context



# 一覧表示
class ListView(ListView):
    template_name = 'bgame/list.html'
    model = Bgame



# # 詳細表示
# class DetailView(DetailView):
#     template_name = 'bgame/detail.html'
#     model = Bgame

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         context['CommentForm'] = CommentForm(initial={'bgame': self.object})
#         wantplay_list = self.wantplay_text.split(",")
#         context['wantplay_list'] = wantplay_list
  
#         return context

# 詳細表示
def detailfunc(request, pk):
    object = Bgame.objects.get(pk=pk)
    wantplay_num = object.want_play.count()
    
    form = WantPlayForm()
    
    return render(request, 'bgame/detail.html', {"object": object, "want_play": wantplay_num ,"form": form})



# 作成機能
class CreateView(CreateView):
    template_name = 'bgame/create.html'
    model = Bgame
    fields = ('title', 'content', 'descrption', 'weight', 'image')
    success_url = reverse_lazy("bgame:list")


# 更新機能
class UpdateView(UpdateView):
    template_name = 'bgame/update.html'
    model = Bgame
    fields = ('title', 'content', 'descrption', 'weight', 'image')
    success_url = reverse_lazy("bgame:list")

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        return reverse("bgame:detail", kwargs={"pk": pk})


# 削除機能
class DeleteView(DeleteView):
    template_name = 'bgame/delete.html'
    model = Bgame
    success_url = reverse_lazy("bgame:list")


# サインアップ
def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username, '', password)
            return render(request, 'bgame/welcome.html')
        except IntegrityError:
            return render(request, 'bgame/signup.html', {'error': 'このアカウント名は既に使用されています。'})
    
    return render(request, 'bgame/signup.html')


# ログイン
def loginfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('bgame:list')
        else:
            return render(request, 'bgame/welcome.html', {'message': 'ログインできませんでした'})

    return render(request, 'bgame/welcome.html')


# ログアウト
def logoutfunc(request):
    logout(request)
    return redirect('bgame:welcome')



# コメント作成
def comment_create(request):
    bgame = request.POST.get("bgame")
    content = request.POST.get("content")
    user = request.user

    data = {"bgame": bgame, "content": content, "user": user}

    form = CommentForm(data=data)
    if form.is_valid():
        form.save()

    return redirect("bgame:detail", pk=bgame)



# 遊んでみたい機能
def wantplayfunc(request, pk):
    bgame = Bgame.objects.get(pk=pk)
    user = request.user
    data = {"bgame": bgame, "user": user}

    print("マッチング数:" + str(bgame.want_play.count()))

    form = WantPlayForm(data=data)
    if form.is_valid():
        form.save()


    if bgame.min_play == bgame.want_play.count():
        print("マッチング")
   
    return redirect("bgame:detail", pk=pk)



# 興味あり機能
def interestfunc(request, pk):
    object = Bgame.objects.get(pk=pk)
    object.interest += 1
    object.save()
    return redirect("bgame:detail", pk=pk)