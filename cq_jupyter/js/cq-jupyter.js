class CqJupyter {

    constructor(id, parts) {
        x3dom.reload();
    }

    findShape(id, name) {
        var cq = $('#cq_x3d_column_' + id);
        var children = cq.find("scene").children();
        var shape = null;
        var swtch = null;
        for (var i = 0; i < children.length; i++) {
            if (children[i].getAttribute("DEF") == name) {
                shape = children[i];
                swtch = children[i + 1];
                break;
            }
        }
        return [shape, swtch];
    };

    changeviewpoint(id, dir) {
        document.getElementById(id +"_" + dir +"_view").setAttribute('set_bind','true')
    }

    reset(id) {
        this.changeviewpoint(id, "iso");
    }

    right(id) {
        this.changeviewpoint(id, "right");
    }

    left(id) {
        this.changeviewpoint(id, "left");
    }

    front(id) {
        this.changeviewpoint(id, "front");
    }

    rear(id) {
        this.changeviewpoint(id, "rear");
    }

    bottom(id) {
        this.changeviewpoint(id, "bottom");
    }

    top(id) {
        this.changeviewpoint(id, "top");
    }

    refit(id) {
        var e = document.getElementById(id);
        e.runtime.fitAll(false);
    };

    toggle(id, name) {
        var shape = this.findShape(id, name);
        if (shape[0].getAttribute("render") == "true") {
            shape[0].setAttribute("render", false);
        }
        else {
            shape[0].setAttribute("render", true);
        }
        if (shape[1].getAttribute("whichChoice") == 0) {
            shape[1].setAttribute("whichChoice", -1);
        }
        else {
            shape[1].setAttribute("whichChoice", 0);
        }
    };

    wire(id, name) {
        var shape = this.findShape(id, name);
        if (shape[0].getAttribute("render") == "true") {
            shape[0].setAttribute("render", false);
        }
        else {
            shape[0].setAttribute("render", true);
        }
        shape[1].setAttribute("whichChoice", 0);
    };
}