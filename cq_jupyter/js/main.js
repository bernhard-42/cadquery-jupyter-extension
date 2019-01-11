define([
    'require', 
    'jquery', 
    './x3dom',
    './view-connector',
    './cq-jupyter',
    'base/js/namespace'
], function (
    requirejs, 
    $,
    x3dom,
    _ViewConnector,
    CqJupyter,
    Jupyter 
) {
    "use strict";

    var initialize = function () {
        // update params with any specified in the server's config file.
        // the "thisextension" value of the Jupyter notebook config's
        // data may be undefined, but that's ok when using JQuery's extend
        // $.extend(true, params, Jupyter.notebook.config.thisextension);

        // add our extension's css to the page
        $('<link/>').attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: requirejs.toUrl('../css/x3dom.css')
        }).appendTo('head');
            
        $('<link/>').attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: requirejs.toUrl('../css/cq-jupyter.css')
        }).appendTo('head');

        x3dom.reload();
    };

    var load_ipython_extension = function () {
        return Jupyter.notebook.config.loaded.then(initialize);
    }

    // return object to export public methods
    return {
        load_ipython_extension : load_ipython_extension,
        CqJupyter : CqJupyter
    };        
});