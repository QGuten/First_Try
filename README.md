# magicbean-platform

自动化测试平台

# 测试平台项目结构与简单介绍
## 简介
> 代码层面讲，整个测试平台除基础服务外，分为用户中心（UserCenter）、系统中心（BaseCenter）、资源库（ResourceCenter）、用例库（CaseCenter）、任务库（JobCenter）。
> 每一个部分，在相对应的页面、接口中均以部分为单位。

## 项目结构
- PlatApp/
平台模块（app）
	- CustomizeDecorator/
		自定义装饰器
	- CustomizeEnumeration/
		枚举文件集合
	- CustomizeMiddleware/
		自定义中间键
	- FilterForModel/
		模型搜索
	- FormsForApp/
		自定义表单
	- FunctionsForBase/
		基础方法封装
	- FunctionsForModels/
		模型操作方法封装
	- migrations/
		数据库迁移脚本
	- PageForApp/
		页面视图
	- RestFulForApp/
		接口视图
	- SerializersForModel/
		模型序列化
	- SerializerType/
		自定义序列化中特殊字段的处理
	- templatetags/
		前端模版中的过滤器
	- UrlsForApp/
		模块中的路由配置（按模块划分）
	- apps.py
		app配置
	- models.py
		数据库模型
	- tests.py
		测试脚本
	- views.py
		页面脚本
- MagicbeanPlatform/
平台项目配置目录
	- setting.py
	项目配置
	- urls.py
	路由配置
	- wsgi.py
	web服务配置
- AutoText/
自动化测试代码
	- Common/
		框架级二次封装
	- Config/
		框架级配置
	- InterfaceDocument/
		接口文档解析相关
	- logs/
		自动化测试相关日志
	- ResultBase/
		测试报告基础封装
	- Src/
		执行级
		- common/
			自动化框架二次封装
		- functions/
			常用方法封装
		- runcase/
			执行用例方法封装
		- testcase/
			测试用例方法封装
- common/
平台级基础方法封装
- logs/
平台日志
- static/
静态资源文件存放文件夹
- templates/
模版文件（HTML）存放文件夹
- DependencyPackages.txt
依赖库记录文档
- InitializationSql.sql
初始化sql记录文档
- manage.py
Django项目命令行工具
