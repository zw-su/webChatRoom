from django.db import models
'''
1.每一个用户有一个好友列表.  (多对多关系)
  2.有一个组列表.         (多对多关系)
'''


class User(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"昵称")
    passwd = models.CharField(max_length=200, verbose_name=u"密码")
    age = models.IntegerField(verbose_name="年龄")
    sex = models.BooleanField(verbose_name="性别")
    signature = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=u"签名")

    head_img = models.ImageField(
        blank=True, null=True, verbose_name="头像", upload_to="uploads")
    # ImageFied字段说明https://docs.djangoproject.com/en/1.9/ref/models/fields/
    # 大概的意思是,ImageField 继承的是FileField,除了FileField的属性被继承了,它还有两个属性 ImageField.height_field和ImageField.width_field,设置后当你存入图片字段时,它会把默认尺寸设置成高height_field宽:width_field
    # 如果想在前端上传图像,需要下载一个Pillow模块,具体使用后面会用到
    friends = models.ManyToManyField(
        'self', related_name='my_friends', blank=True)
    # related_name ,关联自己,用于反向查找

    def __str__(self):
        return self.name

    def friends_list(self):  # 不定义,admin中不能显示manytomany字段(可查看,不能更改)
        return ','.join([i.name for i in self.friends.all()])
    '''django 默认每个主表的对象都有一个是外键的属性，
    可以通过它来查询到所有属于主表的子表的信息。
    这个属性的名称默认是以子表的名称小写加上_set()来表示(上面默认以b_set访问)，
    默认返回的是一个querydict对象。
    related_name 可以给这个外键定义好一个别的名称 '''
    # def my_group_list(self):#本来想在这里查看自己有多少个群的(还没实现)

    #     return ','.join([i.name for i in self.webgroup_set.all()])

    # Meta是在admin后台管理显示的表名称
    class Meta:
        verbose_name = u"用户表"  # 给你的模型类起一个更可读的名字
        verbose_name_plural = u"用户表"  # 模型的复数形式是什么,不指定Django会自动在模型名称后加一个’s’


class WebGroup(models.Model):
    name = models.CharField(max_length=64)
    brief = models.CharField(max_length=255, blank=True, null=True)

    # 下面三个字段都是外建关联User,如果不设related_name,创建表时会报错
    '''原因:当一个表中有多个字段关联外键到一张表,反向查找时,
    用的都是本表的表名,就乱了;比如:1,获得用户a管理那些组 
    2,获得用户a 属于那些组,用户a都是对象,所以反向查找的是同一个表,这肯定有歧义'''
    # 多对多的关系所以用ManyToManyField，如果一对多呢？就用ForeignKey
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # 管理员账户
    admins = models.ManyToManyField(
        User, blank=True, related_name='group_admins')
    # 群组成员
    members = models.ManyToManyField(
        User, blank=True, related_name='group_members')
    max_members = models.IntegerField(default=200)

    def __str__(self):
        return self.name
    # def admins_list(self):
    #     return ','.join([i.name for i in self.admins.all()])
    # def members_list(self):#报错,(admin.E120) The value of 'list_editable' must be a list or tuple.

    #     return ','.join([i.name for i in self.members.all()])

    class Meta:
        verbose_name = u"聊天组"
        verbose_name_plural = u"聊天组"


'''建好表以后在主文件目录下运行
python3 manage.py makemigrations
python3 manage.py migrate(django 1.8)'''
