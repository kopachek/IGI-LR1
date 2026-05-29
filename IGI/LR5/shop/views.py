import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from shop.decorators import client_required, employee_required
from shop.forms import (
    CheckoutForm,
    CustomerRegistrationForm,
    OrderCRUDForm,
    ProductCRUDForm,
    ProductFilterForm,
    ReviewForm,
    TimezoneForm,
)
from shop.models import (
    Article,
    ClientProfile,
    CompanyHistory,
    CompanyInfo,
    ContactPerson,
    Coupon,
    EmployeeProfile,
    FAQEntry,
    Order,
    OrderItem,
    PickupPoint,
    Product,
    ProductCategory,
    PromoCode,
    Review,
    Vacancy,
)
from shop.services import fetch_public_holiday
from shop.utils import (
    build_category_chart_base64,
    format_date_dd_mm_yyyy,
    format_datetime_dd_mm_yyyy,
    sales_statistics,
)

logger = logging.getLogger('shop')


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class ShopLoginView(LoginView):
    template_name = 'shop/login.html'


class ShopLogoutView(LogoutView):
    next_page = 'home'


def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info('New customer registered: %s', user.username)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'shop/register.html', {'form': form})


def set_timezone(request):
    if request.method == 'POST':
        form = TimezoneForm(request.POST)
        if form.is_valid():
            request.session['django_timezone'] = form.cleaned_data['timezone']
            messages.info(request, f'Timezone set to {form.cleaned_data["timezone"]}')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def home(request):
    latest = Article.objects.filter(is_published=True).order_by('-published_at').first()
    return render(request, 'shop/home.html', {'latest_article': latest})


def about(request):
    info = CompanyInfo.objects.first()
    history = CompanyHistory.objects.all()
    return render(request, 'shop/about.html', {'info': info, 'history': history})


def news_list(request):
    articles = Article.objects.filter(is_published=True)
    return render(request, 'shop/news.html', {'articles': articles})


def faq_list(request):
    entries = FAQEntry.objects.all()
    return render(
        request,
        'shop/faq.html',
        {
            'entries': entries,
            'dates_local': {e.pk: format_datetime_dd_mm_yyyy(e.created_at) for e in entries},
        },
    )


def contacts(request):
    people = ContactPerson.objects.all()
    return render(request, 'shop/contacts.html', {'people': people})


def privacy(request):
    return render(request, 'shop/privacy.html')


def vacancies(request):
    items = Vacancy.objects.filter(is_open=True)
    return render(request, 'shop/vacancies.html', {'vacancies': items})


def reviews_list(request):
    reviews = Review.objects.all()[:10]
    return render(request, 'shop/reviews.html', {'reviews': reviews})


@login_required
def review_create(request):
    profile = getattr(request.user, 'client_profile', None)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.author_name = request.user.get_full_name() or request.user.username
            review.save()
            logger.info('Review created by %s', request.user)
            messages.success(request, 'Thank you for your review!')
            return redirect('reviews')
    else:
        form = ReviewForm()
    return render(request, 'shop/review_form.html', {'form': form})


def promos(request):
    active = PromoCode.objects.filter(is_active=True)
    archived = PromoCode.objects.filter(is_active=False)
    coupons = Coupon.objects.all()
    return render(
        request,
        'shop/promos.html',
        {'active_promos': active, 'archived_promos': archived, 'coupons': coupons},
    )


def category_list(request):
    categories = ProductCategory.objects.prefetch_related('products')
    return render(request, 'shop/categories.html', {'categories': categories})


def product_list(request):
    form = ProductFilterForm(request.GET or None)
    products = Product.objects.filter(is_available=True).select_related('category', 'manufacturer')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            products = products.filter(
                Q(name__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q)
            )
        min_p = form.cleaned_data.get('min_price')
        max_p = form.cleaned_data.get('max_price')
        if min_p is not None:
            products = products.filter(price__gte=min_p)
        if max_p is not None:
            products = products.filter(price__lte=max_p)
        cat = form.cleaned_data.get('category')
        if cat:
            products = products.filter(category_id=cat)
        sort = form.cleaned_data.get('sort') or 'name'
        products = products.order_by(sort)
    else:
        products = products.order_by('name')

    return render(
        request,
        'shop/products.html',
        {'products': products, 'filter_form': form, 'categories': ProductCategory.objects.all()},
    )


@client_required
def pickup_points(request):
    points = PickupPoint.objects.all()
    return render(request, 'shop/pickup_points.html', {'points': points})


@client_required
def purchase_history(request):
    orders = Order.objects.filter(client=request.user.client_profile).prefetch_related('items__product')
    return render(
        request,
        'shop/purchase_history.html',
        {
            'orders': orders,
            'dates': {o.pk: format_date_dd_mm_yyyy(o.sale_date) for o in orders},
        },
    )


@client_required
def my_promos(request):
    promos_qs = PromoCode.objects.filter(is_active=True)
    return render(request, 'shop/my_promos.html', {'promos': promos_qs})


@client_required
def checkout(request):
    products = Product.objects.filter(is_available=True)
    points = PickupPoint.objects.all()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, pk=form.cleaned_data['product_id'])
            qty = form.cleaned_data['quantity']
            delivery_date = form.cleaned_data['delivery_date']
            client = request.user.client_profile

            holiday = fetch_public_holiday(delivery_date.year, delivery_date.month, delivery_date.day)
            if holiday.get('is_holiday'):
                messages.warning(request, f'Delivery date is a public holiday: {holiday.get("name")}')

            delivery_cost = Decimal('5.00')
            promo = None
            code = form.cleaned_data.get('promo_code')
            if code:
                promo = PromoCode.objects.filter(code__iexact=code, is_active=True).first()

            order = Order.objects.create(
                client=client,
                delivery_date=delivery_date,
                delivery_cost=delivery_cost,
                pickup_point_id=form.cleaned_data.get('pickup_point') or None,
                promo_code=promo,
            )
            line_price = product.price
            if promo:
                line_price = line_price * (100 - promo.discount_percent) / 100
            OrderItem.objects.create(order=order, product=product, quantity=qty, unit_price=line_price)
            order.products.add(product)
            logger.info('Order %s created for %s', order.pk, client)
            messages.success(request, f'Order #{order.pk} placed successfully.')
            return redirect('purchase_history')
    else:
        form = CheckoutForm()
    return render(request, 'shop/checkout.html', {'form': form, 'products': products, 'points': points})


@employee_required
def employee_dashboard(request):
    employee = request.user.employee_profile
    clients = employee.clients.all()
    orders = Order.objects.filter(Q(employee=employee) | Q(client__in=clients)).distinct()
    return render(
        request,
        'shop/employee_dashboard.html',
        {'employee': employee, 'clients': clients, 'orders': orders},
    )


def statistics_page(request):
    stats = sales_statistics()
    chart_category = build_category_chart_base64()
    return render(
        request,
        'shop/statistics.html',
        {
            'stats': stats,
            'chart_category': chart_category
        },
    )


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductCRUDForm
    template_name = 'shop/crud_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Create product'
        return ctx


class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCRUDForm
    template_name = 'shop/crud_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Update product'
        return ctx


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/confirm_delete.html'
    success_url = reverse_lazy('product_list')


class OrderCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Order
    form_class = OrderCRUDForm
    template_name = 'shop/crud_form.html'
    success_url = reverse_lazy('statistics')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Create order'
        return ctx


class OrderUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Order
    form_class = OrderCRUDForm
    template_name = 'shop/crud_form.html'
    success_url = reverse_lazy('statistics')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Update order'
        return ctx


class OrderDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Order
    template_name = 'shop/confirm_delete.html'
    success_url = reverse_lazy('statistics')
