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


    // 插件加载入口
    var load_ipython_extension = function () {
        treePage();
    };

    return {
        load_ipython_extension: load_ipython_extension
    };

});
