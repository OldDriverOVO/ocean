function check_file_name_img(file_name) {
    var suffixIndex = file_name.lastIndexOf(".");
    var suffix = file_name.substring(suffixIndex + 1).toUpperCase();
    return (suffix != "BMP" && suffix != "JPG" && suffix != "JPEG" && suffix != "PNG" && suffix != "GIF");

}


function initPageBar(data) {

    var page_info = $('#page_info');
    page_info.empty();
    var pageinfo = '当前第' + data.current_page + '页 共' + data.pages + '页';
    page_info.append(pageinfo);
    var page_list = $('#page_list');
    page_list.empty();
    var previous = '';
    if (data.has_previous) {
        previous = '<li ><a onclick="getPageInfo(' + (data.current_page - 1) + ')">«</a></li>';
    }
    else {
        previous = '<li class="disabled"><a>«</a></li>';
    }
    page_list.append(previous);

    for (var page in data.pageRange) {
        var onePage = '';
        if (data.pageRange[page] == data.current_page) {
            onePage = '<li class="active"><a >' + data.pageRange[page] + '</a></li>';
        }
        else {
            onePage = '<li ><a onclick="getPageInfo(' + data.pageRange[page] + ')">' + data.pageRange[page] + '</a></li>';
        }
        page_list.append(onePage);
    }
    var next = '';
    if (data.has_next) {
        next = '<li><a onclick="getPageInfo(' + (data.current_page + 1) + ')">»</a></li>';
    }
    else {
        next = '<li class="disabled"><a>»</a></li>';
    }
    page_list.append(next);

}
