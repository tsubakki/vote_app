from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import UserCreateForm
from .models import Vote, Band
import random

User = get_user_model()

def VoteButtonCheck(user):
    vote = Vote.objects.latest('date_joined')
    if vote.is_active and user.suffrage:
        return True
    else:
        return False

def AdminResultButtonCheck():
    vote = Vote.objects.latest('date_joined')
    vote_user_count = User.objects.filter(suffrage=True).count()
    vote_finish_user_count = User.objects.filter(suffrage=True, vote_finish=True).count()
    announce = vote.announce
    is_active = vote.is_active
    if is_active == False and announce == False and vote_finish_user_count == vote_user_count:
        return True
    else:
        return False

def ResultButtonCheck():
    vote = Vote.objects.latest('date_joined')
    vote_user_count = User.objects.filter(suffrage=True).count()
    vote_finish_user_count = User.objects.filter(suffrage=True, vote_finish=True).count()
    announce = vote.announce
    is_active = vote.is_active
    result_ok = False
    if vote.pass_band != []:
        result_ok = True
    if result_ok and announce and is_active == False and vote_finish_user_count == vote_user_count:
        return True
    else:
        return False

class Top(generic.TemplateView):
    
    def get(self, *args, **kwargs):
        vote = Vote.objects.latest('date_joined')
        vote_user_count = User.objects.filter(suffrage=True).count()
        vote_finish_user_count = User.objects.filter(suffrage=True, vote_finish=True).count()
        vote_button_check = VoteButtonCheck(self.request.user)
        admin_result_button_check = AdminResultButtonCheck()
        result_button_check = ResultButtonCheck()
        return render(self.request,'top.html' ,{'vote':vote, 
                                                'vote_finish_user_count':vote_finish_user_count, 
                                                'vote_user_count':vote_user_count, 
                                                'vote_button_check':vote_button_check, 
                                                'admin_result_button_check':admin_result_button_check, 
                                                'result_button_check':result_button_check,
                                                })

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

        # 勝手に入らないようにリダイレクトの設定を追加する
        vote_button_check = VoteButtonCheck(self.request.user)
        if vote_button_check == False:
            return redirect('top')
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

class VoteAdminResultView(generic.TemplateView):

    def get_band_name_dict(self, all_band):
        band_name_dict = {}
        for band in all_band:
            band_name_dict[str(band.name)] = 0
        return band_name_dict

    def get_count(self, band_name_dict , all_user):
        for user in all_user:
            for uuid in user.vote_contents:
                band_name = Band.objects.get(uuid=uuid).name
                band_name_dict[band_name] += 1
        return band_name_dict
    
    def get_rank(self, seq):
        rank = 1
        tmp_rank = 1
        pre_count = seq[0][1]
        seq[0] += (rank,)
        for i in range(1,len(seq)):
            count = seq[i][1]
            if count == pre_count:
                tmp_rank += 1
            else:
                tmp_rank += 1
                rank = tmp_rank
            seq[i] += (rank,)
            pre_count = count
        return seq
    
    def no_vote(self,seq):
        for i , ans in enumerate(seq):
            if str(f'{i+1}バンド目') == str(ans):
                return True
        return False
    
    def has_duplicate(self,seq):
        return len(seq) != len(set(seq))
            
    def get(self, *args, **kwargs):
        admin_result_button_check = AdminResultButtonCheck()
        if self.request.user.is_superuser == False or admin_result_button_check == False:
            return redirect('top')
        all_user = User.objects.all()
        band_name_dict = self.get_band_name_dict(Band.objects.all())
        band_name_dict = self.get_count(band_name_dict,all_user)
        rank_tuple = sorted(band_name_dict.items(), key=lambda x:x[1], reverse=True)
        rank_tuple = self.get_rank(rank_tuple)

        vote = Vote.objects.latest('date_joined')
        band_num = [i for i in range(1,vote.band_num + 1)]
        all_band = Band.objects.all()
        
        return render(self.request,'admin_result.html', {
                                                        'rank_tuple':rank_tuple,
                                                        'band_num':band_num, 
                                                        'all_band':all_band}
                                                        )
    
    def post(self, *args, **kwargs):
        all_user = User.objects.all()
        band_name_dict = self.get_band_name_dict(Band.objects.all())
        band_name_dict = self.get_count(band_name_dict,all_user)
        rank_tuple = sorted(band_name_dict.items(), key=lambda x:x[1], reverse=True)
        rank_tuple = self.get_rank(rank_tuple)

        vote = Vote.objects.latest('date_joined')
        band_num = [i for i in range(1,vote.band_num + 1)]
        all_band = Band.objects.all()
        ans = []
        for i in range(vote.band_num):
            ans.append(self.request.POST[f'band{i+1}'])
        
        if self.has_duplicate(ans) == True:
            duplicate_error = "同じバンドを選択しています"
        else:
            duplicate_error = None
        
        if self.no_vote(ans) == True:
            no_vote_error = "無選択が存在しています"
        else:
            no_vote_error = None

        if (duplicate_error == None) and (no_vote_error == None):
            vote.pass_band = ans
            print(ans)
            vote.save()
            return render(self.request,'result_done.html')
        else:
            return render(self.request,'admin_result.html',{
                                                    'rank_tuple':rank_tuple,
                                                    'band_num':band_num, 
                                                    'all_band':all_band,
                                                    'duplicate_error':duplicate_error, 
                                                    'no_vote_error':no_vote_error,
                                                    })

class VoteResultView(LoginRequiredMixin, generic.View):

    def get_band_name(self,seq):
        band_name = []
        for uuid in seq:
            band_name.append(Band.objects.get(uuid = uuid).name)
        return band_name

    def get(self, *args, **kwargs):
        result_button_check = ResultButtonCheck()
        if result_button_check == False:
            return redirect('top')
        else:
            vote = Vote.objects.latest('date_joined')
            band_name = self.get_band_name(vote.pass_band)
            random.shuffle(band_name)
            return render(self.request,'result.html',{'band_name':band_name,})

class ProfileView(LoginRequiredMixin, generic.View):

    def get_band_name(self,seq):
        band_name = []
        for uuid in seq:
            band_name.append(Band.objects.get(uuid = uuid).name)
        return band_name

    def get(self, *args, **kwargs):
        vote_contents = self.request.user.vote_contents
        band_name = self.get_band_name(vote_contents)
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

