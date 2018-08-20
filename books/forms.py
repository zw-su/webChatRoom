from django import forms
from django.forms import widgets, fields
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# 正则表达

# error_message={}  覆盖｛｛form.name.error｝｝信息
# disable  字段是否可以修改

# imagefield  图片上传按钮。
# 需要用django-imagekit来处理用户上传的作为头像的文件，
# 而django-imagekit处理图像需要用到Pillow，它们都可以通过pip工具安装。
# pip3 install pillow
# import PIL


# form 文件上传要加上 enctype="multipart/form-data"

# <!--  {{ form|all_errors }} -->#无效的过滤器
# clean函数是在调用form.is_valid()后默认自动执行的函数

class RegisterForm(forms.Form):
    name = forms.CharField(
        label='用户名',
        required=True,  # 是否允许为空
        # 自定义插件
        widget=widgets.TextInput(attrs={'class':
                                        "register ", 'placeholder': '用户名为2-10个字符'}),
        min_length=2,
        max_length=10,
        # 是否移除用户输入空白
        # strip=True,
        # 自定义错误信息
        error_messages={'required': '用户名不能为空',
                        'min_length': '用户名最少为2个字符',
                        'max_length': '用户名不超过10个字符'},)

    def clean_name(self):
        u = User.objects.filter(name=self.cleaned_data['name'])
        if u:  # 如果用户名已经存在，提示报错信息
            raise ValidationError('用户名已经存在!')
        else:  # 不存在，验证通过
            return self.cleaned_data['name']
    passwd = forms.CharField(
        # label='密码',
        required=True,
        widget=widgets.PasswordInput(attrs={'class':\
                                            "register ", 'placeholder': '密码为6-16个字符'}),
        min_length=6,
        max_length=16,
        # strip=True,
        # 验证器
        validators=[
            # 正则内容,对密码的认证
            RegexValidator(r'((?=.*\d))^.{6,16}$', '必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,16}$', '必须包含字母'),
            # RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,16}$', '必须包含特殊字符'),
            RegexValidator(r'^.(\S){6,16}$', '密码不能包含空白字符'),

        ],
        error_messages={'required': '密码不能为空',
                        'min_length': '密码最少为6个字符',
                        'max_length': '密码不超过16个字符'},

    )
    passwd_again = forms.CharField(
        # label='密码',
        # render_value会对于PasswordInput，错误是否清空密码输入框内容，默认为清除，我改为不清楚
        widget=widgets.PasswordInput(
            attrs={'class': "register ", 'placeholder': '请再次输入密码!'}, render_value=True),
        required=True,
        min_length=6,
        max_length=16,
        # strip=True,
        error_messages={'required': '请再次输入密码!', }
    )

    def _clean_new_password2(self):  # 查看两次密码是否一致
        password1 = self.cleaned_data.get('passwd')
        password2 = self.cleaned_data.get('passwd_again')
        if password1 and password2:
            if password1 != password2:
                 # self.error_dict['pwd_again'] = '两次密码不匹配'
                raise ValidationError('两次密码不匹配！')
    # fields.CharField()有什么区别
    age = forms.IntegerField(
        # label='年龄',
        required=True,
        # strip=True,
        widget=widgets.NumberInput(attrs={'class':
                                          "register", 'placeholder': '16-100'}),
    )

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 16 or age > 100:
            raise ValidationError("年龄不符合要求")
        return age
    sex = forms.ChoiceField(
        # label='性别',
        choices=((1, '男'), (0, '女'),),
        initial=1,  # 初始值
        widget=widgets.RadioSelect(attrs={'class': "sex_change"})

    )
    signature = forms.CharField(
        # label='签名',
        required=False,
        max_length=20,
        # widget=forms.Textarea,#多行文本域
        widget=widgets.TextInput(
            attrs={'class': "register ", 'placeholder': '最长20个字符'}),
        help_text='最长20个字符',
        error_messages={'max_length': '签名最长为20个字符!', }
    )

    head_img = forms.ImageField(
        # label='头像',
        required=False,
        help_text='不超过5M',
    )

    def clean(self):

        # 是基于form对象的验证，字段全部验证通过会调用clean函数进行验证

        self._clean_new_password2()


'''由于form组件中每个字段都是类的数据属性（全局变量），在类每次实例化之后，
数据属性不会发生改变，会保留上次的更新结果
           导致无法动态显示数据库的内容(对于下拉框属性)
解决方法一：每次实例化之前，更新xx字段的值
     xx=fields.MultipleChoiceField(
        # choices=models.Classes.objects.values_list('id','title'),
        widget=widgets.SelectMultiple
      )

    def __init__(self,*args,**kwargs):
        super(TeacherForm,self).__init__(*args,**kwargs)
        self.fields['xx'].choices=models.Classes.objects.values_list('id','title')
'''

# 验证顺序：
# 先user字段，在clean_user方法
# 再email字段，在clean_email方法

# form循环，
# 先第一个字段正则表达式判断，执行字段钩子函数；
# 第二个字段正则，第二个的钩子；
# 所有字段完成后，执行clean钩子；
# clean执行完后，执行_post_clean钩子
# 怎么去记：通过看源码去找：
# 先找is_valid，找到errors，找到full_clean，
# 所有的钩子基于full_clean执行的
# email = fields.EmailField(
#         required=True,
#         widget=widgets.TextInput(attrs={'class': "form-control",'placeholder': '请输入邮箱'}),
#         strip=True,
#         error_messages={'required': '邮箱不能为空',
#                           'invalid':'请输入正确的邮箱格式'},
#      )#invalid 是格式错误
# def clean_email(self):
#         # 对email的扩展验证，查找用户是否已经存在
#         email = self.cleaned_data.get('email')
#         email_count = models.User.objects.filter(email=email).count() #从数据库中查找是否用户已经存在
#         if email_count:
#             raise ValidationError('该邮箱已经注册！')
#         return email
