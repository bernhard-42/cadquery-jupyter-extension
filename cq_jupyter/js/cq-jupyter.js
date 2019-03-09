class CqJupyter { // jshint ignore:line

    constructor() {
        x3dom.reload(); // jshint ignore:line
    }

    findShape(id, name) {
        var cq = $('#cq_x3d_column_' + id); // jshint ignore:line
        return cq.find("#switch_" + name)[0];
    }
    findMesh(id, name) {
        var cq = $('#cq_x3d_column_' + id); // jshint ignore:line
        return cq.find("#switch_" + name + "_edges")[0]
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
        this.findShape(id, name).setAttribute('whichChoice', 0);
    }

    hideFaces(id, name) {
        this.findShape(id, name).setAttribute('whichChoice', -1);
    }

    showMesh(id, name) {
        this.findMesh(id, name).setAttribute('whichChoice', 0);
    }

    hideMesh(id, name) {
        this.findMesh(id, name).setAttribute('whichChoice', -1);
    }
}