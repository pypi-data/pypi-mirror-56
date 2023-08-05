"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var p = require("@bokehjs/core/properties");
var object_1 = require("@bokehjs/core/util/object");
var html_box_1 = require("@bokehjs/models/layouts/html_box");
var dom_1 = require("@bokehjs/core/dom");
var vtk = window.vtk;
function majorAxis(vec3, idxA, idxB) {
    var axis = [0, 0, 0];
    var idx = Math.abs(vec3[idxA]) > Math.abs(vec3[idxB]) ? idxA : idxB;
    var value = vec3[idx] > 0 ? 1 : -1;
    axis[idx] = value;
    return axis;
}
var VTKPlotView = /** @class */ (function (_super) {
    __extends(VTKPlotView, _super);
    function VTKPlotView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._setting = false;
        return _this;
    }
    VTKPlotView.prototype.initialize = function () {
        this._container = dom_1.div({
            style: {
                width: "100%",
                height: "100%"
            }
        });
        _super.prototype.initialize.call(this);
    };
    VTKPlotView.prototype._create_orientation_widget = function () {
        var _this = this;
        var axes = vtk.Rendering.Core.vtkAxesActor.newInstance();
        // add orientation widget
        var orientationWidget = vtk.Interaction.Widgets.vtkOrientationMarkerWidget.newInstance({
            actor: axes,
            interactor: this._interactor,
        });
        orientationWidget.setEnabled(true);
        orientationWidget.setViewportCorner(vtk.Interaction.Widgets.vtkOrientationMarkerWidget.Corners.BOTTOM_RIGHT);
        orientationWidget.setViewportSize(0.15);
        orientationWidget.setMinPixelSize(100);
        orientationWidget.setMaxPixelSize(300);
        this._orientationWidget = orientationWidget;
        var widgetManager = vtk.Widgets.Core.vtkWidgetManager.newInstance();
        widgetManager.setRenderer(orientationWidget.getRenderer());
        var widget = vtk.Widgets.Widgets3D.vtkInteractiveOrientationWidget.newInstance();
        widget.placeWidget(axes.getBounds());
        widget.setBounds(axes.getBounds());
        widget.setPlaceFactor(1);
        var vw = widgetManager.addWidget(widget);
        this._widgetManager = widgetManager;
        // Manage user interaction
        vw.onOrientationChange(function (inputs) {
            var direction = inputs.direction;
            var focalPoint = _this._camera.getFocalPoint();
            var position = _this._camera.getPosition();
            var viewUp = _this._camera.getViewUp();
            var distance = Math.sqrt(Math.pow(position[0] - focalPoint[0], 2) +
                Math.pow(position[1] - focalPoint[1], 2) +
                Math.pow(position[2] - focalPoint[2], 2));
            _this._camera.setPosition(focalPoint[0] + direction[0] * distance, focalPoint[1] + direction[1] * distance, focalPoint[2] + direction[2] * distance);
            if (direction[0]) {
                _this._camera.setViewUp(majorAxis(viewUp, 1, 2));
            }
            if (direction[1]) {
                _this._camera.setViewUp(majorAxis(viewUp, 0, 2));
            }
            if (direction[2]) {
                _this._camera.setViewUp(majorAxis(viewUp, 0, 1));
            }
            _this._orientationWidget.updateMarkerOrientation();
            _this._renderer.resetCameraClippingRange();
            _this._rendererEl.getRenderWindow().render();
        });
        this._orientation_widget_visbility(this.model.orientation_widget);
    };
    VTKPlotView.prototype.after_layout = function () {
        var _this = this;
        if (!this._rendererEl) {
            this.el.appendChild(this._container);
            this._rendererEl = vtk.Rendering.Misc.vtkFullScreenRenderWindow.newInstance({
                rootContainer: this.el,
                container: this._container
            });
            this._renderer = this._rendererEl.getRenderer();
            this._interactor = this._rendererEl.getInteractor();
            this._camera = this._renderer.getActiveCamera();
            this._plot();
            this._camera.onModified(function () { return _this._get_camera_state(); });
            this._remove_default_key_binding();
            this.model.renderer_el = this._rendererEl;
            // this._interactor.onRightButtonPress((_callData: any) => {
            //   console.log('Not Implemented')
            // })
        }
        _super.prototype.after_layout.call(this);
    };
    VTKPlotView.prototype._orientation_widget_visbility = function (visbility) {
        this._orientationWidget.setEnabled(visbility);
        if (visbility) {
            this._widgetManager.enablePicking();
        }
        else {
            this._widgetManager.disablePicking();
        }
        this._orientationWidget.updateMarkerOrientation();
        this._rendererEl.getRenderWindow().render();
    };
    VTKPlotView.prototype.connect_signals = function () {
        var _this = this;
        _super.prototype.connect_signals.call(this);
        this.connect(this.model.properties.data.change, function () { return _this._plot(); });
        this.connect(this.model.properties.camera.change, function () { return _this._set_camera_state(); });
        this.connect(this.model.properties.orientation_widget.change, function () {
            _this._orientation_widget_visbility(_this.model.orientation_widget);
        });
        this._container.addEventListener('mouseenter', function () {
            if (_this.model.enable_keybindings) {
                document.querySelector('body').addEventListener('keypress', _this._interactor.handleKeyPress);
                document.querySelector('body').addEventListener('keydown', _this._interactor.handleKeyDown);
                document.querySelector('body').addEventListener('keyup', _this._interactor.handleKeyUp);
            }
        });
        this._container.addEventListener('mouseleave', function () {
            document.querySelector('body').removeEventListener('keypress', _this._interactor.handleKeyPress);
            document.querySelector('body').removeEventListener('keydown', _this._interactor.handleKeyDown);
            document.querySelector('body').removeEventListener('keyup', _this._interactor.handleKeyUp);
        });
    };
    VTKPlotView.prototype._remove_default_key_binding = function () {
        document.querySelector('body').removeEventListener('keypress', this._interactor.handleKeyPress);
        document.querySelector('body').removeEventListener('keydown', this._interactor.handleKeyDown);
        document.querySelector('body').removeEventListener('keyup', this._interactor.handleKeyUp);
    };
    VTKPlotView.prototype._get_camera_state = function () {
        if (!this._setting) {
            this._setting = true;
            var state = object_1.clone(this._camera.get());
            delete state.classHierarchy;
            delete state.vtkObject;
            delete state.vtkCamera;
            delete state.viewPlaneNormal;
            this.model.camera = state;
            this._setting = false;
        }
    };
    VTKPlotView.prototype._set_camera_state = function () {
        if (!this._setting) {
            this._setting = true;
            try {
                this._camera.set(this.model.camera);
            }
            finally {
                this._setting = false;
            }
            if (this._orientationWidget != null) {
                this._orientationWidget.updateMarkerOrientation();
            }
            this._renderer.resetCameraClippingRange();
            this._rendererEl.getRenderWindow().render();
        }
    };
    VTKPlotView.prototype._plot = function () {
        var _this = this;
        this._delete_all_actors();
        if (!this.model.data) {
            this._rendererEl.getRenderWindow().render();
            return;
        }
        var dataAccessHelper = vtk.IO.Core.DataAccessHelper.get('zip', {
            zipContent: atob(this.model.data),
            callback: function (_zip) {
                var sceneImporter = vtk.IO.Core.vtkHttpSceneLoader.newInstance({
                    renderer: _this._rendererEl.getRenderer(),
                    dataAccessHelper: dataAccessHelper,
                });
                var fn = vtk.macro.debounce(function () {
                    if (_this._orientationWidget == null)
                        _this._create_orientation_widget();
                    _this._set_camera_state();
                }, 100);
                sceneImporter.setUrl('index.json');
                sceneImporter.onReady(fn);
            }
        });
    };
    VTKPlotView.prototype._delete_all_actors = function () {
        var _this = this;
        this._renderer.getActors().map(function (actor) { return _this._renderer.removeActor(actor); });
    };
    VTKPlotView.__name__ = "VTKPlotView";
    return VTKPlotView;
}(html_box_1.HTMLBoxView));
exports.VTKPlotView = VTKPlotView;
var VTKPlot = /** @class */ (function (_super) {
    __extends(VTKPlot, _super);
    function VTKPlot(attrs) {
        var _this = _super.call(this, attrs) || this;
        _this.renderer_el = null;
        _this.outline = vtk.Filters.General.vtkOutlineFilter.newInstance(); //use to display bouding box of a selected actor
        var mapper = vtk.Rendering.Core.vtkMapper.newInstance();
        mapper.setInputConnection(_this.outline.getOutputPort());
        _this.outline_actor = vtk.Rendering.Core.vtkActor.newInstance();
        _this.outline_actor.setMapper(mapper);
        return _this;
    }
    VTKPlot.prototype.getActors = function () {
        return this.renderer_el.getRenderer().getActors();
    };
    VTKPlot.init_VTKPlot = function () {
        this.prototype.default_view = VTKPlotView;
        this.define({
            data: [p.String],
            camera: [p.Any],
            enable_keybindings: [p.Boolean, false],
            orientation_widget: [p.Boolean, false],
        });
        this.override({
            height: 300,
            width: 300
        });
    };
    VTKPlot.__name__ = "VTKPlot";
    VTKPlot.__module__ = "panel.models.vtk";
    return VTKPlot;
}(html_box_1.HTMLBox));
exports.VTKPlot = VTKPlot;
VTKPlot.init_VTKPlot();
//# sourceMappingURL=vtk.js.map