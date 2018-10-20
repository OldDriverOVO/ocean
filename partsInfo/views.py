from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Parts,Factory,Customer
import win32timezone
import json
from django.core import serializers
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your partinfo here.

def index(request):

    return render(request, 'partinfo/index.html')

def parts_list(request):

    # for i in range(31,150):
    #     new = Parts(oem='909612'+str(i),cn_name='测试数据'+str(i),en_name='Test Data',last_change_date=win32timezone.now(),last_change_user_id=1)
    #     new.save()
    #     pass
    if request.is_ajax():

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
              'parts_list':json.loads(serializers.serialize('json',contacts.object_list)),
              'page_info':{
                  'current_page': contacts.number,
                  'has_next': contacts.has_next(),
                  'has_previous': contacts.has_previous(),
                  'pageRange': list(pageRange),
                  'pages': contacts.paginator.num_pages
              },

             },safe=False

        )


    return render(request, 'partinfo/parts_list.html')

def add_parts_info(request):

    if request.is_ajax():
        state = None

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
                    last_change_user_id=1,
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

    return render(request, 'partinfo/factory_list.html')



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
                    last_change_user_id=1

                )
                new.save()
                state = 'success'
                return HttpResponse(state)

        except:
            state="error"
            return HttpResponse(state)

    else:
        return HttpResponse("")

def customer_list(request):

    if request.is_ajax():

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

    return render(request,'partinfo/customer_list.html')


def add_customer_info(request):
    if request.is_ajax():
        print(request.POST)
        return HttpResponse('')
    else:
        return HttpResponse('')



    return HttpResponse("")
