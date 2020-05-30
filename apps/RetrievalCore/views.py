from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from django.db.models import Q

import json
from datetime import datetime
import apps.RetrievalCore.CommonTools as tool
from RetrievalCore.models import Document, Session, UserProfile, DVectorRecord
from MultiTopicDocRetrieval.settings import CLASS_NUM, SESSION_NUM, ETA, classification


class DocumentListView(View):
    """
    文献列表视图
    """
    def get(self, request, user_id, flag):
        """
        验证用户是否登录
            已登录:
                查找当前用户是否有未完成的Session、没有:
                    1.从Document取出20个该用户还未打分过的文档
                    2.根据当前用户、1中取出的20个文档生成Session记录存库
                    3.返回页面（需要包含 用户实体、Session实体、Documents实体列表）
                有未完成的Session:
                    恢复session
            未登录:
                返回登录页面
        :param request:
        :return:
        """
        flag = int(flag)
        # user_id = request.path.split("list")[1].replace("/", "")
        # flag = int('')
        if len(user_id) < 1:
            return render(request, "login.html")
        # user_id = int(user_id)
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            return render(request, "login.html")
        user = user[0]
        user_sessions = Session.objects.filter(user=user, D_vector=None, P_vector=None)
        documents = None
        if len(user_sessions) > 0:
            for session in user_sessions:
                if session.documents.first().flag == flag:
                    user_session = session
                    documents = user_session.documents.all()
                    break
            if documents is None:
                # TODO 此处documents可能为空，因为有可能是一个新的flag
                pass
            new = tool.sort_docs_by_dp(documents, user.get_D_vector(flag), user.get_P_vector(flag))
            for i in range(len(new)):
                print(new[i].id, documents[i].id)
            return render(request, "list.html", {
                "documents": documents,
                "session": user_session,
                "user_id": user_id,
                "flag": flag
            })
        else:
            user_sessions = Session.objects.filter(user=user)
            new_documents = Document.objects.filter(~Q(session__documents__session__in=list(user_sessions)), flag=flag)[:20]
            new_session = Session.objects.create(user=user, D_vector=None, P_vector=None, precision=None)
            new_session.documents.set(list(new_documents))
            new_session.save()
            new = tool.sort_docs_by_dp(new_documents, user.get_D_vector(flag), user.get_P_vector(flag))
            return render(request, "list.html", {
                "documents": new,
                "session": new_session,
                "user_id": user_id,
                "flag": flag
            })

    def post(self, request):
        """
        {
           "1":{
              "classification":3,
              "relevance":0.8
           },...
        }
        :param request:
        :return:
        """
        json_response = {
            "success": False,
            "msg": "",
            "user_id": None,
            "redirect": None
        }
        user_relevance = json.loads(request.POST.get("session_relevance"))
        user_id = request.POST.get("user_id")
        flag = int(request.POST.get("flag"))
        json_response['flag'] = flag
        if len(user_id) < 1:
            json_response["redirect"] = "/user/login/"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user_id = int(user_id)
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            json_response["redirect"] = "/user/login/"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user = user[0]
        user_sessions = Session.objects.filter(user=user, D_vector=None, P_vector=None)
        if len(user_sessions) > 0:
            for session in user_sessions:
                if session.documents.first().flag == flag:
                    user_session = session
                    break
            d = user.get_D_vector(flag)
            user_d = [0 for i in range(len(d))]
            num_d = [0 for i in range(len(d))]
            if user_relevance:
                for k, v in user_relevance.items():
                    user_d[v['classification']] += v['relevance']
                    num_d[v['classification']] += 1
                for k, v in enumerate(user_d):
                    if v > 0:
                        v /= num_d[k]
            new_d = json.dumps(tool.update_d_value(d, user_d, SESSION_NUM))
            new_p = json.dumps(tool.update_p_value(user.get_P_vector(), new_d, ETA))
            user_session.D_vector = new_d
            user_session.P_vector = new_p
            if flag == 0:
                user.D_vector_female = new_d
                user.P_vector_female = new_p
            elif flag == 1:
                user.D_vector_male = new_d
                user.P_vector_male = new_p
            else:
                user.D_vector_older = new_d
                user.P_vector_older = new_p
            user_session.save()
            user.save()
            # session_documents = Document.objects.filter(session__documents__session__in=[user_session])
            json_response["redirect"] = "/user/assess/{0}/".format(user_session.id)
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})


class DocumentDetailView(View):
    def get(self, request, document_id, session_id):
        """
        验证用户是否登录
            已登录:
                1.根据document_id从Document中取出该文献详细信息
                2.返回页面（需要包含 Document实体、用户实体、Session实体）
            未登录:
                返回登录页面
        :param session_id:
        :param document_id:
        :param request:
        :return:
        """
        session = Session.objects.filter(id=session_id)[0]
        document = Document.objects.filter(id=document_id)[0]
        return render(request, "doc_detail.html", {
            "document": document,
            "session": session
        })


class UserLogin(View):
    """
    用戶登录
    """
    def get(self, request):
        """
        访问用户登录界面
        :param request:
        :return:
        """
        return render(request, "login.html")

    def post(self, request):
        """
        提交登录信息(账户名，密码)
        :param request:
        :return:
        """
        json_response = {
            "success": False,
            "msg": "",
            "user_id": None,
            "redirect": None
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        flag = int(request.POST.get("flag"))
        json_response['flag'] = flag
        if username is None or password is None:
            json_response["msg"] = "用户名或密码为空！"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user = UserProfile.objects.filter(username=username)
        if len(user) < 1:
            json_response["msg"] = "未找到该用户"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        else:
            user = user[0]
        if user.password == password or user.check_password(password):
            json_response["success"] = True
            json_response["user_id"] = user.id
            try:
                if sum(user.get_D_vector(flag)) == 0:
                    json_response["redirect"] = "/user/preference_customize/{0}/{1}/".format(user.id, flag)
            except Exception as e:
                json_response["redirect"] = "/user/preference_customize/{0}/{1}/".format(user.id, flag)
        else:
            json_response["msg"] = "密码错误"
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})


class UserRegister(View):
    """
    用户注册
    """
    def get(self, request):
        """
        访问用户注册界面
        :param request:
        :return:
        """
        return render(request, "register.html")

    def post(self, request):
        """
        提交注册信息(账户名，密码)
        :param request:
        :return:
        """
        json_response = {
            "success": False,
            "msg": "",
            "redirect": ""
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username is None or password is None:
            json_response["msg"] = "用户名或密码为空！"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user = UserProfile.objects.filter(username=username)
        if len(user) > 0:
            json_response["msg"] = "用户已注册"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        new_user = UserProfile()
        new_user.username = username
        new_user.password = password
        init_d, init_p = tool.initial_d_p_vector(CLASS_NUM[0])
        new_user.D_vector_female = json.dumps(init_d)
        new_user.P_vector_female = json.dumps(init_p)
        init_d, init_p = tool.initial_d_p_vector(CLASS_NUM[1])
        new_user.D_vector_male = json.dumps(init_d)
        new_user.P_vector_male = json.dumps(init_p)
        init_d, init_p = tool.initial_d_p_vector(CLASS_NUM[2])
        new_user.D_vector_older = json.dumps(init_d)
        new_user.P_vector_older = json.dumps(init_p)
        new_user.save()
        json_response["success"] = True
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})


class UserPreference(View):
    def get(self, request, user_id, flag):
        # user_id = request.path.split("preference_customize")[1].replace("/", "")
        # flag = int('')
        flag = int(flag)
        if len(user_id) < 1:
            return render(request, "login.html")
        user_id = int(user_id)
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            return render(request, "login.html")
        user = user[0]
        D_vector = user.get_D_vector(flag)
        for i in range(len(classification[flag])):
            classification[flag][i]["interest_value"] = D_vector[i]
        return render(request, "preference_customize.html", {
            "user": user,
            "classification": classification[flag],
            "flag": flag
        })

    def post(self, request, user_id, flag):
        flag = int(flag)
        user_preference = request.POST.get("user_preference")
        user_preference = json.loads(user_preference)
        if len(user_id) < 1:
            return render(request, "login.html")
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            return render(request, "login.html")
        user = user[0]
        if user_preference is not None and sum(user_preference) > 0:
            if flag == 0:
                user.D_vector_female = json.dumps(user_preference)
                user.P_vector_female = json.dumps(tool.update_p_value(user.get_P_vector(flag), user_preference, 0.5))
            elif flag == 1:
                user.D_vector_male = json.dumps(user_preference)
                user.P_vector_male = json.dumps(tool.update_p_value(user.get_P_vector(flag), user_preference, 0.5))
            else:
                user.D_vector_older = json.dumps(user_preference)
                user.P_vector_older = json.dumps(tool.update_p_value(user.get_P_vector(flag), user_preference, 0.5))
            user.save()
        return JsonResponse({"success": True, "user_id": user_id}, json_dumps_params={"ensure_ascii": False})


class PreferenceAssess(View):
    """
    推荐评估
    """
    def get(self, request, session_id, flag):
        # session_id = request.path.split("assess")[1].replace("/", "")
        # flag = int('')
        if session_id is None or len(session_id) < 1:
            return render(request, "login.html")
        session = Session.objects.filter(id=session_id)
        if len(session) < 1:
            return render(request, "login.html")
        session = session[0]
        session_documents = session.documents.all()
        user = session.user
        new = tool.sort_docs_by_dp(session_documents, user.get_D_vector(flag), user.get_P_vector(flag))
        return render(request, "preference_assess.html", {
            "session": session,
            "documents": new,
            "user": user,
            "flag": flag
        })

    def post(self, request):
        json_response = {
            "success": False,
            "msg": "",
            "user_id": None,
            "redirect": None
        }
        session_id = request.POST.get("session_id")
        flag = int(request.POST.get("flag"))
        session = Session.objects.filter(id=session_id).all()[0]
        user_preference = request.POST.get("user_preference")
        session.precision, session.default_precision = tool.calc_precision(json.loads(user_preference), session.documents.all())
        session.save()
        json_response["success"] = True
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})


class RecordPreference(View):
    def get(self, request, user_id):
        flag = int('')
        user = UserProfile.objects.filter(id=user_id)[0]
        return render(request, "record_preference.html", {
            "user": user,
            "classification": classification[flag]
        })

    def post(self, request, user_id):
        json_response = {
            "success": False,
            "msg": "",
            "user_id": None,
            "redirect": None
        }
        user = UserProfile.objects.filter(id=user_id)[0]
        user_preference = request.POST.get("user_preference")
        flag = int(request.POST.get("flag"))
        D_record = DVectorRecord.objects.create(user=user)
        D_record.user_D_vector = user_preference
        D_record.sys_D_vector = user.D_vector
        D_record.submit_time = datetime.now()
        D_record.flag = flag
        D_record.save()
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
