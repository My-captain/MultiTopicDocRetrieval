from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import json
from django.utils import timezone
from MultiTopicDocRetrieval.settings import CLASS_NUM, SESSION_NUM, ETA, classification
from RetrievalCore import CommonTools


class Document(models.Model):
    title = models.CharField(max_length=2048, verbose_name="Title", null=False, blank=False)
    publish_year = models.IntegerField(default=2019, verbose_name="Publish Year")
    authors = models.TextField(verbose_name="Authors")
    abstract = models.TextField(verbose_name="Abstract")
    doi_url = models.TextField(verbose_name="DOI URL")
    references = models.TextField(verbose_name="References")
    publication = models.TextField(verbose_name="Publication")
    classification = models.IntegerField(verbose_name="Classification", default=-1, null=True, blank=True)
    flag = models.IntegerField(verbose_name="DataBase Flag")

    class Meta:
        verbose_name = "Documents"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_authors(self):
        """
        获取当前文献的所有作者
        :return: List<author>
        """
        try:
            author_list = json.loads(self.authors)
            return author_list
        except Exception as e:
            return list()

    def get_references(self):
        """
        获取当前文献的所有引用列表
        :return: List<reference>
        """
        try:
            reference_list = json.loads(self.references)
            return reference_list
        except Exception as e:
            return list()


class UserProfile(AbstractUser):
    # 继承AbstractUser类
    username = models.CharField(max_length=50, unique=True, verbose_name="Username", default="")
    D_vector_female = models.TextField(verbose_name="D vector", null=True, blank=True)
    P_vector_female = models.TextField(verbose_name="P vector", null=True, blank=True)
    D_vector_male = models.TextField(verbose_name="D vector", null=True, blank=True)
    P_vector_male = models.TextField(verbose_name="P vector", null=True, blank=True)
    D_vector_older = models.TextField(verbose_name="D vector", null=True, blank=True)
    P_vector_older = models.TextField(verbose_name="P vector", null=True, blank=True)

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = verbose_name
        db_table = "user_profile"

    def get_D_vector(self, flag):
        """
        获取当前会话的D向量
        :return: List<D_i>
        """
        D_vectors = [self.D_vector_female, self.D_vector_male, self.D_vector_older]
        try:
            D = json.loads(D_vectors[flag])
            return D
        except Exception as e:
            return CommonTools.initial_d_p_vector(CLASS_NUM[flag])[0]

    def get_P_vector(self, flag):
        """
        获取当前会话的P向量
        :return: List<P_i>
        """
        P_vectors = [self.P_vector_female, self.P_vector_male, self.P_vector_older]
        try:
            P = json.loads(P_vectors[flag])
            return P
        except Exception as e:
            return CommonTools.initial_d_p_vector(CLASS_NUM[flag])[1]

    def __str__(self):
        return self.username


class Session(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="User", null=False, blank=False, on_delete=models.CASCADE)
    documents = models.ManyToManyField(Document, verbose_name="Documents")
    D_vector = models.TextField(verbose_name="D vector", null=True, blank=True)
    P_vector = models.TextField(verbose_name="P vector", null=True, blank=True)
    precision = models.FloatField(verbose_name="Precision By User", null=True, blank=True)
    default_precision = models.FloatField(verbose_name="Precision By Default", null=True, blank=True)

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = verbose_name

    def get_D_vector(self):
        """
        获取当前会话的D向量
        :return: List<D_i>
        """
        D = json.loads(self.D_vector)
        return D

    def get_P_vector(self):
        """
        获取当前会话的P向量
        :return: List<P_i>
        """
        P = json.loads(self.P_vector)
        return P


class DVectorRecord(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="User", on_delete=models.CASCADE, null=False, blank=False)
    user_D_vector = models.TextField(verbose_name="D vector of User", null=True, blank=True)
    sys_D_vector = models.TextField(verbose_name="D vector of Algorithm", null=True, blank=True)
    submit_time = models.DateTimeField(verbose_name="Submit Time", null=True, blank=True)
    flag = models.IntegerField(verbose_name="DataBase Flag")

    class Meta:
        verbose_name = "D vector"
        verbose_name_plural = verbose_name

    def get_user_D_vector(self):
        """
        获取当前会话的D向量
        :return: List<D_i>
        """
        D = json.loads(self.user_D_vector)
        return D

    def get_sys_P_vector(self):
        """
        获取当前会话的D向量
        :return: List<D_i>
        """
        D = json.loads(self.sys_D_vector)
        return D

    def __str__(self):
        if self.submit_time is None:
            return "{0}".format(self.user.username)
        else:
            return "{0}:{1}".format(self.user.username, self.submit_time.strftime("%Y/%m/%d:%H:%M:%S"))
