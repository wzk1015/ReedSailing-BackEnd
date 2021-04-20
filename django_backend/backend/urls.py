"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BUAA.views import *
from BUAA.superUser import *
from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户端
    path('sendVerify/', send_email),
    path('verify/', verify_email),
    path('login/', code2Session),
    path('adminLogIn/', login),
    path('register/', register),

    # 自动生成接口文档
    url(r'^docs/', include_docs_urls(title='一苇以航API接口')),

    # 版块
    url(r'^blocks/$', BlockViewSet.as_view({"get": "list", "post": "create"})),
    url(r'^blocks/(?P<pk>\d+)/$', BlockViewSet.as_view({"put": "update", "delete": "destroy"})),

    # 用户
    url(r'^users/$', WXUserViewSet.as_view({"get": "list"})),
    url(r'^users/(?P<pk>\d+)/$', WXUserViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update"})),

    # 组织申请
    url(r'^organizations/applications/$', OrgApplicationViewSet.as_view({"post": "create", "get": "list"})),
    url(r'^organizations/applications/(?P<pk>\d+)/$', OrgApplicationViewSet.as_view({"delete": "destroy"})),
    url(r'^users/organizations/applications/(?P<user_id>\d+)/$', OrgApplicationViewSet.as_view({"get": "user_get_all"})),
    url(r'^organizations/applications/verifications/(?P<pk>\d+)/$', OrgApplicationViewSet.as_view({"put": "verify"})),

    # 组织
    url(r'^organizations/$', OrganizationModelViewSet.as_view({"post": "create"})),
    url(r'^organizations/(?P<pk>\d+)/$', OrganizationModelViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    url(r'^blocks/organizations/(?P<block_id>\d+)/$', OrganizationModelViewSet.as_view({"get": "get_org_by_block"})),
    url(r'^organizations/owner/(?P<pk>\d+)/$', OrganizationModelViewSet.as_view({"post": "change_org_owner"})),

    # 关注组织
    url(r'^users/followed_organizations/$', FollowedOrgViewSet.as_view({"post": "create", "delete": "destroy"})),
    url(r'^users/followed_organizations/(?P<pk>\d+)/$', FollowedOrgViewSet.as_view({"get": "get_followed_org"})),

    # 组织管理
    url(r'^organizations/managers/$', OrgManageViewSet.as_view({"post": "create", "delete": "destroy", })),
    url(r'^organizations/managers/(?P<pk>\d+)/$', OrgManageViewSet.as_view({"get": "get_all_managers"})),
    url(r'^users/managed_organizations/(?P<pk>\d+)/$', OrgManageViewSet.as_view({"get": "get_managed_org"})),

    # 活动分类
    url(r'^activities/categories/$', CategoryViewSet.as_view({"get": "list", "post": "create"})),
    url(r'^activities/categories/(?P<pk>\d+)/$', CategoryViewSet.as_view({"put": "update", "delete": "destroy"})),

    # 活动地址
    url(r'^activities/addresses/$', AddressViewSet.as_view({"get": "list", "post": "create"})),
    url(r'^activities/addresses/(?P<pk>\d+)/$', AddressViewSet.as_view({"delete": "destroy"})),

    # 用户反馈
    url(r'^feedbacks/$', UserFeedbackViewSet.as_view({"get": "list", "post": "create"})),
    url(r'^feedbacks/(?P<pk>\d+)/$', UserFeedbackViewSet.as_view({"delete": "destroy"})),

    # 活动
    url(r'^activities/$', ActivityViewSet.as_view({"post": "create", "get": "list"})),
    url(r'^activities/(?P<pk>\d+)/$', ActivityViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update"})),
    url(r'^organizations/activities/(?P<org_id>\d+)/$', ActivityViewSet.as_view({"get": "get_org_act"})),
    url(r'^users/released_activities/(?P<user_id>\d+)/$', ActivityViewSet.as_view({"get": "get_user_act"})),
    url(r'^blocks/activities/(?P<block_id>\d+)/$', ActivityViewSet.as_view({"get": "get_block_act"})),

    # 活动参与
    url(r'activities/participants/$', JoinedActViewSet.as_view({"post": "create"})),
    url(r'activities/participants/(?P<pk>\d+)/$', JoinedActViewSet.as_view({"delete": "destroy"})),
    url(r'user/joined_act/(?P<user_id>\d+)/$', JoinedActViewSet.as_view({"get": "get_user_joined_act"})),
    url(r'activities/joined_number/(?P<act_id>\d+)', JoinedActViewSet.as_view({"get": "get_act_participants_number"})),

    # 测试使用
    url(r'^test/users/$', WXUserViewSet.as_view({"post": "create"})),


]

router = SimpleRouter()
router.register('comments', CommentViewSet)
router.register('activities/join_applications', JoinActApplicationViewSet)
urlpatterns += router.urls



