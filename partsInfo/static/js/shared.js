function check_file_name_img(file_name) {
    var suffixIndex = file_name.lastIndexOf(".");
    var suffix = file_name.substring(suffixIndex + 1).toUpperCase();
    return (suffix != "BMP" && suffix != "JPG" && suffix != "JPEG" && suffix != "PNG" && suffix != "GIF");

}


function initPageBar(data,page_bar_id) {

    if (data.pageRange.length == 1){
        return;
    }

    var page_info = $('#'+page_bar_id).find("#page_info");
    page_info.empty();
    var pageinfo = '当前第' + data.current_page + '页 共' + data.pages + '页';
    page_info.append(pageinfo);
    var page_list =  $('#'+page_bar_id).find("#page_list");;
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

function deleteFactoryPriceInfo(id) {
    $.confirm({
        title: '提示',
        content: '确定删除？',
        animation: 'top',
        closeAnimation: 'top',
        animateFromElement: false,
        buttons: {
            cancel: {
                text: '取消',
            },
            confirm: {
                text: '删除',
                btnClass: 'btn-danger',
                action: function () {
                    $.ajax({
                        type: "POST",
                        headers: {"X-CSRFtoken": $.cookie('csrftoken')},
                        url: "/baseinfo/delete_factory_price/",
                        data: {'id': id},

                        success: function (data) {


                            if (data == "success") {

                                toastr.success('删除成功！2333');
                                getFactoryPriceInfo(1);
                            }
                            else if (data == "object_not_found") {

                                toastr.error('失败 没有找到删除对象');
                            }
                            else {
                                toastr.error('没有权限');
                            }

                        }

                    });
                }
            }

        }
    });


}

function updateFactoryPriceInfo(id, price, desc) {

    $.confirm({
        title: '修改',
        animation: 'top',
        closeAnimation: 'top',
        animateFromElement: false,
        content: '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        '<label>价格</label>' +
        '<input type="number" min="0.0" step="0.1" value="' + price + '" name="txt_price" id="txt_price"  class="name form-control" required />' +
        '<label>备注</label>' +
        '<textarea class="form-control" rows="4" name="txt_area_desc" id="txt_area_desc" > ' + desc + '\n' +
        '</textarea>' +
        '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: '保存',
                btnClass: 'btn-blue',
                action: function () {
                    var new_price = this.$content.find('#txt_price').val();
                    var new_desc = this.$content.find('#txt_area_desc').val();

                    $.ajax({
                        type: "POST",
                        headers: {"X-CSRFtoken": $.cookie('csrftoken')},
                        url: "/baseinfo/update_factory_price/",

                        data: {
                            'id': id,
                            'price': new_price,
                            'desc': new_desc,
                        },

                        success: function (data) {


                            if (data == "success") {

                                toastr.success('修改成功');
                                getFactoryPriceInfo(1);
                            }
                            else if (data == "object_not_found") {

                                toastr.error('修改失败 没有找到修改对象');
                            }
                            else if (data == "data_error") {
                                toastr.error('数据库错误');
                            }
                            else {
                                toastr.error('没有权限');
                            }

                        }

                    });


                }

            },
            cancel: {
                text: '取消',

            },
        },

    });
}

function deleteCustomerPriceInfo(id) {
    $.confirm({
        title: '提示',
        content: '确定删除？',
        animation: 'top',
        closeAnimation: 'top',
        animateFromElement: false,
        buttons: {
            cancel: {
                text: '取消',
            },
            confirm: {
                text: '删除',
                btnClass: 'btn-danger',
                action: function () {
                    $.ajax({
                        type: "POST",
                        headers: {"X-CSRFtoken": $.cookie('csrftoken')},
                        url: "/baseinfo/delete_customer_price/",
                        data: {'id': id},

                        success: function (data) {


                            if (data == "success") {

                                toastr.success('删除成功！2333');
                                getCustomerPriceInfo(1);
                            }
                            else if (data == "object_not_found") {

                                toastr.error('失败 没有找到删除对象');
                            }
                            else {
                                toastr.error('没有权限');
                            }

                        }

                    });
                }
            }

        }
    });


}

function updateCustomerPriceInfo(id, price, desc) {

    $.confirm({
        title: '修改',
        animation: 'top',
        closeAnimation: 'top',
        animateFromElement: false,
        content: '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        '<label>价格</label>' +
        '<input type="number" min="0.0" step="0.1" value="' + price + '" name="txt_price" id="txt_price"  class="name form-control" required />' +
        '<label>备注</label>' +
        '<textarea class="form-control" rows="4" name="txt_area_desc" id="txt_area_desc" > ' + desc + '\n' +
        '</textarea>' +
        '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: '保存',
                btnClass: 'btn-blue',
                action: function () {
                    var new_price = this.$content.find('#txt_price').val();
                    var new_desc = this.$content.find('#txt_area_desc').val();

                    $.ajax({
                        type: "POST",
                        headers: {"X-CSRFtoken": $.cookie('csrftoken')},
                        url: "/baseinfo/update_customer_price/",
                        data: {
                            'id': id,
                            'price': new_price,
                            'desc': new_desc,
                        },

                        success: function (data) {


                            if (data == "success") {

                                toastr.success('修改成功');
                                getCustomerPriceInfo(1);
                            }
                            else if (data == "object_not_found") {

                                toastr.error('修改失败 没有找到修改对象');
                            }
                            else if (data == "data_error") {
                                toastr.error('数据库错误');
                            }
                            else {
                                toastr.error('没有权限');
                            }

                        }

                    });


                }

            },
            cancel: {
                text: '取消',

            },
        },

    });
}