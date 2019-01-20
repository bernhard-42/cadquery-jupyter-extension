class CqJupyter { // jshint ignore:line

    constructor() {
        x3dom.reload(); // jshint ignore:line
    }

    findShape(id, name) {
        var cq = $('#cq_x3d_column_' + id); // jshint ignore:line
        var children = cq.find('scene').children();
        var shape = null;
        var swtch = null;
        for (var i = 0; i < children.length; i++) {
            if (children[i].getAttribute('DEF') === name) {
                shape = children[i];
                swtch = children[i + 1];
                break;
            }
        }
        return [shape, swtch];
    }

    changeviewpoint(id, dir) {
        document.getElementById(id + '_' + dir + '_view').setAttribute('set_bind','true');
        var e = $('#' + id); // jshint ignore:line
        e[0].runtime.resetView();
    }

    isometric(id) {
        this.changeviewpoint(id, 'iso');
    }

    right(id) {
        this.changeviewpoint(id, 'right');
    }

    left(id) {
        this.changeviewpoint(id, 'left');
    }

    front(id) {
        this.changeviewpoint(id, 'front');
    }

    rear(id) {
        this.changeviewpoint(id, 'rear');
    }

    bottom(id) {
        this.changeviewpoint(id, 'bottom');
    }

    top(id) {
        this.changeviewpoint(id, 'top');
    }

    refit(id) {
        var e = document.getElementById(id);
        e.runtime.fitAll(false);
    }

    showFaces(id, name) {
        var shape = this.findShape(id, name);
        shape[0].setAttribute('render', true);
    }

    hideFaces(id, name) {
      var shape = this.findShape(id, name);
      shape[0].setAttribute('render', false);
    }

    showEdges(id, name) {
      var shape = this.findShape(id, name);
      shape[1].setAttribute('whichChoice', 0);
    }

    hideEdges(id, name) {
      var shape = this.findShape(id, name);
      shape[1].setAttribute('whichChoice', -1);
    }
}