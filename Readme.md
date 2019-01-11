# CadQuery extension jor Jupyter

An extension to view X3DOM content created by CadQuery 2.x

Install

```bash
pip install .
```

Enable

```bash
jupyter nbextension install cq-jupyter --user
jupyter nbextension enable cq-jupyter/js/main --user
```


# Credits

## x3dom

The x3dom framework ([https://www.x3dom.org](https://www.x3dom.org)) is available under the MIT license ([https://github.com/x3dom/component-editor/blob/master/LICENSE](https://github.com/x3dom/component-editor/blob/master/LICENSE)) and the files `css/x3dom.css` and `js/x3dom.js` are downloaded from [https://www.x3dom.org/download/1.7.2](https://www.x3dom.org/download/1.7.2) and used unchanged.

## Component Editor for x3dom

The Component Editor for x3dom ([https://github.com/x3dom/component-editor](https://github.com/x3dom/component-editor)) is available under the MIT license ([https://github.com/x3dom/component-editor/blob/master/LICENSE](https://github.com/x3dom/component-editor/blob/master/LICENSE)): 

- the file `js/jquery.viewConnector.js` is downloaded from [https://github.com/x3dom/component-editor/blob/master/static/js/jquery.viewConnector.js](https://github.com/x3dom/component-editor/blob/master/static/js/jquery.viewConnector.js) and used unchanged
- the axis part in the file `x3d_template.j2` is based on [https://github.com/x3dom/component-editor/blob/master/static/x3d/axesSmall.x3d](https://github.com/x3dom/component-editor/blob/master/static/x3d/axesSmall.x3d)

