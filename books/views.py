from django.shortcuts import render, redirect
# from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from books import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate  # 密码验证函数
from django.contrib import auth
import json
import queue
import time
import os
import shutil
import random
from django.utils import timezone
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.forms.models import model_to_dict
import string
import datetime
from HelloWorld import settings
from .forms import RegisterForm
from .verify_code import generate_code  # 生成验证码的函数
from PIL import Image  # 形成图像缩略图

MSG_QUEUES = {}

CODE_NUM = 0  # 密码错一次出验证码


def dmy(request):
    global CODE_NUM
    if request.method == 'GET':
        return render(request, 'dmy.html')
    elif request.method == 'POST':
        nm = request.POST.get('name', '')
        pwd = request.POST.get('passwd', '')
        _my_code = request.POST.get('verify_code', '')

        data = models.User.objects.filter(name=nm)
        if data:
            result = check_password(pwd, data[0].passwd)

            if result:
                if CODE_NUM > 1:
                    if cache.get('random_code', '').lower() == _my_code:
                        print('验证正确')
                    else:
                        data = load_code(request)
                        data['code_switch'] = True
                        data['code_error'] = '验证码错误'
                        return render(request, 'dmy.html', data)
                request.session['is_hero'] = True
            # request.session.setdefault('k1',123)  存在则不设置
                request.session.setdefault('user', nm)
                # request.session.set_expiry(60 * 5)  # 设置超时时间
                return redirect('/index.html/')
            else:
                passwd_error = '密码错误'

                CODE_NUM += 1
                data = load_code(request)
                data['passwd_error'] = passwd_error
                data['code_switch'] = True
                return render(request, 'dmy.html', data)
        else:
            name_error = '用户名不存在'
            return render(request, 'dmy.html', {'name_error': name_error})

        # result = authenticate(name=nm, password=pwd)


def ajax_code(request):  # 验证码异步验证
    vcode = request.POST.get('vcode', '')  # 判断验证码
    vercode = request.POST.get('vercode', '')
    if vercode == 'ok':
        file_path = settings.VERIFICATION_CODE_IMGS_DIR
        shutil.rmtree(file_path)  # 在验证成功或刷新时删除以前的
        os.mkdir(file_path)
        data = load_code(request)  # 创建新的验证码
        data['msg'] = 'ok'
        return JsonResponse(data)

    if cache.get('random_code', '').lower() == vcode:
        return JsonResponse({'msg': 'ok'})
    else:
        return JsonResponse({'msg': ''})


def load_code(request):  # 输错密码加载验证码到前端
    # today_date = datetime.date.today().strftime('%Y%m%d')
    # strftime()接收时间元组,返回字符串表示的本地时间
    # verify_code_path = '%s/%s' % (settings.VERIFICATION_CODE_IMGS_DIR,
    #                               today_date)

    random_filename = ''.join(random.sample(string.ascii_lowercase, 4))
    random_code = generate_code(
        settings.VERIFICATION_CODE_IMGS_DIR, random_filename)
    cache.set('random_code', random_code, 31)
    return {'filename': random_filename}


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        # return render_to_response('register.html',locals())
    elif request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        # form_image=RegisterForm(request.FILES)
        # print('-->',form_image)
        errors = {}
        if form.is_valid():
            data = form.cleaned_data
            data.pop('passwd_again')
            print(len(make_password(data['passwd'])))
            data['passwd'] = make_password(data['passwd'])
            # print(data)
            models.User.objects.create(**data)
            # data=models.User.objects.create()
            return redirect('/dmy.html/')
        else:
            errors = form.errors
    return render(request, 'register.html', locals())


def change_session(request):  # 前端点退出或者关闭清除session
    ''''''
    del_name = request.POST.get('del_name', '')
    key = request.session.session_key

    if del_name:

        try:
            request.session.flush()  # 删除本地sessionid,并删除session表的数据
            # request.session.delete(key)#同上(还没发现区别)
        except KeyError:
            pass
        else:
            return JsonResponse({'msg': 'ok'})


def make_session():  # 获取当前的session的用户

    utid_list = []
    # sessions = Session.objects.filter(
    #     expire_date__gte=datetime.datetime.now())
    # 以上方法报RunTimeWarning：DateTimeField在时区支持处于活动状态时收到天真的日期时间
    sessions = Session.objects.filter(
        expire_date__gte=timezone.now())

    for session in sessions:
        data = session.get_decoded()
        # print('sess_data', data)
        utid_list.append(data.get('user', None))
    online_list = models.User.objects.filter(name__in=utid_list).distinct()
    return online_list


def is_online(request):  # 判断是否在线
    # my_id = request.POST.get('my_id')
    my_id = request.POST.get('id')  # 接受前端的json字符串
    uid = json.loads(my_id)  # 解析字符串成列表
    uid_list = []  # 前端返回的在线的人员id列表
    for x in uid:
        uid_list.append(int(x['my_id']))

    print('--', uid_list)

    online_list = make_session().values('id')
    print(online_list)
    session_list = [i['id'] for i in online_list]
    print(session_list)
    data = {}
    if set(session_list) < set(uid_list):  # (清除不在线的)
        num = set(uid_list) - set(session_list)  # 不在线的人的id
        for y in num:
            data[y] = y
        data['delete'] = 'ok'
        print(data, 'del')
        return JsonResponse(data)
    elif set(session_list) > set(uid_list):  # (显示在线的)
        num = set(session_list) - set(uid_list)  # 不在线的人的id
        for y in num:
            data[y] = y
        print(data)
        return JsonResponse(data)

    return HttpResponse('')
    # if word:(queryset转为json)
    #     word = list(online_list) #ValuesQuerySet对象需要先转换成list(转换get)
    #     data = json.dumps(word) # 把list转成json
    # data = serializers.serialize("json", word) #django.db.models.query.QuerySet对象可以序列化(转换all,filter得到的集合)
    # 第二种 from django.forms.models import model_to_dict(queryset转为字典)(转换get得到的实例)
    #data_dict= model_to_dict(online_list)


def index(request):  # 登录聊天页面函数

    #     #cookie做法
    #     # if request.COOKIES.get('username',None):
    #     #     name=request.COOKIES.get('username',None)
    #     #     return render_to_response('index.html',locals())
    if request.session.get('is_hero', None):
        my_name = request.session.get('user', None)
        cache.set('%s' % my_name, 1, 60 * 60 * 2)

        data = models.User.objects.get(name=my_name)
        my_head = data.head_img

        my_id = data.id
        my_signature = data.signature
        # print('--->>>>', my_head)

        # if my_head:
        # reqimage = Image.open(my_head)
        # reqimage.thumbnail((128, 128), Image.ANTIALIAS)
        # print('-->', reqimage)

        # q = models.UserInfo.objects.all()
        # .values('name','id','ut__title').filter(id__lt=60)
        # q = models.UserInfo.objects.all().select_related('ut').filter(id__lt=60)
        # select_related('ut') 相当 于 inner join 先连成一张表再进行查询
        friends_list = models.User.objects.all()
        group_list = models.WebGroup.objects.all()
        online_list = make_session()
        return render(request, 'chat_main.html', locals())
    else:
        return redirect('/dmy.html/')

# 用类写,get方法就是get,post方法就是post
# from django.views.generic.base import View

# class Cbv(View):
#     def dispatc(self,request,*args,**kwargs):
#         #不管get还是post都要经过这里,可以定制
#         result=super(Cbv,self).dispatc(self,request,*args,**kwargs)
#         return result
#     def get(self,request):
#         return HttpResponse('Cbv.get')

#     def post(self,request):
#         ret= HttpResponse('Cbv.post')#这里就是响应体
#         ret['h1']='v1'#这就是响应头(django要求这样写的)
#         return ret


def send_msg(request):
    my_name = request.session.get('user', None)
    my_id = models.User.objects.get(name=my_name).id
    print(request.POST)
    msg_data = request.POST.get('data')
    if msg_data:
        msg_data = json.loads(msg_data)
# 没有导入json模块时,前端出现jquery模块query-3.3.1.js:9600; 500 (INTERNAL SERVER ERROR)
        msg_data['timestamp'] = time.time()
        if msg_data['type'] == 'single':
            sdata = int(msg_data['to'])
            if not MSG_QUEUES.get(sdata):
                MSG_QUEUES[sdata] = queue.Queue()
            MSG_QUEUES[sdata].put(msg_data)
        else:

            # 群聊,找到该组的所有成员
            group_obj = models.WebGroup.objects.get(id=int(msg_data['to']))
            # 往下是添加字段到members,目前是只要进行群聊就加进去了

            user_obj = models.User.objects.get(id=my_id)
            group_obj.members.add(user_obj)
            group_obj.save()
            # print(group_obj.members.all())
            for member in group_obj.members.select_related():
                # prefetch_related()和select_related()的

                # 这里查询的结果是User里的所有字段还是只有Id(会不会浪费?)
                print('member:', member)
                if not MSG_QUEUES.get(member.id):
                    MSG_QUEUES[member.id] = queue.Queue()
                if member.id != my_id:
                    MSG_QUEUES[member.id].put(msg_data)
        print('send_msg', MSG_QUEUES)

    return HttpResponse("---msg recevied---")


def get_msg(request):
    print('get_msg')
    # 用以下两个必须在admin里面注册
    # my_id=request.user.id
    # my_name=request.user

    my_name = request.session.get('user', None)
    my_id = models.User.objects.get(name=my_name).id
    print(my_name, my_id)
    # 判断自己有没有queue,如果新用户第一次登录就是没有queue
    if my_id not in MSG_QUEUES:
        print('no queue for user[%s]' % my_id, my_name)
        # 创建一个queue
        MSG_QUEUES[my_id] = queue.Queue()
    # 获取消息的大小
    msg_count = MSG_QUEUES[my_id].qsize()
    q_obj = MSG_QUEUES[my_id]
    msg_list = []
    if msg_count > 0:
        for msg in range(msg_count):
            msg_list.append(q_obj.get())
        print('new msgs:', msg_list)
    else:
        print('get', MSG_QUEUES)
        try:
            msg_list.append(q_obj.get(timeout=30))
        except queue.Empty:
            print('\033[41m;no msg\033[0m')

    return HttpResponse(json.dumps(msg_list))


def file_upload(request):
    print('file:', request.FILES)
    file_obj = request.FILES.get('file')
    new_file_name = 'uploads/%s' % file_obj.name
    with open(new_file_name, 'wb+') as new_fo:
        for chunk in file_obj.chunks():
            new_fo.write(chunk)
    return HttpResponse('--file upload success---')
