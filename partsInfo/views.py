from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Parts, Factory, Customer, FactoryPartsPrice, CustomerPartsPrice
import win32timezone
import json
from django.urls import reverse
from django.contrib import auth
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from partsInfo.sql_utils import SqlUtils
from django.contrib.auth.decorators import login_required, permission_required


# Create your partinfo here.

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('partsinfo:index'))

    state = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('partsinfo:index'))
        else:
            state = '账号或密码错误！'

    return render(request, 'partinfo/login.html', context={'state': state})


def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(reverse('partsinfo:login'))


@login_required
def index(request):
    return render(request, 'partinfo/index.html', context={'user': request.user})


@login_required
def parts_list(request):
    # for i in range(31,150):
    #     new = Parts(oem='909612'+str(i),cn_name='测试数据'+str(i),en_name='Test Data',last_change_date=win32timezone.now(),last_change_user_id=1)
    #     new.save()
    #     pass
    if request.is_ajax():
        if request.GET.get('q'):
            contact_list = Parts.objects.filter(oem__icontains=request.GET.get('q'))
        else:
            contact_list = Parts.objects.all().order_by('-last_change_date')

        paginator = Paginator(contact_list, 40)  # Show 25 contacts per page

        try:
            currentPage = int(request.GET.get('page'))
            contacts = paginator.page(currentPage)
            if paginator.num_pages > 10:
                if currentPage - 5 < 1:
                    pageRange = range(1, 11)
                elif currentPage + 5 > paginator.num_pages:
                    pageRange = range(currentPage - 5, paginator.num_pages + 1)

                else:
                    pageRange = range(currentPage - 5, currentPage + 5)

            else:
                pageRange = paginator.page_range

        except ValueError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except TypeError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            pageRange = paginator.page_range

        return JsonResponse(
            {
                'parts_list': json.loads(serializers.serialize('json', contacts.object_list)),
                'page_info': {
                    'current_page': contacts.number,
                    'has_next': contacts.has_next(),
                    'has_previous': contacts.has_previous(),
                    'pageRange': list(pageRange),
                    'pages': contacts.paginator.num_pages
                },

            }, safe=False

        )

    return render(request, 'partinfo/parts_list.html', context={'user': request.user})


@login_required
def add_parts_info(request):
    if request.is_ajax():
        state = None
        user = request.user
        try:
            if (Parts.objects.filter(oem=request.POST.get("txt_OEM"))):
                state = 'info_exist'
                return HttpResponse(state)

            else:
                new_parts = Parts(
                    oem=request.POST.get("txt_OEM"),
                    cn_name=request.POST.get("txt_cn_name"),
                    en_name=request.POST.get("txt_en_name"),
                    description=request.POST.get("txt_area_desc"),
                    img=request.FILES.get("file_img"),
                    last_change_date=win32timezone.now(),
                    last_change_user_id=user.id,
                    car_model_id=1

                )
                new_parts.save()
                state = 'success'
                return HttpResponse(state)

        except:
            state = 'error'
            return HttpResponse(state)

    else:
        return HttpResponse("")


@login_required
def factory_list(request):
    # for i in range(21,100):
    #     new = Factory(name='测试数据'+str(i),
    #                   Contact='曾大姐',
    #                   phone_num='135-5154-3621',
    #                   address='浙江省宁波市奉化区云峰路36号',
    #                   qq='909614012',
    #                   last_change_user_id=1,
    #                   last_change_date=win32timezone.now())
    #     new.save()
    if request.is_ajax():

        if request.GET.get('q'):
            contact_list = Factory.objects.filter(name__icontains=request.GET.get('q')).order_by('-last_change_date')
        else:
            contact_list = Factory.objects.all().order_by('-last_change_date')

        paginator = Paginator(contact_list, 40)  # Show 25 contacts per page

        try:
            currentPage = int(request.GET.get('page'))
            contacts = paginator.page(currentPage)
            if paginator.num_pages > 10:
                if currentPage - 5 < 1:
                    pageRange = range(1, 11)
                elif currentPage + 5 > paginator.num_pages:
                    pageRange = range(currentPage - 5, paginator.num_pages + 1)

                else:
                    pageRange = range(currentPage - 5, currentPage + 5)

            else:
                pageRange = paginator.page_range

        except ValueError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except TypeError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            pageRange = paginator.page_range

        return JsonResponse(
            {
                'factory_list': json.loads(serializers.serialize('json', contacts.object_list)),
                'page_info': {
                    'current_page': contacts.number,
                    'has_next': contacts.has_next(),
                    'has_previous': contacts.has_previous(),
                    'pageRange': list(pageRange),
                    'pages': contacts.paginator.num_pages
                },

            }, safe=False

        )

    return render(request, 'partinfo/factory_list.html', context={'user': request.user})


@login_required
def add_factory_info(request):
    if request.is_ajax():
        state = None
        try:
            if Factory.objects.filter(name=request.POST.get('txt_factory_name')):
                state = 'info_exist'
                return HttpResponse(state)
            else:
                new = Factory(
                    name=request.POST.get('txt_factory_name'),
                    Contact=request.POST.get('txt_factory_contact'),
                    qq=request.POST.get('txt_factory_qq'),
                    phone_num=request.POST.get('txt_factory_phone_num'),
                    address=request.POST.get('txt_factory_address'),
                    description=request.POST.get('txt_area_factory_desc'),
                    last_change_date=win32timezone.now(),
                    last_change_user_id=request.user.id

                )
                new.save()
                state = 'success'
                return HttpResponse(state)

        except:
            state = "error"
            return HttpResponse(state)

    else:
        return HttpResponse("")


@login_required
def customer_list(request):
    if request.is_ajax():

        if request.GET.get('q'):
            contact_list = Customer.objects.filter(nick_name__icontains=request.GET.get('q'))
        else:
            contact_list = Customer.objects.all().order_by('-last_change_date')

        paginator = Paginator(contact_list, 40)  # Show 25 contacts per page

        try:
            currentPage = int(request.GET.get('page'))
            contacts = paginator.page(currentPage)
            if paginator.num_pages > 10:
                if currentPage - 5 < 1:
                    pageRange = range(1, 11)
                elif currentPage + 5 > paginator.num_pages:
                    pageRange = range(currentPage - 5, paginator.num_pages + 1)

                else:
                    pageRange = range(currentPage - 5, currentPage + 5)

            else:
                pageRange = paginator.page_range

        except ValueError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except TypeError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            pageRange = paginator.page_range

        return JsonResponse(
            {
                'customer_list': json.loads(serializers.serialize('json', contacts.object_list)),
                'page_info': {
                    'current_page': contacts.number,
                    'has_next': contacts.has_next(),
                    'has_previous': contacts.has_previous(),
                    'pageRange': list(pageRange),
                    'pages': contacts.paginator.num_pages
                },

            }, safe=False

        )

    return render(request, 'partinfo/customer_list.html', context={'user': request.user})


@login_required
def add_customer_info(request):
    if request.is_ajax():

        state = None
        try:
            if Customer.objects.filter(name=request.POST.get('txt_customer_nick_name')):
                state = 'info_exist'
                return HttpResponse(state)
            else:
                new = Customer(
                    name=request.POST.get('txt_customer_name'),
                    nick_name=request.POST.get('txt_customer_nick_name'),
                    icon_img=request.FILES.get('file_customer_icon'),
                    description=request.POST.get('txt_area_customer_desc'),
                    last_change_date=win32timezone.now(),
                    last_change_user_id=request.user.id

                )
                new.save()
                state = 'success'
                return HttpResponse(state)

        except:
            state = "error"
            return HttpResponse(state)
    else:
        return HttpResponse('')


@login_required
# @permission_required(perm='partsInfo.view_factorypartsprice')
def factory_price_list(request):
    if request.is_ajax():

        if request.GET.get("oem"):
            contact_list = SqlUtils.get_factory_parts_price(request.GET.get("oem"))
        else:
            contact_list = SqlUtils.get_factory_parts_price()

        paginator = Paginator(contact_list, 25)  # Show 25 contacts per page

        try:
            currentPage = int(request.GET.get('page'))
            contacts = paginator.page(currentPage)
            if paginator.num_pages > 10:
                if currentPage - 5 < 1:
                    pageRange = range(1, 11)
                elif currentPage + 5 > paginator.num_pages:
                    pageRange = range(currentPage - 5, paginator.num_pages + 1)

                else:
                    pageRange = range(currentPage - 5, currentPage + 5)

            else:
                pageRange = paginator.page_range

        except ValueError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except TypeError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            pageRange = paginator.page_range

        return JsonResponse(
            {
                'factory_price_list': contacts.object_list,
                'page_info': {
                    'current_page': contacts.number,
                    'has_next': contacts.has_next(),
                    'has_previous': contacts.has_previous(),
                    'pageRange': list(pageRange),
                    'pages': contacts.paginator.num_pages
                },

            }, safe=False

        )

    return render(request, 'partinfo/factory_price_list.html', context={'user': request.user})


@login_required
def add_factory_price(request):
    state = None
    if request.is_ajax():
        if FactoryPartsPrice.objects.filter(oem=request.POST.get('select_parts'),
                                            factory_id=request.POST.get('select_factory')):
            state = 'info_exist'
            return HttpResponse(state)
        else:
            try:
                part = Parts.objects.get(oem=request.POST.get('select_parts'))
                factory = Factory.objects.get(id=request.POST.get('select_factory'))
            except:
                state = 'data_error'
                return HttpResponse(state)

            new = FactoryPartsPrice(
                oem=part,
                factory_id=factory,
                price=request.POST.get('num_price'),
                description=request.POST.get('txt_area_factory_price_desc'),
                last_change_user_id=request.user.id
            )
            new.save()
            state = 'success'
            return HttpResponse(state)

    else:
        return HttpResponse("")


@login_required
# @permission_required(perm='partsInfo.delete_factorypartsprice')
def delete_factory_price(request):
    state = None
    if request.is_ajax():
        target = FactoryPartsPrice.objects.filter(id=request.POST.get("id"))
        if target:
            target.delete()
            state = 'success'
            return HttpResponse(state)
        else:
            state = 'object_not_found'
            return HttpResponse(state)

    else:
        return HttpResponse("")


@login_required
# @permission_required(perm='partsInfo.change_factorypartsprice')
def update_factory_price(request):
    state = None
    if request.is_ajax():
        target = FactoryPartsPrice.objects.get(id=request.POST.get("id"))
        if target:
            try:
                target.price = request.POST.get('price')
                target.description = request.POST.get('desc').strip()
                target.last_change_user_id = request.user.id
                target.save()
            except:
                state = 'data_error'
                return HttpResponse(state)

            state = 'success'
            return HttpResponse(state)

        else:
            state = 'object_not_found'
            return HttpResponse(state)

    else:
        return HttpResponse('')


@login_required
# @permission_required(perm='partsInfo.view_factorypartsprice')
def customer_price_list(request):
    if request.is_ajax():

        if request.GET.get("oem"):
            contact_list = SqlUtils.get_customer_parts_price(request.GET.get("oem"))
        else:
            contact_list = SqlUtils.get_customer_parts_price()

        paginator = Paginator(contact_list, 25)  # Show 25 contacts per page

        try:
            currentPage = int(request.GET.get('page'))
            contacts = paginator.page(currentPage)
            if paginator.num_pages > 10:
                if currentPage - 5 < 1:
                    pageRange = range(1, 11)
                elif currentPage + 5 > paginator.num_pages:
                    pageRange = range(currentPage - 5, paginator.num_pages + 1)

                else:
                    pageRange = range(currentPage - 5, currentPage + 5)

            else:
                pageRange = paginator.page_range

        except ValueError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except TypeError:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
            pageRange = paginator.page_range
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
            pageRange = paginator.page_range

        return JsonResponse(
            {
                'customer_price_list': contacts.object_list,
                'page_info': {
                    'current_page': contacts.number,
                    'has_next': contacts.has_next(),
                    'has_previous': contacts.has_previous(),
                    'pageRange': list(pageRange),
                    'pages': contacts.paginator.num_pages
                },

            }, safe=False

        )

    return render(request, 'partinfo/customer_price_list.html', context={'user': request.user})


@login_required
def add_customer_price(request):
    state = None
    if request.is_ajax():

        if CustomerPartsPrice.objects.filter(oem=request.POST.get('select_parts'),
                                             customer_id=request.POST.get('select_customer')):
            state = 'info_exist'
            return HttpResponse(state)
        else:
            try:
                part = Parts.objects.get(oem=request.POST.get('select_parts'))
                customer = Customer.objects.get(id=request.POST.get('select_customer'))
            except:
                state = 'data_error'
                return HttpResponse(state)

            new = CustomerPartsPrice(
                oem=part,
                customer_id=customer,
                price=request.POST.get('num_price'),
                description=request.POST.get('txt_area_customer_price_desc'),
                last_change_user_id=request.user.id
            )
            new.save()
            state = 'success'
            return HttpResponse(state)

    else:
        return HttpResponse("")


@login_required
def update_customer_price(request):
    state = None
    if request.is_ajax():
        target = CustomerPartsPrice.objects.get(id=request.POST.get("id"))
        if target:
            try:
                target.price = request.POST.get('price')
                target.description = request.POST.get('desc').strip()
                target.last_change_user_id = request.user.id
                target.save()
            except:
                state = 'data_error'
                return HttpResponse(state)

            state = 'success'
            return HttpResponse(state)

        else:
            state = 'object_not_found'
            return HttpResponse(state)

    else:
        return HttpResponse('')


@login_required
def delete_customer_price(request):
    state = None
    if request.is_ajax():
        target = CustomerPartsPrice.objects.filter(id=request.POST.get("id"))
        if target:
            target.delete()
            state = 'success'
            return HttpResponse(state)
        else:
            state = 'object_not_found'
            return HttpResponse(state)

    else:
        return HttpResponse("")


@login_required
def part_detail(request, pk):
    target = Parts.objects.get(oem=pk)
    if target:
        return render(request, 'partinfo/part_detail.html', context={'user': request.user,
                                                                     'part': target
                                                                     })
    else:
        return HttpResponseRedirect(reverse("partsinfo:part_list"))

@login_required
def factory_detail(request, pk):
    target = Factory.objects.get(id=pk)
    if target:
        return render(request, 'partinfo/factory_detail.html', context={'user': request.user,
                                                                     'factory': target
                                                                     })
    else:
        return HttpResponseRedirect(reverse("partsinfo:factory_list"))

