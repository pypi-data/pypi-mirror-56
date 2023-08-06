define([
    'jquery',
    'base/js/utils',
    'base/js/namespace',
    'base/js/dialog'
], function ($, utils, Jupyter, dialog) {
    'use strict';
    var treePage = function () {
        $("head").append("<link>");
        var css = $("head").children(":last");
        css.attr({
            rel: "stylesheet",
            type: "text/css",
            href: utils.get_body_data('baseUrl') + 'nbextensions/nbsysinfo/tree.css'
        });
    };

    var showBar = function () {
        var dom = '<div class="btn-group dropdown" id="resource_dp">\
            <button class=" btn btn-default btn-xs dropdown-toggle" id="dropdownMenu1" data-toggle="dropdown" aria-expanded="true"> \
                    <span style="vertical-align: middle;color:#777;display: inline-block;padding-right: 4px">内存使用</span>\
                    <div class="progress" style="margin-bottom: 0px; display: inline-block;vertical-align: middle; min-width: 185px; padding-right: 5px">\
                        <div class="progress-bar progress-bar-success bar_mem" role="progresdbar" aria-valuenow="16.240692138671875" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>\
                        <p id="show-mem-usage" style="position: absolute; width:185px; text-align:center; color:#333;font-size: 13px">0M/0M</p>\
                    </div>\
                    <span class="caret"></span>\
            </button>\
            <ul class="dropdown-menu" id="jq-resource" role="menu" aria-labelledby="dropdown1" style="width: 255px">\
                <li role="presentation">\
                    <span style="vertical-align: middle;color:#777;display: inline-block;padding-right: 4px;padding-left:5px;font-size:12px">CPU使用</span>\
                        <div class="progress" style="margin-bottom: 0px; display: inline-block;vertical-align: middle; min-width: 185px; padding-right: 5px">\
                            <div class="progress-bar progress-bar-success bar_cpu" role="progresdbar" aria-valuenow="0.5080618013576359" aria-valuemin="0" ari-valuemax="100" style="width: 0.508062%;"></div>\
                            <p id="show-cpu-usage" style="position: absolute;width:185px; text-align:center; color:#333;font-size: 13px">0%</p>\
                        </div>\
                </li>\
                <li role="presentation" class="divider jq_customer_hidden"></li>\
                <li role="presentation" class="jq_customer_hidden">\
                    <span style="vertical-align: middle;color:#777;display: inline-block;padding-right: 4px;padding-left:5px;font-size:12px">磁盘使用</span>\
                        <div class="progress" style="margin-bottom: 0px; display: inline-block;vertical-align: middle; min-width: 185px; padding-right: 5px">\
                            <div class="progress-bar progress-bar-success bar_disk" role="progresdbar" aria-valuenow="0.067138671875" aria-valuemin="0" aria-valuemax="100" style="width: 0.0671387%;"></div>\
                            <p id="show-disk-usage" style="position: absolute;width:185px; text-align:center; color:#333;font-size: 13px">0M/0M</p>\
                        </div>\
                </li>\
            </ul>\
        </div>';
        $('#maintoolbar-container').append(dom);
        $("#notebook_toolbar .pull-right").before(dom);
    }

    var refreshSysInfo = function() {
        var base_url = utils.get_body_data("baseUrl");
        var url = utils.url_join_encode(base_url, '/sysinfo');
        var action = function(){
            utils.ajax(url, {
                type: "GET",
                async: true,
                dataType: "json",
                timeout: 5000,
                success: function (data, status, xhr) {
                    if (status === "success") {
                        console.log(data);
                        $('#show-mem-usage').text(data.memory_usage+'M/'+data.memory_total+'M');
                        $('.bar_mem').width(((data.memory_usage/data.memory_total)*100) + '%');
                        $('#show-cpu-usage').text(data.cpu_usage + '%');
                        $('.bar_cpu').width(data.cpu_usage + '%');
                        $('#show-disk-usage').text(data.disk_usage+'M/'+data.disk_total+'M');
                        $('.bar_disk').width(((data.disk_usage/data.disk_total)*100) + '%');
                    }
                    else {
                        console.log(status);
                    }
                },
                error: function (xhr, status, error) {
                    console.log(error);
                }
            });
        }
        action();
        setInterval(function(){
            action();
        }, 5000);
    }

    // 插件加载入口
    var load_ipython_extension = function () {
        treePage();
        showBar();
        refreshSysInfo();
    };

    return {
        load_ipython_extension: load_ipython_extension
    };

});
