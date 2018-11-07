from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import VolumeWeightData, Parts, Factory, Customer, FactoryPartsPrice, CustomerPartsPrice
import win32timezone
import json
from django.urls import reverse
from django.contrib import auth
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from partsInfo.sql_utils import SqlUtils
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q


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
    if request.is_ajax():
        if request.GET.get('q') != '':
            contact_list = Parts.objects.filter(
                Q(oem__icontains=request.GET.get('q')) |
                Q(cn_name__icontains=request.GET.get('q')) |
                Q(en_name__icontains=request.GET.get('q')) |
                Q(car_model__icontains=request.GET.get('q'))
            )
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
    # for i in range(31, 1500):
    #     new = Parts(oem='909612' + str(i), cn_name='测试数据' + str(i), en_name='Test Data',car_model='MATIZ',
    #                 last_change_date=win32timezone.now(), last_change_user_id=1)
    #     new.save()
    #     pass
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
                    car_model=request.POST.get('txt_car_model')

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
def delete_parts_info(request):
    if request.is_ajax():
        targat = Parts.objects.filter(oem=request.POST.get('oem')).first()
        if targat:
            targat.delete()
            return HttpResponse('success')
        else:
            return HttpResponse("object_not_found")
    else:

        return HttpResponseRedirect(reverse('partsinfo:part_list'))


@login_required
def update_parts_info(request):
    if request.is_ajax():
        try:
            target = Parts.objects.get(oem=request.POST.get("txt_OEM"))
            if target:
                target.cn_name = request.POST.get('txt_cn_name')
                target.en_name = request.POST.get('txt_en_name')
                target.car_model = request.POST.get('txt_car_model')
                target.description = request.POST.get('txt_area_desc')
                target.last_change_user_id = request.user.id
                if request.POST.get('file_img') != "" or request.POST.get('chb_delete_img'):
                    target.img.delete(False)
                    target.img = request.FILES.get('file_img')

                target.save()

                return HttpResponse('success')
            else:
                return HttpResponse("object_not_found")
        except:
            return HttpResponse("data_error")
    else:
        return render(request, 'partinfo/parts_list.html')


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

        if request.GET.get('q') != '':
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
def delete_factory_info(request):
    if request.is_ajax():
        targat = Factory.objects.filter(id=request.POST.get('id')).first()
        if targat:
            targat.delete()
            return HttpResponse('success')
        else:
            return HttpResponse("object_not_found")
    else:

        return HttpResponseRedirect(reverse('partsinfo:factory_list'))


@login_required
def update_factory_info(request):
    if request.is_ajax():

        info_exist = Factory.objects.filter(name=request.POST.get("txt_factory_name")).first()

        if info_exist:

            if info_exist.id != int(request.POST.get('id')):
                return HttpResponse('info_exist')

        try:
            target = Factory.objects.get(id=request.POST.get('id'))

            target.name = request.POST.get("txt_factory_name")
            target.Contact = request.POST.get("txt_factory_contact")
            target.phone_num = request.POST.get("txt_factory_phone_num")
            target.qq = request.POST.get("txt_factory_qq")
            target.address = request.POST.get("txt_factory_address")
            target.description = request.POST.get("txt_area_factory_desc")
            target.last_change_user_id = request.user.id
            target.save()
            return HttpResponse('success')
        except:
            return HttpResponse("data_error")

    else:
        return render(request, 'partinfo/factory_list.html')


@login_required
def customer_list(request):
    if request.is_ajax():

        if request.GET.get('q') != '':
            contact_list = Customer.objects.filter(
                Q(nick_name__icontains=request.GET.get('q')) | Q(name__icontains=request.GET.get('q')))
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
def delete_customer_info(request):
    if request.is_ajax():
        targat = Customer.objects.filter(id=request.POST.get('id')).first()
        if targat:
            targat.delete()
            return HttpResponse('success')
        else:
            return HttpResponse("object_not_found")
    else:

        return HttpResponseRedirect(reverse('partsinfo:customer_list'))


@login_required
def update_customer_info(request):
    if request.is_ajax():

        info_exist = Customer.objects.filter(name=request.POST.get("txt_customer_nick_name")).first()

        if info_exist:

            if info_exist.id != int(request.POST.get('id')):
                return HttpResponse('info_exist')

        try:
            target = Customer.objects.get(id=request.POST.get('id'))

            target.name = request.POST.get("txt_customer_name")
            target.nick_name = request.POST.get("txt_customer_nick_name")
            target.description = request.POST.get("txt_area_customer_desc")
            if request.POST.get('file_customer_icon') != "" or request.POST.get('chb_delete_img'):
                target.icon_img.delete(False)
                target.icon_img = request.FILES.get("file_customer_icon")
            target.last_change_user_id = request.user.id
            target.save()
            return HttpResponse('success')
        except:
            return HttpResponse("data_error")

    else:
        return render(request, 'partinfo/customer_list.html')


@login_required
# @permission_required(perm='partsInfo.view_factorypartsprice')
def factory_price_list(request):
    if request.is_ajax():

        contact_list = SqlUtils.get_factory_parts_price(oem=request.GET.get("oem"),
                                                        factory_id=request.GET.get('factory_id'),
                                                        factory_q=request.GET.get('factory_q') if request.GET.get(
                                                            'factory_q') != '' else None,
                                                        parts_q=request.GET.get('parts_q') if request.GET.get(
                                                            'parts_q') != '' else None
                                                        )

        paginator = Paginator(contact_list, 13)

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

        contact_list = SqlUtils.get_customer_parts_price(oem=request.GET.get('oem'),
                                                         customer_id=request.GET.get('customer_id'),
                                                         customer_q=request.GET.get('customer_q') if request.GET.get(
                                                             'customer_q') != '' else None,
                                                         parts_q=request.GET.get('parts_q') if request.GET.get(
                                                             'parts_q') != '' else None
                                                         )

        paginator = Paginator(contact_list, 13)  # Show 25 contacts per page

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
    target = Factory.objects.filter(id=pk).first()
    if target:
        return render(request, 'partinfo/factory_detail.html', context={'user': request.user,
                                                                        'factory': target
                                                                        })
    else:
        return HttpResponseRedirect(reverse("partsinfo:factory_list"))


@login_required
def customer_detail(request, pk):
    target = Customer.objects.filter(id=pk).first()
    if target:
        return render(request, 'partinfo/customer_detail.html', context={'user': request.user,
                                                                         'customer': target
                                                                         })
    else:
        return HttpResponseRedirect(reverse("partsinfo:customer_list"))


@login_required
def volume_data(request):
    if request.is_ajax():
        if request.GET.get('q'):
            contact_list = VolumeWeightData.objects.filter(oem__oem__icontains=request.GET.get('q')).order_by(
                '-last_change_date')
        else:
            contact_list = VolumeWeightData.objects.all().order_by('-last_change_date')

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
                'volume_data': json.loads(serializers.serialize('json', contacts.object_list)),
                'page_info': {
                    'current_page': contacts.number,
                    'has_next': contacts.has_next(),
                    'has_previous': contacts.has_previous(),
                    'pageRange': list(pageRange),
                    'pages': contacts.paginator.num_pages
                },

            }, safe=False

        )

    return render(request, 'partinfo/volume_data.html')


@login_required
def add_volume_data(request):
    if request.is_ajax():
        if VolumeWeightData.objects.filter(oem=request.POST.get("select_parts")):
            return HttpResponse("info_exist")
        part = Parts.objects.get(oem=request.POST.get("select_parts"))

        new = VolumeWeightData(
            oem=part,
            length=request.POST.get("length") if request.POST.get("length")!='' else 0,
            width=request.POST.get("width") if request.POST.get("width")!='' else 0,
            height=request.POST.get("height") if request.POST.get("height")!='' else 0,
            net_weight=request.POST.get("net_weight") if request.POST.get("net_weight")!='' else 0,
            gross_weight=request.POST.get("gross_weight") if request.POST.get("gross_weight")!='' else 0,
            description=request.POST.get("desc"),
            last_change_user_id=request.user.id,

        )
        new.save()
        return HttpResponse('success')
    else:
        return HttpResponse("")


@login_required
def delete_volume_data(request):
    if request.is_ajax():
        try:
            target = VolumeWeightData.objects.get(id=request.POST.get("id"))
            target.delete()
            return HttpResponse('success')
        except:
            return HttpResponse('object_not_found')

    else:
        return HttpResponse("")


@login_required
def update_volume_data(request):
    state = None
    if request.is_ajax():
        target = VolumeWeightData.objects.get(id=request.POST.get("id"))
        if target:
            try:
                target.height = request.POST.get('height')
                target.width = request.POST.get('width')
                target.length = request.POST.get('length')
                target.net_weight = request.POST.get('net_weight')
                target.gross_weight = request.POST.get('gross_weight')
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
