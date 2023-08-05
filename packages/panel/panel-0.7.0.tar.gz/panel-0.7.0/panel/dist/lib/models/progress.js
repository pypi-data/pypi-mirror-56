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
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
Object.defineProperty(exports, "__esModule", { value: true });
var layout_1 = require("@bokehjs/core/layout");
var p = require("@bokehjs/core/properties");
var widget_1 = require("@bokehjs/models/widgets/widget");
var ProgressView = /** @class */ (function (_super) {
    __extends(ProgressView, _super);
    function ProgressView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProgressView.prototype.connect_signals = function () {
        var _this = this;
        _super.prototype.connect_signals.call(this);
        this.connect(this.model.change, function () {
            _this.render();
            _this.root.compute_layout(); // XXX: invalidate_layout?
        });
        this.connect(this.model.properties.active.change, function () { return _this.setCSS(); });
        this.connect(this.model.properties.bar_color.change, function () { return _this.setCSS(); });
        this.connect(this.model.properties.css_classes.change, function () { return _this.setCSS(); });
        this.connect(this.model.properties.value.change, function () { return _this.setValue(); });
        this.connect(this.model.properties.max.change, function () { return _this.setMax(); });
    };
    ProgressView.prototype.render = function () {
        _super.prototype.render.call(this);
        var style = __assign(__assign({}, this.model.style), { display: "inline-block" });
        this.progressEl = document.createElement('progress');
        this.setValue();
        this.setMax();
        // Set styling
        if (!this.model.sizing_mode || this.model.sizing_mode === 'fixed') {
            if (this.model.width)
                this.progressEl.style.width = this.model.width + 'px';
        }
        else if (this.model.sizing_mode == 'stretch_width' ||
            this.model.sizing_mode == 'stretch_both' ||
            this.model.width_policy == 'max' ||
            this.model.width_policy == 'fit') {
            this.progressEl.style.width = '100%';
        }
        this.setCSS();
        for (var prop in style)
            this.progressEl.style.setProperty(prop, style[prop]);
        this.el.appendChild(this.progressEl);
    };
    ProgressView.prototype.setCSS = function () {
        var css = this.model.css_classes.join(" ") + " " + this.model.bar_color;
        if (this.model.active)
            this.progressEl.className = css + " active";
        else
            this.progressEl.className = css;
    };
    ProgressView.prototype.setValue = function () {
        if (this.model.value != null)
            this.progressEl.value = this.model.value;
    };
    ProgressView.prototype.setMax = function () {
        if (this.model.max != null)
            this.progressEl.max = this.model.max;
    };
    ProgressView.prototype._update_layout = function () {
        this.layout = new layout_1.VariadicBox(this.el);
        this.layout.set_sizing(this.box_sizing());
    };
    ProgressView.__name__ = "ProgressView";
    return ProgressView;
}(widget_1.WidgetView));
exports.ProgressView = ProgressView;
var Progress = /** @class */ (function (_super) {
    __extends(Progress, _super);
    function Progress(attrs) {
        return _super.call(this, attrs) || this;
    }
    Progress.init_Progress = function () {
        this.prototype.default_view = ProgressView;
        this.define({
            active: [p.Boolean, true],
            bar_color: [p.String, 'primary'],
            style: [p.Any, {}],
            max: [p.Number, 100],
            value: [p.Number, null],
        });
    };
    Progress.__name__ = "Progress";
    Progress.__module__ = "panel.models.widgets";
    return Progress;
}(widget_1.Widget));
exports.Progress = Progress;
Progress.init_Progress();
//# sourceMappingURL=progress.js.map