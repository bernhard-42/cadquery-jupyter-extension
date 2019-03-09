
'use strict';

function navTree($, divId, data, cqJupyter) { // jshint ignore:line
    var icons = {
        mesh: ['hide_mesh', 'show_mesh', 'mix_mesh'],
        shape: ['hide_shape', 'show_shape', 'mix_shape', 'empty']
    };

    var $tree = $(`#tree-${divId}`);

    $tree.tree({
        data: data,
        autoOpen: 1,
        selectable: false,
        onCreateLi: function (node, $li) {
            var title = $li.find('.jqtree-title');
            title.html(`<span class="toggle_shape tree_icon ${icons.shape[node.shape]}" data-shape-id=${node.id}></span>` +
                       `<span class="toggle_mesh tree_icon  ${icons.mesh[node.mesh]}"   data-mesh-id=${node.id}> </span>` +
            title.html());
            if (node.type === 'part') {
                setObject(node, "shape");
                adaptAssembly($tree.tree('getTree').children, "shape");
                setObject(node, "mesh");
                adaptAssembly($tree.tree('getTree').children, "mesh");
            }
        }
    });

    function setFeature(id, feature, status) {
        var e = $tree.find(`[data-${feature}-id='${id}']`);
        e.removeClass(`show_${feature} hide_${feature} mix_${feature}`);
        e.addClass(icons[feature][status]);
    }

    function setObject(node, feature) {
        if (feature === 'shape') {
            if (node.shape === 1) {
                cqJupyter.showFaces(divId, node.x3d_name)
            } else {
                cqJupyter.hideFaces(divId, node.x3d_name)
            }
        } else {
            if (node.mesh === 1) {
                cqJupyter.showMesh(divId, node.x3d_name)
            } else {
                cqJupyter.hideMesh(divId, node.x3d_name)
            }
        }
    }

    function adaptAssembly(tree, feature) {
        var status = [];
        for (var i = 0; i < tree.length; i++) {
            var node = tree[i];
            console.log(node.type, node.name, feature, node[feature])
            if (node.type === 'part') {
                status.push(node[feature]);
            } else if (node.type === 'assembly') {
                var s = adaptAssembly(node.children, feature);
                node[feature] = s;
                setFeature(node.id, feature, s);
                status.push(s);
            } else if (node.type === 'edges') {
                if (feature === "mesh") {
                    status.push(node[feature]);
                }
            } else {
                console.log(`Wrong node type ${node.type}`);
            }
        }
        console.log(status)
        if ((status.length > 0) && status.every((val, i, arr) => val === arr[0])) {
            return status[0];
        } else {
            return 2;
        }
    }

    function propagateAssembly(node, feature, status) {
        console.log(node, feature, status)
        if (node.type === 'part') {
            node[feature] = status;
            setFeature(node.id, feature, status);
            setObject(node, feature);
        } else if (node.type === 'edges') {
            if (feature === "mesh") {
                node[feature] = status;
                setFeature(node.id, feature, status);
                setObject(node, feature);
            }
        } else if (node.type === 'assembly') {
            for (var i = 0; i < node.children.length; i++) {
                propagateAssembly(node.children[i], feature, status);
            }
        } else {
            console.log(`Wrong node type ${node.type}`);
        }
    }

    function handle(e, feature) {
        var nodeId = $(e.target).data(`${feature}-id`);
        var node = $tree.tree('getNodeById', nodeId);
        if (node.type === 'part') {
            status = (node[feature] + 1) % 2;
            node[feature] = status;
            setFeature(node.id, feature, status);
            setObject(node, feature);

        } else if (node.type === 'edges') {
            if (feature === "mesh" ) {
                status = (node[feature] + 1) % 2;
                node[feature] = status;
                setFeature(node.id, feature, status);
                setObject(node, feature);
            }
        } else if (node.type === 'assembly') {
            var status = 0;
            if (node[feature] < 2) {
                status = (node[feature] + 1) % 2;
            } else {
                status = 1;
            }
            node[feature] = status;
            propagateAssembly(node, feature, status);
        } else {
            console.log(`Wrong node type ${node.type}`);
        }
        adaptAssembly($tree.tree('getTree').children, feature);
    }

    $tree.on('click', '.toggle_shape', function (e) {
        handle(e, 'shape');
    });

    $tree.on('click', '.toggle_mesh', function (e) {
        handle(e, 'mesh');
    });
}