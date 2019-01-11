define([
    'require', 
    'jquery', 
    './x3dom',
    './jquery.viewConnector',
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
        // load x3dom css
        $('<link/>').attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: requirejs.toUrl('../css/x3dom.css')
        }).appendTo('head');
            
        // load cq-jupyter css
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