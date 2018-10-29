$(document).ready(function () {
    if ($("#select_parts")[0]) {
        $("#select_parts").select2({
            language: {

                inputTooShort: function () {
                    return "";
                }
            },
            ajax: {
                async: false,
                url: "/baseinfo/part_list/",
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term

                    };
                },
                processResults: function (data) {

                    data.parts_list.forEach(function (value, index) {
                        value["id"] = value["pk"];
                    });

                    return {
                        results: data.parts_list,

                    };
                },
                cache: true
            },
            placeholder: 'Search for a repository',
            escapeMarkup: function (markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 1,
            templateResult: formatParts,
            templateSelection: formatPartsSelection,
            allowClear:true
        });

    }
    if ($("#select_factory")[0] ) {


        $("#select_factory").select2({
            language: {

                inputTooShort: function () {
                    return "";
                }
            },
            ajax: {
                async: false,
                url: "/baseinfo/factory_list",
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term

                    };
                },
                processResults: function (data) {

                    data.factory_list.forEach(function (value) {
                        value["id"] = value["pk"];
                    });

                    return {
                        results: data.factory_list,

                    };
                },
                cache: true
            },
            placeholder: 'Search for a repository',
            escapeMarkup: function (markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 1,
            templateResult: formatFactory,
            templateSelection: formatFactorySelection,
            allowClear:true
        });

    }
    if ($("#select_customer")[0] ) {


        $("#select_customer").select2({
            language: {

                inputTooShort: function () {
                    return "";
                }
            },
            ajax: {
                async: false,
                url: "/baseinfo/customer_list/",
                dataType: 'json',
                delay: 250,
                data: function (params) {
                    return {
                        q: params.term, // search term

                    };
                },
                processResults: function (data) {

                    data.customer_list.forEach(function (value) {
                        value["id"] = value["pk"];
                    });

                    return {
                        results: data.customer_list,

                    };
                },
                cache: true
            },
            placeholder: 'Search for a repository',
            escapeMarkup: function (markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 1,
            templateResult: formatCustomer,
            templateSelection: formatCustomerSelection,
            allowClear:true

        });

    }


})

function formatParts(repo) {
    if (repo.loading) {
        return repo.text;
    }


    var html = ' <div class="select2-result-repository clearfix">\
                               <div class="info-box" style="min-height: 100px;">\
                                     ';
    var html2 = '<a style="color: #444;" ><span class="info-box-icon" style="height: 100px;width: 100px;font-size: 50px;line-height: 0px"><img src="/media/' + repo.fields.img + '" width="100%" height="100%">'
    var img = '<a style="color: #444;"  ><span class="info-box-icon" style="height: 100px;width: 100px;font-size: 50px;line-height: 100px;"><i class="fa fa-file-photo-o"></i>'
    var end = '</a></span>\
                                     <div class="info-box-content" style="margin-left: 100px" >\
                                            <a style="color: #444;" ><span class="info-box-number">' + repo.pk + '</span></a>\
                                            <span class="info-box-text">' + repo.fields.cn_name + '</span>\
                                            <span class="info-box-text">' + repo.fields.en_name + '</span>\
                                          </div>\
                                </div>\
                         </div>';
    if (repo.fields.img == '') {
        var markup = html + img + end;
    }
    else {
        var markup = html + html2 + end;
    }
    return markup;
}

function formatPartsSelection(repo) {
    if (repo.id === '') {
        return '查询条件....';
    }
    return repo.pk;
}

function formatFactory(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var markup = '<div class="box-header with-border"><span class="info-box-text" style="font-size:16px;">' + repo.fields.name + '</span></div>';

    return markup;
}

function formatFactorySelection(repo) {
    if (repo.id === '') {
        return '查询条件....';
    }
    return repo.fields.name;
}

function formatCustomer(repo) {
    if (repo.loading) {
        return repo.text;
    }


    var markup = '<div class="">\n' +
        '                    <div class="box box-widget widget-user-2">\n' +
        '                        <div class="widget-user-header">\n' +
        '                            <div class="widget-user-image">\n' +
        '                                <img class="img-circle" src="/media/' + repo.fields.icon_img + '">\n' +
        '                            </div>\n' +
        '                            <h3 class="widget-user-username" style="display: block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + repo.fields.nick_name + '</h3>\n' +
        '                            <h5 class="widget-user-desc" style="display: block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + repo.fields.name + '</h5>\n' +
        '                        </div>\n' +
        '                    </div>\n' +
        '                </div>';
    return markup;
}

function formatCustomerSelection(repo) {
    if (repo.id === '') {
        return '查询条件....';
    }
    return repo.fields.nick_name;
}



