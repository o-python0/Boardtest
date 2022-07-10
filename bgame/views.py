from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView

from .models import Bgame, WantPlay
from django.contrib.auth.models import User

from .forms import CommentForm, InterestForm, WantPlayForm




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


    def get_queryset(self):
        qs = Bgame.objects.all()
        keyword = self.request.GET.get("q")

        if keyword:
            qs = qs.filter(title__contains=keyword)

        return qs



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
    
    Wform = WantPlayForm() #遊びたいフォーム
    Iform = InterestForm() #興味ありフォーム
    Cform = CommentForm() #コメントフォーム
    
    return render(request, 'bgame/detail.html', {"object": object, "Wform": Wform, "Iform": Iform, "Cform": Cform})



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

    def form_valid(self, form):
        messages.success(self.request, "更新しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新できませんでした")
        return super().form_invalid(form)



# 削除機能
class DeleteView(DeleteView):
    template_name = 'bgame/delete.html'
    model = Bgame
    success_url = reverse_lazy("bgame:list")

    def form_valid(self, form):
        messages.success(self.request, "削除しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "削除できませんでした")
        return super().form_invalid(form)


# サインアップ
def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            User.objects.create_user(username, '', password)
            messages.success(request, "アカウントが正常に作成されました。")
            return redirect('bgame:welcome')
        except IntegrityError:
            messages.error(request, "このアカウント名は既に使用されています。")
            return render(request, 'bgame/signup.html')
    
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
            messages.error(request, "ログインできませんでした。ユーザー名かパスワードが間違っている可能性があります。")
            return redirect('bgame:welcome')


    return render(request, 'bgame/welcome.html')


# ログアウト
def logoutfunc(request):
    logout(request)
    return redirect('bgame:welcome')



# コメント作成
def comment_create(request, pk):
    bgame = Bgame.objects.get(pk=pk)
    content = request.POST.get("content")
    user = request.user

    print(bgame)

    data = {"bgame": bgame, "content": content, "user": user}

    form = CommentForm(data=data)
    if form.is_valid():
        form.save()

    return redirect("bgame:detail", pk=pk)



# 遊んでみたい機能
def wantplayfunc(request, pk):
    bgame = Bgame.objects.get(pk=pk)
    user = request.user


    if bgame.wantplay_bgame.filter(is_match=True, user=user):
        try:
            WantPlay.objects.create(bgame=bgame, user=user)
            messages.success(request, "このゲームにマッチング希望をしました。")
        except IntegrityError:
            pass
    else:
        messages.error(request, "既にマッチング希望をしています。")


    # マッチング処理
    match_list = bgame.wantplay_bgame.filter(is_match=False)
    print(match_list)
    # if bgame.min_play == match_list.count():
    #     print("マッチング")
    #     for target in match_list:
    #         print("メール送信：" + str(target.user.email))
    #         target.is_match = True
    #         target.save()

    return redirect("bgame:detail", pk=pk)



# 興味あり機能
def interestfunc(request, pk):
    bgame = Bgame.objects.get(pk=pk)
    
    print(bgame)

    return redirect("bgame:detail", pk=pk)