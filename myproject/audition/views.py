from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import UserCreateForm
from .models import Vote, Band

User = get_user_model()

class Top(generic.TemplateView):
    template_name = 'top.html'

class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class VoteView(LoginRequiredMixin, generic.View):

    def no_vote(self,seq):
        for i , ans in enumerate(seq):
            if str(f'{i+1}バンド目') == str(ans):
                return True
        return False
    
    def has_duplicate(self,seq):
        return len(seq) != len(set(seq))
    
    def get(self, *args, **kwargs):
        vote = Vote.objects.latest('date_joined')
        first_grade_band = Band.objects.filter(is_first_grade_band = True)
        all_band = Band.objects.all()
        first_grade_band_num = [i for i in range(1,vote.first_grade_band_num + 1)]
        band_num = [i for i in range(vote.first_grade_band_num + 1, vote.band_num + 1)]
        return render(self.request,'vote.html',{'first_grade_band_num':first_grade_band_num, 'band_num':band_num, 'first_grade_band':first_grade_band, 'all_band':all_band, })
        
    def post(self, *args, **kwargs):
        vote = Vote.objects.latest('date_joined')
        first_grade_band = Band.objects.filter(is_first_grade_band = True)
        all_band = Band.objects.all()
        first_grade_band_num = [i for i in range(1,vote.first_grade_band_num + 1)]
        band_num = [i for i in range(vote.first_grade_band_num + 1, vote.band_num + 1)]
        ans = []
        for i in range(vote.band_num):
            ans.append(self.request.POST[f'band{i+1}'])
        
        if self.has_duplicate(ans) == True:
            duplicate_error = "同じバンドに投票しています"
        else:
            duplicate_error = None
        
        if self.no_vote(ans) == True:
            no_vote_error = "無投票が存在しています"
        else:
            no_vote_error = None

        if (duplicate_error == None) and (no_vote_error == None):
            self.request.user.vote_finish = True
            self.request.user.vote_contents = ans
            self.request.user.save()
            return render(self.request,'vote_done.html')
        else:
            return render(self.request,'vote.html',{
                                                    'first_grade_band_num':first_grade_band_num,
                                                    'band_num':band_num,
                                                    'first_grade_band':first_grade_band, 
                                                    'all_band':all_band, 
                                                    'duplicate_error':duplicate_error, 
                                                    'no_vote_error':no_vote_error
                                                    })

class ProfileView(LoginRequiredMixin, generic.View):

    def get_band_name(self,seq):
        band_name = []
        for uuid in seq:
            band_name.append(Band.objects.get(uuid = uuid).name)
        return band_name

    def get(self, *args, **kwargs):
        vote_contents = self.request.user.vote_contents
        band_name = self.get_band_name(vote_contents)
        print(band_name)
        return render(self.request,'registration/profile.html',{'band_name':band_name})


class DeleteView(LoginRequiredMixin, generic.View):

    def get(self, *args, **kwargs):
        user = User.objects.get(user_id=self.request.user.user_id)
        user.is_active = False
        user.delete()
        auth_logout(self.request)
        return render(self.request,'registration/delete_complete.html')

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('audition:password_change_done')
    template_name = 'registration/password_change_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context


class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'registration/password_change_done.html'

