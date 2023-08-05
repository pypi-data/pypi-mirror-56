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
var serialization_1 = require("@bokehjs/core/util/serialization");
var html_box_1 = require("@bokehjs/models/layouts/html_box");
var dom_1 = require("@bokehjs/core/dom");
var vtk = window.vtk;
function utf8ToAB(utf8_str) {
    var buf = new ArrayBuffer(utf8_str.length); // 2 bytes for each char
    var bufView = new Uint8Array(buf);
    for (var i = 0, strLen = utf8_str.length; i < strLen; i++) {
        bufView[i] = utf8_str.charCodeAt(i);
    }
    return buf;
}
var VTKVolumePlotView = /** @class */ (function (_super) {
    __extends(VTKVolumePlotView, _super);
    function VTKVolumePlotView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    VTKVolumePlotView.prototype.after_layout = function () {
        if (!this._rendererEl) {
            this._controllerWidget = vtk.Interaction.UI.vtkVolumeController.newInstance({
                size: [400, 150],
                rescaleColorMap: false,
            });
            this._controllerWidget.setContainer(this.el);
            this._container = dom_1.div({
                style: {
                    width: "100%",
                    height: "100%"
                }
            });
            this.el.appendChild(this._container);
            this._rendererEl = vtk.Rendering.Misc.vtkFullScreenRenderWindow.newInstance({
                rootContainer: this.el,
                container: this._container
            });
            this._rendererEl.getRenderWindow().getInteractor();
            this._rendererEl.getRenderWindow().getInteractor().setDesiredUpdateRate(45);
            this._plot();
            this._rendererEl.getRenderer().resetCamera();
            this._rendererEl.getRenderWindow().render();
        }
        _super.prototype.after_layout.call(this);
    };
    VTKVolumePlotView.prototype._create_source = function () {
        var data = this.model.data;
        var source = vtk.Common.DataModel.vtkImageData.newInstance({
            spacing: data.spacing
        });
        source.setDimensions(data.dims);
        source.setOrigin(data.origin != null ? data.origin : data.dims.map(function (v) { return v / 2; }));
        var dataArray = vtk.Common.Core.vtkDataArray.newInstance({
            name: "scalars",
            numberOfComponents: 1,
            values: new serialization_1.ARRAY_TYPES[data.dtype](utf8ToAB(atob(data.buffer)))
        });
        source.getPointData().setScalars(dataArray);
        return source;
    };
    VTKVolumePlotView.prototype._plot = function () {
        //Create vtk volume and add it to the scene
        var source = this._create_source();
        var actor = vtk.Rendering.Core.vtkVolume.newInstance();
        var mapper = vtk.Rendering.Core.vtkVolumeMapper.newInstance();
        actor.setMapper(mapper);
        mapper.setInputData(source);
        var dataArray = source.getPointData().getScalars() || source.getPointData().getArrays()[0];
        var dataRange = dataArray.getRange();
        var lookupTable = vtk.Rendering.Core.vtkColorTransferFunction.newInstance();
        var piecewiseFunction = vtk.Common.DataModel.vtkPiecewiseFunction.newInstance();
        var sampleDistance = 0.7 * Math.sqrt(source.getSpacing()
            .map(function (v) { return v * v; })
            .reduce(function (a, b) { return a + b; }, 0));
        mapper.setSampleDistance(sampleDistance);
        actor.getProperty().setRGBTransferFunction(0, lookupTable);
        actor.getProperty().setScalarOpacity(0, piecewiseFunction);
        actor.getProperty().setInterpolationTypeToFastLinear();
        //actor.getProperty().setInterpolationTypeToLinear();
        // For better looking volume rendering
        // - distance in world coordinates a scalar opacity of 1.0
        actor
            .getProperty()
            .setScalarOpacityUnitDistance(0, vtk.Common.DataModel.vtkBoundingBox.getDiagonalLength(source.getBounds()) / Math.max.apply(Math, source.getDimensions()));
        // - control how we emphasize surface boundaries
        //  => max should be around the average gradient magnitude for the
        //     volume or maybe average plus one std dev of the gradient magnitude
        //     (adjusted for spacing, this is a world coordinate gradient, not a
        //     pixel gradient)
        //  => max hack: (dataRange[1] - dataRange[0]) * 0.05
        actor.getProperty().setGradientOpacityMinimumValue(0, 0);
        actor
            .getProperty()
            .setGradientOpacityMaximumValue(0, (dataRange[1] - dataRange[0]) * 0.05);
        // - Use shading based on gradient
        actor.getProperty().setShade(true);
        actor.getProperty().setUseGradientOpacity(0, true);
        // - generic good default
        actor.getProperty().setGradientOpacityMinimumOpacity(0, 0.0);
        actor.getProperty().setGradientOpacityMaximumOpacity(0, 1.0);
        actor.getProperty().setAmbient(0.2);
        actor.getProperty().setDiffuse(0.7);
        actor.getProperty().setSpecular(0.3);
        actor.getProperty().setSpecularPower(8.0);
        this._rendererEl.getRenderer().addVolume(actor);
        this._controllerWidget.setupContent(this._rendererEl.getRenderWindow(), actor, true);
    };
    VTKVolumePlotView.__name__ = "VTKVolumePlotView";
    return VTKVolumePlotView;
}(html_box_1.HTMLBoxView));
exports.VTKVolumePlotView = VTKVolumePlotView;
var VTKVolumePlot = /** @class */ (function (_super) {
    __extends(VTKVolumePlot, _super);
    function VTKVolumePlot(attrs) {
        return _super.call(this, attrs) || this;
    }
    VTKVolumePlot.init_VTKVolumePlot = function () {
        this.prototype.default_view = VTKVolumePlotView;
        this.define({
            data: [p.Any],
            actor: [p.Any],
        });
        this.override({
            height: 300,
            width: 300
        });
    };
    VTKVolumePlot.__name__ = "VTKVolumePlot";
    VTKVolumePlot.__module__ = "panel.models.vtk";
    return VTKVolumePlot;
}(html_box_1.HTMLBox));
exports.VTKVolumePlot = VTKVolumePlot;
VTKVolumePlot.init_VTKVolumePlot();
//# sourceMappingURL=vtkvolume.js.map