from django.shortcuts import render
from django.http import HttpResponse
from .models import Parts
import win32timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your partinfo here.

def index(request):

    return render(request, 'partinfo/index.html')

def parts_list(request):

    # for i in range(31,150):
    #     new = Parts(oem='909612'+str(i),cn_name='测试数据'+str(i),en_name='Test Data',last_change_date=win32timezone.now(),last_change_user_id=1)
    #     new.save()
    #     pass
    contact_list = Parts.objects.all()
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

    return render(request, 'partinfo/parts_list.html', {'contacts': contacts,
                                                        'pageRange':pageRange
                                                        })

