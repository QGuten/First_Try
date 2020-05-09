from django.contrib.auth.models import AbstractUser
from django.db import models
from mdeditor.fields import MDTextField


# Create your models here.


class MDEditorForm(models.Model):
    """
    @Author: 朱孟彤
    @desc: md文档表
    """
    id = models.AutoField(verbose_name='id', primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=50)
    context = MDTextField()
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)  # 不可改变
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True)  # 每次更新数据都会更新时间
    created_by = models.CharField(verbose_name='创建人', max_length=20, null=True)
    updated_by = models.CharField(verbose_name='更新人', max_length=20, null=True)

    class Meta:
        verbose_name = 'md文档表'
        db_table = 't_base_md'


class Role(models.Model):
    """
    @Author: 朱孟彤
    @desc: 角色表
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Menu')
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    def __str__(self):
        return self.title

    @property
    def menu_title(self):
        return self.permissions.title

    class Meta:
        verbose_name = '角色表'
        db_table = 't_base_role'


class Menu(models.Model):
    """
    @Author: 朱孟彤
    @desc: 菜单表
    """
    id = models.AutoField(verbose_name='id', primary_key=True)
    title = models.CharField(max_length=32, verbose_name='菜单')
    parent = models.ForeignKey('self', models.SET_NULL, verbose_name='父级项目', null=True, blank=True)
    url = models.CharField(verbose_name='含正则的URL', max_length=100, default='#')
    icon = models.CharField(verbose_name='图标icon', max_length=100,  null=True)
    order = models.SmallIntegerField(verbose_name='展示顺序')
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '菜单表'
        db_table = 't_base_menu'


class OpsUser(AbstractUser):
    """
    @Author: 朱孟彤
    @desc: 扩展User模型
    """
    mobile_no = models.CharField(verbose_name='手机号码', max_length=11, db_index=True)
    department = models.CharField(verbose_name='部门', max_length=11, db_index=True)
    role = models.ManyToManyField(verbose_name='角色', to='Role', max_length=11)
    pro = models.ManyToManyField(verbose_name='项目', to='ProjectForBase')

    class Meta:
        verbose_name = '用户表'
        db_table = 't_ops_user'
        ordering = ['id']


class BaseSysParam(models.Model):
    """
    @Author: 朱孟彤
    @desc: 系统配置表
    """
    id = models.AutoField(verbose_name='id', primary_key=True)
    param_key = models.CharField(verbose_name='参数键', max_length=100, db_index=True)
    param_value = models.CharField(verbose_name='参数值', max_length=255, db_index=True)
    param_name = models.CharField(verbose_name='参数名称', max_length=255, db_index=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)  # 每次更新数据都会更新时间
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='sys_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='sys_updated_by')
    description = models.TextField(verbose_name='描述', max_length=255, null=True)
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '系统配置表'
        db_table = 't_base_sys_param'
        ordering = ['id']


class JobForBase(models.Model):
    """
    @Author: 朱孟彤
    @desc: 系统任务表
    """
    id = models.AutoField(verbose_name='id', primary_key=True)
    name = models.CharField(verbose_name='任务名称', max_length=100, db_index=True)
    state = models.SmallIntegerField(verbose_name='任务状态', default=10)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)  # 每次更新数据都会更新时间
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='syj_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='syj_updated_by')
    description = models.TextField(verbose_name='描述', max_length=255, null=True)
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '系统任务表'
        db_table = 't_base_sys_job'
        ordering = ['id']


class JobRecordForBase(models.Model):
    """
    @Author: 朱孟彤
    @desc: 系统任务执行记录表
    """
    id = models.AutoField(verbose_name='id', primary_key=True)
    job = models.ForeignKey(JobForBase, on_delete=models.CASCADE, verbose_name="任务id")
    params = models.TextField(verbose_name='任务执行参数')
    date = models.TextField(verbose_name='任务执行结果内容')
    explain = models.TextField(verbose_name='任务说明')
    state = models.SmallIntegerField(verbose_name='任务状态', default=10)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)  # 每次更新数据都会更新时间
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='jr_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='jr_updated_by')
    description = models.TextField(verbose_name='描述', max_length=255, null=True)
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '系统任务执行记录表'
        db_table = 't_base_sys_job_record'
        ordering = ['id']


class ProjectForBase(models.Model):
    """
    @Author: 朱孟彤
    @desc: 项目配置表
    """
    id = models.AutoField(verbose_name="id", primary_key=True)
    parent = models.ForeignKey('self', models.SET_NULL, verbose_name='父级项目', null=True, blank=True, db_index=True)
    project_name = models.CharField(verbose_name="项目名称", max_length=50, db_index=True)
    project_type = models.CharField(verbose_name="项目类型", max_length=20, db_index=True)
    project_code = models.CharField(verbose_name="项目code", max_length=10, null=True, db_index=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    description = models.TextField(verbose_name='描述', max_length=255, null=True)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='sp_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='sp_updated_by')
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '系统项目配置表'
        db_table = 't_base_sys_project'
        ordering = ['id']

    @property
    def get_name(self):
        return self.parent.project_name, self.parent.id


class VersionForProject(models.Model):
    """
    @Author: 朱孟彤
    @desc: 项目版本表
    """
    id = models.AutoField(verbose_name="id", primary_key=True)
    pro = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE, verbose_name='所属项目', db_index=True)
    type = models.CharField(verbose_name="版本号", max_length=20, db_index=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='pv_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='pv_updated_by')
    description = models.TextField(verbose_name='描述', max_length=255, null=True)
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '系统项目配置表'
        db_table = 't_base_sys_project_version'
        ordering = ['id']


class RequestsForResources(models.Model):
    """
    @Author: 朱孟彤
    @desc: 接口管理列表
    """
    id = models.AutoField(verbose_name='id', primary_key=True)
    serial_number = models.CharField(verbose_name='接口序列号', max_length=20, db_index=True)  # 接口序列号，用来做接口的唯一标识
    re_name = models.CharField(verbose_name='接口名称', max_length=50, db_index=True)
    re_path = models.CharField(verbose_name='请求地址', max_length=200, db_index=True)
    re_method = models.CharField(verbose_name='请求方式', max_length=50, db_index=True)
    project = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE)
    re_params = models.TextField(verbose_name='请求参数')
    re_response = models.TextField(verbose_name='响应参数', null=True)
    edition = models.CharField(verbose_name='版本', max_length=20)
    developer = models.CharField(verbose_name='开发者', max_length=20, db_index=True)
    if_have_case = models.SmallIntegerField(verbose_name='用例是否已生成', default=1)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)  # 每次更新数据都会更新时间
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='re_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='re_updated_by')
    description = models.TextField(verbose_name='描述', max_length=255, null=True)
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '接口管理表'
        db_table = 't_resource_requests'
        ordering = ['-id']

    @property
    def menu_title(self):
        return self.project.project_name, self.project.id


class ConfigForResources(models.Model):
    """
    @Author: 朱孟彤
    @desc: 资源库配置表
    """
    id = models.AutoField(verbose_name='id', primary_key=True)
    pro = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE, null=True, db_index=True)
    key = models.CharField(verbose_name='参数键', max_length=100, db_index=True)
    value = models.CharField(verbose_name='参数值', max_length=255, db_index=True)
    name = models.CharField(verbose_name='参数名称', max_length=255, db_index=True)
    created_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)  # 每次更新数据都会更新时间
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='rc_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='rc_updated_by')
    description = models.TextField(verbose_name='描述', max_length=255, null=True, blank=True)
    abandon_flag = models.SmallIntegerField(verbose_name='删除标识', default=1)

    class Meta:
        verbose_name = '资源库配置表'
        db_table = 't_resource_config'
        ordering = ['id']

    @property
    def menu_title(self):
        return self.pro.project_name, self.pro.id


class CaseSuiteForCaseCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 自动化测试，用例集合表
    """
    id = models.AutoField('套件id', primary_key=True)
    pro = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE, null=True, db_index=True)
    case_type = models.ForeignKey(BaseSysParam, on_delete=models.CASCADE)  # 用例类型，配置于系统配置中
    suite_name = models.CharField('套件名称', null=False, max_length=50, db_index=True)
    case_id = models.ManyToManyField(verbose_name='关联的测试用例', to='CaseInfoForCaseCenter', null=True, db_index=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200, null=True)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='su_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='su_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '用例集合表'
        db_table = 't_case_center_suite'
        ordering = ['id']

    @property
    def other_info(self):
        return self.pro.project_name, self.pro.id, self.case_type.param_name, self.case_type.id


class CaseInfoForCaseCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 自动化测试，用例信息表
    """
    id = models.AutoField('用例id', primary_key=True)
    pro = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE, null=True, db_index=True)
    case_type = models.ForeignKey(BaseSysParam, on_delete=models.CASCADE, db_index=True)  # 用例类型
    case_suite = models.ForeignKey(CaseSuiteForCaseCenter, on_delete=models.CASCADE, null=True, db_index=True)  # 套件id
    case_name = models.CharField('用例名称', max_length=255, null=False, db_index=True)
    if_update = models.IntegerField('更新状态，有更新10、全部已更新20、全部拒绝110', default=0)
    step_list = models.ManyToManyField(verbose_name='关联的用例步骤', to='CaseStepForCaseCenter', max_length=11, db_index=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200, null=True)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='ci_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='ci_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '用例信息表'
        db_table = 't_case_center_case_info'
        ordering = ['id']

    @property
    def other_info(self):
        return self.pro.project_name, self.pro.id, self.case_type.param_name, self.case_type.id, self.case_suite.id, self.case_suite.suite_name


class CaseStepForCaseCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 自动化测试，用例步骤表
    """
    id = models.AutoField('步骤id', primary_key=True)
    case = models.IntegerField('用例ID/套件ID')  # 用例ID/套件ID
    step_type = models.CharField('步骤类型', null=True, max_length=10)  # setup 、teardown、execute
    step_id = models.IntegerField('步骤id，用于测试用例执行顺序排序', default=1)
    execute_type = models.CharField('执行类型', max_length=500, null=True)  # 10 请求接口、20 sql、30 mq……
    execute_info = models.TextField('执行参数', null=True)  # 请求接口、sql、mq
    for_id = models.IntegerField('关联id', null=True)  # 关联的接口、sql等 ID
    save_list = models.CharField('储存参数列表', max_length=500, null=True)
    if_update = models.IntegerField('更新状态，有更新10、已更新20、拒绝110', default=0)
    check_type = models.IntegerField('检查类型')  # 10返回值直接核对，20还是数据数据比对
    param_info = models.TextField('检验参数', null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200, null=True)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='step_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='step_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '用例步骤表'
        db_table = 't_case_center_case_step'
        ordering = ['id']


class IterationForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 迭代管理信息表
    """
    id = models.AutoField('迭代id', primary_key=True)
    pro = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE, null=True, db_index=True)  # 迭代所属项目
    name = models.CharField('迭代名称', null=True, max_length=50, db_index=True)
    state = models.PositiveIntegerField('迭代状态', default=10, db_index=True)
    version = models.ForeignKey(VersionForProject, on_delete=models.CASCADE, verbose_name='所属版本', null=True)
    job = models.ManyToManyField(verbose_name='迭代相关任务', to='SubJobInfoForJobCenter', max_length=11, db_index=True)
    report = models.ManyToManyField(verbose_name='迭代相关执行报告', to='JobReportListForJobCenter', max_length=11, db_index=True, null=True)
    exe_overview = models.TextField('执行概览', max_length=200, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='it_re_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='it_re_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '迭代管理信息表'
        db_table = 't_job_center_iteration'
        ordering = ['id']


class IterationRecordForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 迭代执行记录表
    """
    id = models.AutoField('记录id', primary_key=True)
    it = models.ForeignKey(IterationForJobCenter, on_delete=models.CASCADE, null=True, db_index=True)  # 记录所属迭代
    report = models.ManyToManyField(verbose_name='迭代相关执行报告', to='JobReportListForJobCenter', max_length=11, db_index=True, null=True)
    exe_overview = models.TextField('执行概览', max_length=200, null=True)
    description = models.TextField('描述', max_length=200)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='it_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='it_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '迭代管理信息表'
        db_table = 't_job_center_iteration_record'
        ordering = ['id']


class JobInfoForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 测试任务信息表
    """
    id = models.AutoField('任务id', primary_key=True)
    pro = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE, null=True, db_index=True)
    job_type = models.ForeignKey(BaseSysParam, on_delete=models.CASCADE, db_index=True)
    job_name = models.CharField('任务名称', null=True, max_length=50, db_index=True)
    job_state = models.PositiveIntegerField('任务状态', db_index=True)
    domain_path = models.CharField('请求域名', max_length=200, null=True)
    header_data = models.TextField('请求头', null=True)
    autograph_config = models.TextField('签名配置', null=True)
    global_list = models.TextField('全局变量', null=True)
    report_id = models.IntegerField('测试报告id', null=True)
    if_update = models.IntegerField('更新状态，有更新10、全部已更新20、全部拒绝110', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='ji_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='ji_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '测试任务信息表'
        db_table = 't_job_center_job_info'
        ordering = ['id']

    @property
    def other_info(self):
        return self.pro.project_name, self.pro.id, self.job_type.param_name, self.job_type.id


class JobDataForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 测试任务、测试用例与测试数据关系表
    """
    id = models.AutoField('任务id', primary_key=True)
    if_setup = models.IntegerField('是否是前提条件', default=0, null=True)
    exe_step = models.IntegerField('执行步骤', default=1, null=True)
    job = models.ForeignKey(JobInfoForJobCenter, on_delete=models.CASCADE, null=True)
    case = models.ForeignKey(CaseInfoForCaseCenter, on_delete=models.CASCADE, null=True)
    exe_data = models.TextField('执行数据', null=True)
    save_list = models.CharField('储存参数列表', max_length=500, null=True)
    domain_path = models.CharField('请求域名', max_length=200, null=True)
    if_update = models.IntegerField('更新状态，有更新10、已更新20、拒绝110', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='jd_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='jd_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '测试任务、测试用例与测试数据关系表'
        db_table = 't_job_center_job_data'
        ordering = ['id']

    @property
    def other_info(self):
        return self.job.job_name, self.job.id, self.case.case_name, self.case.id


class SubJobInfoForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 子任务信息表
    """
    id = models.AutoField('任务id', primary_key=True)
    pro = models.ForeignKey(ProjectForBase, on_delete=models.CASCADE, null=True, db_index=True)
    job_type = models.ForeignKey(BaseSysParam, on_delete=models.CASCADE, db_index=True)
    job = models.ForeignKey(JobInfoForJobCenter, on_delete=models.CASCADE, db_index=True)  # 关联任务id
    job_name = models.CharField('任务名称', null=True, max_length=50, db_index=True)
    domain_path = models.CharField('请求域名', max_length=200, null=True)
    autograph_config = models.TextField('签名配置', null=True)
    header_data = models.TextField('请求头', null=True)
    global_list = models.TextField('全局变量', null=True)
    job_state = models.PositiveIntegerField('任务状态', db_index=True)
    if_update = models.IntegerField('更新状态，父任务有更新10、用例有更新20、父任务和用例均有更新30、拒绝更新测试用例112、拒绝更新子任务信息111、40全部更新', default=0)
    report_id = models.IntegerField('测试报告id', null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='sj_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='sj_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '测试任务信息表'
        db_table = 't_job_center_sub_job_info'
        ordering = ['id']

    @property
    def other_info(self):
        return self.pro.project_name, self.pro.id, self.job_type.param_name, self.job_type.id


class SubJobDataForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 子任务、测试用例与测试数据关系表
    """
    id = models.AutoField('任务id', primary_key=True)
    if_setup = models.IntegerField('是否是前提条件', default=0, null=True)
    exe_step = models.IntegerField('执行步骤', default=1, null=True)
    job = models.ForeignKey(SubJobInfoForJobCenter, on_delete=models.CASCADE, null=True)
    case = models.ForeignKey(CaseInfoForCaseCenter, on_delete=models.CASCADE, null=True)
    exe_data = models.TextField('执行数据', null=True)
    if_update = models.IntegerField('更新状态，有更新10、已更新20、拒绝110', default=0)
    save_list = models.CharField('储存参数列表', max_length=500, null=True)
    domain_path = models.CharField('请求域名', max_length=200, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='sjd_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='sjd_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '测试任务、测试用例与测试数据关系表'
        db_table = 't_job_center_sub_job_data'
        ordering = ['id']

    @property
    def other_info(self):
        return self.job.job_name, self.job.id, self.case.case_name, self.case.id


class JobReportListForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 测试报告
    """
    id = models.AutoField('报告id', primary_key=True)
    report_name = models.CharField('报告名称', max_length=50, null=True, db_index=True)
    job = models.ForeignKey(SubJobInfoForJobCenter, on_delete=models.CASCADE, db_index=True)  # 关联任务id
    setup_count = models.CharField('前提条件统计', max_length=200, null=True)
    setup_exe_count = models.CharField('前提步骤执行统计', max_length=200, null=True)
    case_count = models.CharField('测试用例统计', max_length=200, null=True)
    case_exe_count = models.CharField('测试用例步骤执行统计统计', max_length=200, null=True)
    start_at = models.DateTimeField('开始时间')  # 当前时间
    status = models.IntegerField('任务状态', default=10, db_index=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200, null=True)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='rep_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='rep_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '测试报告'
        db_table = 't_job_center_report'
        ordering = ['id']

    @property
    def other_info(self):
        return self.job.job_name, self.job.id


class JobReportInfoForJobCenter(models.Model):
    """
    @Author: 朱孟彤
    @desc: 测试报告详情
    """
    id = models.AutoField('报告id', primary_key=True)
    report = models.ForeignKey(JobReportListForJobCenter, on_delete=models.CASCADE)  # 关联报告ID
    case = models.ForeignKey(CaseInfoForCaseCenter, on_delete=models.CASCADE, null=True)   # 关联的用例ID
    step = models.ForeignKey(CaseStepForCaseCenter, on_delete=models.CASCADE, null=True)   # 关联的用例步骤ID
    # exe_path = models.CharField('执行请求地址', max_length=100, null=True)
    exe_info = models.TextField('执行数据', null=True)
    result_info = models.TextField('执行结果数据', null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)  # 不可改变
    updated_at = models.DateTimeField('更新时间', auto_now=True)  # 每次更新数据都会更新时间
    description = models.TextField('描述', max_length=200)
    created_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='创建人', related_name='ri_created_by')
    updated_by = models.ForeignKey(OpsUser, on_delete=models.CASCADE, verbose_name='更新人', related_name='ri_updated_by')
    abandon_flag = models.IntegerField('删除标识', default=1)

    class Meta:
        verbose_name = '测试报告详情'
        db_table = 't_job_center_report_info'
        ordering = ['id']

    @property
    def other_info(self):
        return self.report.report_name, self.report.id
