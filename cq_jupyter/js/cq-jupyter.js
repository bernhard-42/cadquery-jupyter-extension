class CqJupyter {

    constructor() {
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
        document.getElementById(id +"_" + dir +"_view").setAttribute('set_bind','true');
        var e = $('#' + id);
        e[0].runtime.resetView();
    }

    isometric(id) {
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

    face_toggle(id, name) {
        var shape = this.findShape(id, name);
        var icon = $("#face_toggle_" + name + "_" + id)[0].children[0]
        
        if (shape[0].getAttribute("render") == "true") {
            shape[0].setAttribute("render", false);
            icon.setAttribute("src", "./cq_jupyter/imgs/hidden.png")
        } else {
            shape[0].setAttribute("render", true);
            icon.setAttribute("src", "./cq_jupyter/imgs/visible.png")
        }
    };

    edge_toggle(id, name) {
        var shape = this.findShape(id, name);
        var icon = $("#edge_toggle_" + name + "_" + id)[0].children[0]
        if (shape[1].getAttribute("whichChoice") == -1) {
            shape[1].setAttribute("whichChoice", 0);
            icon.setAttribute("src", "./cq_jupyter/imgs/mesh.png")
        } else {
            shape[1].setAttribute("whichChoice", -1);
            icon.setAttribute("src", "./cq_jupyter/imgs/no_mesh.png")
        }
   };
}