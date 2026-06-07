"""Shop URL patterns (includes regex routes)."""

from django.urls import path, re_path

from shop import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.news_list, name='news'),
    path('faq/', views.faq_list, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('reviews/', views.reviews_list, name='reviews'),
    path('reviews/add/', views.review_create, name='review_add'),
    path('promos/', views.promos, name='promos'),
    path('categories/', views.category_list, name='categories'),
    path('products/', views.product_list, name='product_list'),
    path('statistics/', views.statistics_page, name='statistics'),
    path('login/', views.ShopLoginView.as_view(), name='login'),
    path('logout/', views.ShopLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('pickup/', views.pickup_points, name='pickup_points'),
    path('history/', views.purchase_history, name='purchase_history'),
    path('my-promos/', views.my_promos, name='my_promos'),
    path('checkout/', views.checkout, name='checkout'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    re_path(r'^products/(?P<pk>\d+)/edit/$', views.ProductUpdateView.as_view(), name='product_edit'),
    re_path(r'^products/(?P<pk>\d+)/delete/$', views.ProductDeleteView.as_view(), name='product_delete'),
    re_path(r'^products/new/$', views.ProductCreateView.as_view(), name='product_create'),
    re_path(r'^orders/(?P<pk>\d+)/edit/$', views.OrderUpdateView.as_view(), name='order_edit'),
    re_path(r'^orders/(?P<pk>\d+)/delete/$', views.OrderDeleteView.as_view(), name='order_delete'),
    re_path(r'^orders/new/$', views.OrderCreateView.as_view(), name='order_create'),
    re_path(r'^catalog/category-(?P<slug>[\w-]+)/$', views.category_list, name='category_by_slug'),
]
