# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
# 周报
class ClassWeek(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='classWeek_student', verbose_name='学生', null=True)
    class_id = models.IntegerField("班级id", null=True)
    year = models.IntegerField()  # 年
    week = models.IntegerField(null=True)  # 第几周
    type_int = models.IntegerField(default=0)  # 1-班级总数记录 2-平均数记录 3-班级学生的记录 -9:班级老师的记录
    start_date = models.DateField()  # 开始日期
    end_date = models.DateField()
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='classWeek_mentor', null=True,
                               on_delete=models.SET_NULL)  # 助教
    feed_count = models.IntegerField(default=0)  # 发表日志数
    live_mins = models.IntegerField(default=0)  # 练习时长
    live_days = models.IntegerField(default=0)  # 练习天数
    live_count = models.IntegerField(default=0)  # 练习次数
    live_watched_count = models.IntegerField(default=0)  # 被助教观看的次数
    live_watched_days = models.IntegerField(default=0)  # 被助教观看的天数
    live_commented_count = models.IntegerField(default=0)  # 被助教评论的次数
    last_user_section_id = models.IntegerField(null=True)  # 最后一个学习的课件
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'bee_django_report_class_week'
        app_label = 'bee_django_report'
        ordering = ['created_at']
        # permissions = (
        #     ('can_view_mission', '可以进入mission管理页'),
        # )

    def __str__(self):
        return self.id.__str__()

    def __unicode__(self):
        return self.id.__str__()


# 报表 助教周分数报表
class MentorScoreWeek(models.Model):
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    year = models.IntegerField(verbose_name='年')  # 年
    week = models.IntegerField(null=True, verbose_name='第几周')  # 第几周
    score = models.FloatField(null=True, verbose_name='分数')  # 分数
    rank = models.IntegerField(null=True)  # 排名
    level = models.IntegerField(null=True)  # 等级，1优10中20差
    info = models.TextField(null=True, verbose_name='备注', blank=True)  # 备注
    created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
    score1 = models.FloatField(null=True, verbose_name='分数1', blank=True)
    score2 = models.FloatField(null=True, verbose_name='分数2', blank=True)
    score3 = models.FloatField(null=True, verbose_name='分数3', blank=True)
    score4 = models.FloatField(null=True, verbose_name='分数4', blank=True)

    class Meta:
        db_table = 'bee_django_report_montor_score_week'
        app_label = 'bee_django_report'
        ordering = ['created_at']
        permissions = (
            ('view_mentorscoreweek', '可以查看全部助教分数'),
            ('change_score1', '可以修改分数1'),
            ('change_score2', '可以修改分数2'),
            ('change_score3', '可以修改分数3'),
            ('change_score4', '可以修改分数4'),
        )

    def __unicode__(self):
        return (
                "mentorScore->week:" + self.week.__str__() + ",mentor:" + self.mentor.__str__() + ",score:" + self.score.__str__())

    def __str__(self):
        return (self.pk.__str__())

    @classmethod
    def get_score_help_text(cls):
        return "<div>填写说明：【周报评分】为客服根据周报计算填写。【态度分】【技术分】【关心分】3项由讲师填写。</div>" \
               "<div>总分计算：【周报评分】占比70%，【态度分】【技术分】【关心分】3项总和占比30%</div>"

    @classmethod
    def get_score_title_list(cls, op_user):
        return [
            {"key": "score1", "name": "周报评分", "help_text": "根据周报计算填写", "can_change": cls.can_change_score1(op_user)},
            {"key": "score2", "name": "态度分", "help_text": "满分10分", "can_change": cls.can_change_score2(op_user),
             "title": "讲师评分（3项）"},
            {"key": "score3", "name": "技术分", "help_text": "满分10分", "can_change": cls.can_change_score3(op_user)},
            {"key": "score4", "name": "关心分", "help_text": "满分10分", "can_change": cls.can_change_score4(op_user)}]

    @classmethod
    def can_change_score1(cls, op_user):
        if op_user.has_perm("bee_django_report.change_score1"):
            return True
        else:
            return False

    @classmethod
    def can_change_score2(cls, op_user):
        if op_user.has_perm("bee_django_report.change_score2"):
            return True
        else:
            return False

    @classmethod
    def can_change_score3(cls, op_user):
        if op_user.has_perm("bee_django_report.change_score3"):
            return True
        else:
            return False

    @classmethod
    def can_change_score4(cls, op_user):
        if op_user.has_perm("bee_django_report.change_score4"):
            return True
        else:
            return False

    # 计算总分
    def calculate_score(self):
        if self.score1 and self.score2 and self.score3 and self.score4:
            score = self.score1 * 0.7 + (self.score2 + self.score3 + self.score4) * 0.3
        else:
            score = None
        return score

    # 更新总分
    # 计算方法默认为： score1*0.7 + (score2+score3+score4)*0.3
    def update_score(self):
        self.score = self.calculate_score()
        self.save()
        self.__class__.update_rank(self.year, self.week)

    @classmethod
    def update_rank(cls, year, week):
        # 更新无分数助教的排名为空
        _reports = cls.objects.filter(year=year, week=week, score__isnull=True).order_by('-score')
        for r in _reports:
            r.level = None
            r.rank = None
            r.save()

        # 更新有分数助教的排名
        level = [0.2, 0.7, 0.1]
        reports = cls.objects.filter(year=year, week=week, score__isnull=False).order_by('-score')
        count = reports.count()
        score_last = None
        rank_last = 1

        # 排名
        for i, r in enumerate(reports):
            score = r.score
            if not score_last == score:
                rank_last = i + 1
            r.rank = rank_last
            r.save()
            score_last = score

        # 分数级别
        if count > 0:

            # 第一级
            level1_count = int(level[0] * count) + 1
            reports_temp = reports[:level1_count]
            level1_score = reports_temp[:level1_count][-1].score  # 最低分
            level1_reports = reports.filter(score__gte=level1_score)
            for r in level1_reports:
                r.level = 1
                r.save()

            # 第三级
            level3_count = int(level[2] * count) + 1
            reports_temp = reports[::-1]
            level3_score = reports_temp[:level3_count][-1].score  # 最高分
            level3_reports = reports.filter(score__lte=level3_score)
            for r in level3_reports:
                r.level = 3
                r.save()

            # 第二级
            level2_reports = reports.filter(score__lt=level1_score, score__gt=level3_score)
            for r in level2_reports:
                r.level = 2
                r.save()

        return True


# 每次保存分数时，更新排名
# @receiver(post_save, sender=MentorScoreWeek)
# def update_menter_rank_week(sender, **kwargs):
#     menter_score = kwargs['instance']
# print(sender)

#     year = menter_score.year
#     week = menter_score.week
#     MentorScoreWeek.update_rank(year, week)
#     return
class Report(models.Model):
    class Meta:
        db_table = 'bee_django_report'
        app_label = 'bee_django_report'
        permissions = (
            ('can_view_report', '可以查看报表'),
            ('can_view_website_report', 'can_view_website_report'),  # 可以查看网站数据报表
            ('can_view_user_report', 'can_view_user_report'),  # 可以查看用户报表
            ('can_view_course_report', 'can_view_course_report'),  # 可以查看学习报表
        )



    # ======课程部分=========
    # 获取学生最近一个的user_course_section
    @classmethod
    def get_user_current_course_section(cls, user):
        try:
            from bee_django_course.models import UserCourseSection
            ucs = UserCourseSection.get_user_last_course_section(user)
            return ucs
        except:
            return None

    # 获取学生课程的通过的section
    @classmethod
    def get_user_pass_section_list(cls, user_course):
        try:
            from bee_django_course.models import UserCourseSection
            return UserCourseSection.get_user_pass_sections(user_course)
        except:
            return None
