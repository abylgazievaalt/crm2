from django.contrib import admin
from django.conf.urls import url, include
from api import views
#from .views import CreateUserAPIView, UserRetrieveUpdateAPIView
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
               url(r'^department/$', views.DepartmentList.as_view(),name='department'),
               url(r'^department/(?P<pk>[0-9]+)/$', views.DepartmentDetail.as_view()),
               url(r'^servicepercentage/(?P<pk>[0-9]+)/$', views.ServicePercentageDetail.as_view()),
               url(r'^servicepercentage/$', views.ServicePercentageList.as_view(), name='servicepercentage'),
               url(r'^meal/$', views.MealList.as_view(),name='meal'),
               url(r'^meal/(?P<pk>[0-9]+)/$', views.MealDetail.as_view()),
               url(r'^check/$', views.CheckList.as_view(),name='check'),
               url(r'^check/(?P<pk>[0-9]+)/$', views.CheckDetail.as_view()),
               url(r'^order/$', views.OrderList.as_view(),name='order'),
               url(r'^order/(?P<pk>[0-9]+)/$', views.OrderDetail.as_view()),
               url(r'^order/active/$', views.ActiveOrdersList.as_view()),
               url(r'^status/$', views.StatusList.as_view(),name='status'),
               url(r'^status/(?P<pk>[0-9]+)/$', views.StatusDetail.as_view()),
               url(r'^role/$', views.RoleList.as_view(),name='role'),
               url(r'^role/(?P<pk>[0-9]+)/$', views.RoleDetail.as_view()),
               url(r'^table/$', views.TableList.as_view(),name='table'),
               url(r'^table/(?P<pk>[0-9]+)/$', views.TableDetail.as_view()),
               url(r'^category/$', views.CategoryList.as_view(),name='category'),
               url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryDetail.as_view()),
               url(r'^api-auth/', include('rest_framework.urls')),
               url(r'^signup/$', views.RegistrationAPIView.as_view()),
               url(r'^login/$', views.LoginAPIView.as_view()),
               url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
               url(r'^user/$', views.UserListAPIView.as_view(), name='user'),
               ]
