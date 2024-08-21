from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from .task import send_email

############## News, Comment Views ##############


class NewsListView(View):
    template_name = 'app/index.html'
    context_object_name = 'news'
    
    def get(self, request):
        context = {'news': News.objects.all(), 'categories': Category.objects.all()}
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.POST.get('filtering') or request.POST.get('cancel'):
            context = {'news': News.objects.all(), 'categories': Category.objects.all()}
            return render(request, self.template_name, context)
        else:
            try:
                category = Category.objects.get(pk=int(request.POST.get('filtering')))
                context={'news': News.objects.filter(category_id=category.pk), 'categories': Category.objects.all()}
                return render(request, self.template_name, context)
            except Category.DoesNotExist:
                context={'news': News.objects.all(), 'categories': Category.objects.all()}
                return render(request, self.template_name, context)
            

class NewsDetailView(UpdateView):
    model = News
    template_name = 'app/detail.html'
    context_object_name = 'news'
    form_class = CommentForm

    def form_valid(self, form):
        comment_text = form.cleaned_data['comment_text']
        Comment.objects.create(author = self.request.user, comment_text = comment_text, comment_to_news = self.get_object())
        return redirect(reverse_lazy('detail_news', kwargs={"pk": self.get_object().pk}))

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['comments_count'] = Comment.objects.filter(comment_to_news=self.get_object().pk).count()
        context['comments'] = Comment.objects.filter(comment_to_news=self.get_object().pk)
        return context
    
@method_decorator(login_required, name="dispatch")
class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'app/update_comm.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment'
    
    def get_success_url(self):
        return reverse('detail_news', kwargs={"pk": self.kwargs['pk']})
    
@method_decorator(login_required, name="dispatch")
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'app/del_comm.html'
    pk_url_kwarg = 'del_comment'

    def get_success_url(self):
        return reverse('detail_news', kwargs={"pk": self.kwargs['pk']})
    


# ========================================

############### User Views ###############

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'app/auth.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('main')
    success_message = "ДОБРО ПОЖАЛОВАТЬ"


class RegistrationView(CreateView):
    template_name = 'app/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        send_email.delay(user.pk)

        return redirect('account_sent')


class Account_activation_sent(TemplateView):
    template_name = 'app/account_sent.html'



class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account_complete')
        else:
            return HttpResponseBadRequest('ЧЁ ЗА ХУЙНЯ?!')
        
    
@method_decorator(login_required, name="dispatch")
class Account_activation_complete(TemplateView):
    template_name = 'app/account_complete.html'

@method_decorator(login_required, name="dispatch")
class UserDetailView(DetailView):
    model = User
    template_name = 'app/profile.html'
    context_object_name = 'profile'

@method_decorator(login_required, name="dispatch")
class UserLogoutView(TemplateView):
    template_name = 'app/logout.html'

@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    template_name = 'app/update.html'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('profile', kwargs={"pk": self.kwargs['pk']})

@method_decorator(login_required, name="dispatch")
class ImageUpdateView(UpdateView):
    model = User
    template_name = 'app/update_image.html'
    form_class = ChangePicture
    
    def get_success_url(self):
        return reverse('profile', kwargs={"pk": self.kwargs['pk']})
    
@method_decorator(login_required, name="dispatch")
class UserChangePassword(PasswordChangeView):
    form_class = UserChangePassword
    template_name = 'app/password_change.html'

    def get_success_url(self):
        return reverse('password_change_done', kwargs={"pk": self.kwargs['pk']})


@method_decorator(login_required, name="dispatch")
class UserChangePasswordDone(PasswordChangeDoneView):
    template_name = 'app/password_change_done.html'


# ========================================


# Create your views here.
