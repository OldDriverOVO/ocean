$(document).ready(function () {
    $("#btn_factory_price_save").click(function () {

        var select_parts = $("#select_parts");
        if (select_parts.val() == "") {
            select_parts.parent().addClass("has-error");
            toastr.error('选择产品');
            return;
        }
        var select_factory = $("#select_factory");
        if (select_factory.val() == '') {
            select_factory.parent().addClass("has-error")
            toastr.error('选择工厂');
            return;
        }
        var num_factory_price = $("#num_factory_price");

        if (num_factory_price.val() == '' || num_factory_price.val() < 0) {
            num_factory_price.parent().addClass("has-error")
            toastr.error('价格不能为零或者小于零');
            return;
        }

        var add_factory_price_form = new FormData($("#add_factory_price_form")[0])

        $.ajax({
            type: "POST",
            url: "/baseinfo/add_factory_price/",
            data: add_factory_price_form,
            async: false,
            contentType: false,
            processData: false,
            success: function (data) {


                if (data == "success") {
                    $('#model_factory_price_add').modal('hide');
                    toastr.success('添加成功！2333');
                    getFactoryPriceInfo(1);

                } else if (data == 'info_exist') {

                    toastr.error('信息重复');

                }
                else if (data == "data_error") {
                    toastr.error('数据库错误');
                }
                else {
                    toastr.error('没有权限');
                }

            }

        });


    });

    $('#model_factory_price_add').on('hide.bs.modal', function () {

        $("#select_parts").val(null).trigger('change');
        $("#select_factory").val(null).trigger('change');
        $("#add_factory_price_form")[0].reset();

        var select_parts = $("#select_parts");
        if (select_parts.parent().hasClass("has-error")) {
            select_parts.parent().removeClass("has-error");

        }


        var select_factory = $("#select_factory");
        if (select_factory.parent().hasClass("has-error")) {
            select_factory.parent().removeClass("has-error");

        }
        var num_factory_price = $("#num_factory_price");
        if (num_factory_price.parent().hasClass("has-error")) {
            num_factory_price.parent().removeClass("has-error");

        }

    });

    $("#btn_customer_price_save").click(function () {

        var select_parts = $("#select_parts");
        if (select_parts.val() == "") {
            select_parts.parent().addClass("has-error");
            toastr.error('选择产品');
            return;
        }
        var select_customer = $("#select_customer");
        if (select_customer.val() == '') {
            select_customer.parent().addClass("has-error")
            toastr.error('选择工厂');
            return;
        }
        var num_customer_price = $("#num_price");

        if (num_customer_price.val() == '' || num_customer_price.val() < 0) {
            num_customer_price.parent().addClass("has-error")
            toastr.error('价格不能为零或者小于零');
            return;
        }

        var add_customer_price_form = new FormData($("#add_customer_price_form")[0])

        $.ajax({
            type: "POST",
            url: "/baseinfo/add_customer_price/",
            data: add_customer_price_form,
            async: false,
            contentType: false,
            processData: false,
            success: function (data) {


                if (data == "success") {
                    $('#model_customer_price_add').modal('hide');
                    toastr.success('添加成功！2333');
                    getCustomerPriceInfo(1);

                } else if (data == 'info_exist') {

                    toastr.error('信息重复');

                }
                else if (data == "data_error") {
                    toastr.error('数据库错误');
                }
                else {
                    toastr.error('没有权限');
                }

            }

        });


    });

    $('#model_customer_price_add').on('hide.bs.modal', function () {

        $("#select_parts").val(null).trigger('change');
        $("#select_customer").val(null).trigger('change');
        $("#add_customer_price_form")[0].reset();

        var select_parts = $("#select_parts");
        if (select_parts.parent().hasClass("has-error")) {
            select_parts.parent().removeClass("has-error");

        }


        var select_customer = $("#select_customer");
        if (select_customer.parent().hasClass("has-error")) {
            select_customer.parent().removeClass("has-error");

        }
        var num_customer_price = $("#num_price");
        if (num_customer_price.parent().hasClass("has-error")) {
            num_customer_price.parent().removeClass("has-error");

        }

    });


    $('#customer_price_list').delegate('.customer_price_delete', 'click', function () {
        deleteCustomerPriceInfo($(this).parent().find('input').val());
    });

    $('#customer_price_list').delegate('.customer_price_update', 'click', function () {
        var td = $(this).parents('.price_td');
        var price = td.prev().text();
        var desc = td.next().text();
        var id = td.find('input').val();
        updateCustomerPriceInfo(id, price, desc);

    });

    $('#factory_price_list').delegate('.factory_price_delete', 'click', function () {
        deleteFactoryPriceInfo($(this).parent().find('input').val());
    });

    $('#factory_price_list').delegate('.factory_price_update', 'click', function () {
        var td = $(this).parents('.price_td');
        var price = td.prev().text();
        var desc = td.next().text();
        var id = td.find('input').val();
        updateFactoryPriceInfo(id, price, desc);

    });

})

function check_file_name_img(file_name) {
    var suffixIndex = file_name.lastIndexOf(".");
    var suffix = file_name.substring(suffixIndex + 1).toUpperCase();
    return (suffix != "BMP" && suffix != "JPG" && suffix != "JPEG" && suffix != "PNG" && suffix != "GIF");

}

function initPageBar(data, page_bar_id, initPageFunc) {

    if (data.pageRange.length == 1) {
        return;
    }

    var page_info = $('#' + page_bar_id).find("#page_info");
    page_info.empty();
    var pageinfo = '当前第' + data.current_page + '页 共' + data.pages + '页';
    page_info.append(pageinfo);
    var page_list = $('#' + page_bar_id).find("#page_list");
    ;
    page_list.empty();
    var previous = '';
    if (data.has_previous) {
        previous = '<li ><a onclick="' + initPageFunc + '(' + (data.current_page - 1) + ')">«</a></li>';
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
            onePage = '<li ><a onclick="' + initPageFunc + '(' + data.pageRange[page] + ')">' + data.pageRange[page] + '</a></li>';
        }
        page_list.append(onePage);
    }
    var next = '';
    if (data.has_next) {
        next = '<li><a onclick="' + initPageFunc + '(' + (data.current_page + 1) + ')">»</a></li>';
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
        backgroundDismiss: true,
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
        backgroundDismiss: true,
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
            cancel: {
                text: '取消',

            },
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
        backgroundDismiss: true,
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
        backgroundDismiss: true,
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
            cancel: {
                text: '取消',

            },
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

        },

    });
}