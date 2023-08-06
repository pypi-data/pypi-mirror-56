# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms

from .models import MentorScoreWeek, Report


class MentorScoreWeekForm(forms.ModelForm):
    class Meta:
        model = MentorScoreWeek
        fields = ['year', "week", "info"]

    # def update_rank(self):


class MentorScoreWeekUpdateScoreForm(forms.ModelForm):
    class Meta:
        model = MentorScoreWeek
        fields = []
        fieldsets = [(u'aa', {"fields": ["score1", "score2"]})]

    def __init__(self, request_user, *args, **kwargs):
        super(MentorScoreWeekUpdateScoreForm, self).__init__(*args, **kwargs)
        _list = MentorScoreWeek.get_score_title_list(request_user)
        # score1, score2, score3, score4 = None, None, None, None
        for _dict in _list:
            if not _dict["can_change"]:
                _widget = forms.TextInput(attrs={'disabled': 'disabled'})
            else:
                _widget = None
            key = _dict["key"]
            self.fields[key] = forms.FloatField(label=_dict["name"], required=False, help_text=_dict["help_text"],
                                                widget=_widget)
            self.initial[key] = kwargs["instance"].__dict__[key]
            # if f["can_change"]:
            #     score2 = forms.FloatField(label=f["name"], required=False)
            # if f["can_change"]:
            #     score3 = forms.FloatField(label=f["name"], required=False)
            # if f["can_change"]:
            #     score4 = forms.FloatField(label=f["name"], required=False)
        # if score1:
        #     self.fields['score1'] = score1
        #     self.initial['score1'] = kwargs["instance"].score1
        # if score2:
        #     self.fields['score2'] = score2
        #     self.initial['score1'] = kwargs["instance"].score1
        # if score3:
        #     self.fields['score3'] = score3
        #     self.initial['score1'] = kwargs["instance"].score1
        # if score4:
        #     self.fields['score4'] = score4
        #     self.initial['score1'] = kwargs["instance"].score1


class UserServerForm(forms.Form):
    status = forms.ChoiceField(label='学生状态', choices=((0, '全部'), (1, "正常")), required=False)

    def __init__(self, request_user, *args, **kwargs):
        super(UserServerForm, self).__init__(*args, **kwargs)
        agent_queryset = request_user.get_teacher_list("agent")
        if agent_queryset.exists():
            agent = forms.ModelChoiceField(queryset=agent_queryset, label='客服', required=False)
            self.fields["agent"] = agent
        lecturer_queryset = request_user.get_teacher_list("lecturer")
        if lecturer_queryset.exists():
            lecturer = forms.ModelChoiceField(queryset=lecturer_queryset, label='讲师', required=False)
            self.fields["lecturer"] = lecturer


class UserSectionForm(forms.Form):
    status = forms.ChoiceField(label='学生状态', choices=((0, '全部'), (1, "正常")), required=False)
    expire_date_start = forms.CharField(label='结课开始日', required=False)
    expire_date_end = forms.CharField(label='结课结束日', required=False)

    def _get_user_class_queryset(self,request_user):
        return request_user.userprofile.get_class_list()

    def __init__(self, request_user, *args, **kwargs):
        super(UserSectionForm, self).__init__(*args, **kwargs)
        mentor_queryset = request_user.get_teacher_list("mentor")
        user_class_queryset = self._get_user_class_queryset(request_user)
        if mentor_queryset.exists():
            self.fields['assistant'] = forms.ModelChoiceField(queryset=mentor_queryset, label='助教', required=False)
        if user_class_queryset.exists():
            self.fields['user_class'] = forms.ModelChoiceField(queryset=user_class_queryset, label='班级', required=False)
            # self.initial['assistant'] = kwargs["instance"].userprofile.lecturer
