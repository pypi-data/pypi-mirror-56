/*!
 * Copyright (c) 2012 - 2019, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
*/
(function(root, factory) {
  factory(root["Bokeh"]);
})(this, function(Bokeh) {
  var define;
  return (function(modules, entry, aliases, externals) {
    if (Bokeh != null) {
      return Bokeh.register_plugin(modules, entry, aliases, externals);
    } else {
      throw new Error("Cannot find Bokeh. You have to load it prior to loading plugins.");
    }
  })
({
"55dac5102b": /* index.js */ function _(require, module, exports) {
    var Panel = require("1d13522e8a") /* ./models */;
    exports.Panel = Panel;
    var base_1 = require("@bokehjs/base");
    base_1.register_models(Panel);
},
"1d13522e8a": /* models/index.js */ function _(require, module, exports) {
    var ace_1 = require("c167e0e33e") /* ./ace */;
    exports.AcePlot = ace_1.AcePlot;
    var audio_1 = require("d2f2f8c2b2") /* ./audio */;
    exports.Audio = audio_1.Audio;
    var html_1 = require("cef8bc2777") /* ./html */;
    exports.HTML = html_1.HTML;
    var katex_1 = require("7a3cc4b4c6") /* ./katex */;
    exports.KaTeX = katex_1.KaTeX;
    var mathjax_1 = require("75803aafc7") /* ./mathjax */;
    exports.MathJax = mathjax_1.MathJax;
    var player_1 = require("24a20e4790") /* ./player */;
    exports.Player = player_1.Player;
    var plotly_1 = require("c864119ab3") /* ./plotly */;
    exports.PlotlyPlot = plotly_1.PlotlyPlot;
    var progress_1 = require("1d01be8a6e") /* ./progress */;
    exports.Progress = progress_1.Progress;
    var state_1 = require("4cbc2c8e7e") /* ./state */;
    exports.State = state_1.State;
    var vega_1 = require("780561860e") /* ./vega */;
    exports.VegaPlot = vega_1.VegaPlot;
    var video_1 = require("4a2dcd4d15") /* ./video */;
    exports.Video = video_1.Video;
    var videostream_1 = require("cbedefa11b") /* ./videostream */;
    exports.VideoStream = videostream_1.VideoStream;
    var vtk_1 = require("d4af2357ca") /* ./vtk */;
    exports.VTKPlot = vtk_1.VTKPlot;
    var vtkvolume_1 = require("64e1d58d42") /* ./vtkvolume */;
    exports.VTKVolumePlot = vtkvolume_1.VTKVolumePlot;
},
"c167e0e33e": /* models/ace.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var html_box_1 = require("@bokehjs/models/layouts/html_box");
    var dom_1 = require("@bokehjs/core/dom");
    function ID() {
        // Math.random should be unique because of its seeding algorithm.
        // Convert it to base 36 (numbers + letters), and grab the first 9 characters
        // after the decimal.
        return '_' + Math.random().toString(36).substr(2, 9);
    }
    var AcePlotView = /** @class */ (function (_super) {
        __extends(AcePlotView, _super);
        function AcePlotView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        AcePlotView.prototype.initialize = function () {
            _super.prototype.initialize.call(this);
            this._ace = window.ace;
            this._container = dom_1.div({
                id: ID(),
                style: {
                    width: "100%",
                    height: "100%"
                }
            });
        };
        AcePlotView.prototype.connect_signals = function () {
            var _this = this;
            _super.prototype.connect_signals.call(this);
            this.connect(this.model.properties.code.change, function () { return _this._update_code_from_model(); });
            this.connect(this.model.properties.theme.change, function () { return _this._update_theme(); });
            this.connect(this.model.properties.language.change, function () { return _this._update_language(); });
            this.connect(this.model.properties.annotations.change, function () { return _this._add_annotations(); });
            this.connect(this.model.properties.readonly.change, function () {
                _this._editor.setReadOnly(_this.model.readonly);
            });
        };
        AcePlotView.prototype.render = function () {
            var _this = this;
            _super.prototype.render.call(this);
            if (!(this._container === this.el.childNodes[0]))
                this.el.appendChild(this._container);
            this._container.textContent = this.model.code;
            this._editor = this._ace.edit(this._container.id);
            this._editor.setTheme("ace/theme/" + ("" + this.model.theme));
            this._editor.session.setMode("ace/mode/" + ("" + this.model.language));
            this._editor.setReadOnly(this.model.readonly);
            this._langTools = this._ace.require('ace/ext/language_tools');
            this._editor.setOptions({
                enableBasicAutocompletion: true,
                enableSnippets: true,
                fontFamily: "monospace",
            });
            this._editor.on('change', function () { return _this._update_code_from_editor(); });
        };
        AcePlotView.prototype._update_code_from_model = function () {
            if (this._editor && this._editor.getValue() != this.model.code)
                this._editor.setValue(this.model.code);
        };
        AcePlotView.prototype._update_code_from_editor = function () {
            if (this._editor.getValue() != this.model.code) {
                this.model.code = this._editor.getValue();
            }
        };
        AcePlotView.prototype._update_theme = function () {
            this._editor.setTheme("ace/theme/" + ("" + this.model.theme));
        };
        AcePlotView.prototype._update_language = function () {
            this._editor.session.setMode("ace/mode/" + ("" + this.model.language));
        };
        AcePlotView.prototype._add_annotations = function () {
            this._editor.session.setAnnotations(this.model.annotations);
        };
        AcePlotView.prototype.after_layout = function () {
            _super.prototype.after_layout.call(this);
            this._editor.resize();
        };
        AcePlotView.__name__ = "AcePlotView";
        return AcePlotView;
    }(html_box_1.HTMLBoxView));
    exports.AcePlotView = AcePlotView;
    var AcePlot = /** @class */ (function (_super) {
        __extends(AcePlot, _super);
        function AcePlot(attrs) {
            return _super.call(this, attrs) || this;
        }
        AcePlot.init_AcePlot = function () {
            this.prototype.default_view = AcePlotView;
            this.define({
                code: [p.String],
                language: [p.String, 'python'],
                theme: [p.String, 'chrome'],
                annotations: [p.Array, []],
                readonly: [p.Boolean, false]
            });
            this.override({
                height: 300,
                width: 300
            });
        };
        AcePlot.__name__ = "AcePlot";
        AcePlot.__module__ = "panel.models.ace";
        return AcePlot;
    }(html_box_1.HTMLBox));
    exports.AcePlot = AcePlot;
    AcePlot.init_AcePlot();
},
"d2f2f8c2b2": /* models/audio.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var widget_1 = require("@bokehjs/models/widgets/widget");
    var AudioView = /** @class */ (function (_super) {
        __extends(AudioView, _super);
        function AudioView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        AudioView.prototype.initialize = function () {
            _super.prototype.initialize.call(this);
            this._blocked = false;
            this._time = Date.now();
        };
        AudioView.prototype.connect_signals = function () {
            var _this = this;
            _super.prototype.connect_signals.call(this);
            this.connect(this.model.change, function () { return _this.render(); });
            this.connect(this.model.properties.loop.change, function () { return _this.set_loop(); });
            this.connect(this.model.properties.paused.change, function () { return _this.set_paused(); });
            this.connect(this.model.properties.time.change, function () { return _this.set_time(); });
            this.connect(this.model.properties.value.change, function () { return _this.set_value(); });
            this.connect(this.model.properties.volume.change, function () { return _this.set_volume(); });
        };
        AudioView.prototype.render = function () {
            var _this = this;
            if (this.audioEl)
                return;
            this.audioEl = document.createElement('audio');
            this.audioEl.controls = true;
            this.audioEl.src = this.model.value;
            this.audioEl.currentTime = this.model.time;
            this.audioEl.loop = this.model.loop;
            if (this.model.volume != null)
                this.audioEl.volume = this.model.volume / 100;
            else
                this.model.volume = this.audioEl.volume * 100;
            this.audioEl.onpause = function () { return _this.model.paused = true; };
            this.audioEl.onplay = function () { return _this.model.paused = false; };
            this.audioEl.ontimeupdate = function () { return _this.update_time(_this); };
            this.audioEl.onvolumechange = function () { return _this.update_volume(_this); };
            this.el.appendChild(this.audioEl);
            if (!this.model.paused)
                this.audioEl.play();
        };
        AudioView.prototype.update_time = function (view) {
            if ((Date.now() - view._time) < view.model.throttle)
                return;
            view._blocked = true;
            view.model.time = view.audioEl.currentTime;
            view._time = Date.now();
        };
        AudioView.prototype.update_volume = function (view) {
            view._blocked = true;
            view.model.volume = view.audioEl.volume * 100;
        };
        AudioView.prototype.set_loop = function () {
            this.audioEl.loop = this.model.loop;
        };
        AudioView.prototype.set_paused = function () {
            if (!this.audioEl.paused && this.model.paused)
                this.audioEl.pause();
            if (this.audioEl.paused && !this.model.paused)
                this.audioEl.play();
        };
        AudioView.prototype.set_volume = function () {
            if (this._blocked) {
                this._blocked = false;
                return;
            }
            if (this.model.volume != null) {
                this.audioEl.volume = this.model.volume / 100;
            }
        };
        AudioView.prototype.set_time = function () {
            if (this._blocked) {
                this._blocked = false;
                return;
            }
            this.audioEl.currentTime = this.model.time;
        };
        AudioView.prototype.set_value = function () {
            this.audioEl.src = this.model.value;
        };
        AudioView.__name__ = "AudioView";
        return AudioView;
    }(widget_1.WidgetView));
    exports.AudioView = AudioView;
    var Audio = /** @class */ (function (_super) {
        __extends(Audio, _super);
        function Audio(attrs) {
            return _super.call(this, attrs) || this;
        }
        Audio.init_Audio = function () {
            this.prototype.default_view = AudioView;
            this.define({
                loop: [p.Boolean, false],
                paused: [p.Boolean, true],
                time: [p.Number, 0],
                throttle: [p.Number, 250],
                value: [p.Any, ''],
                volume: [p.Number, null],
            });
        };
        Audio.__name__ = "Audio";
        Audio.__module__ = "panel.models.widgets";
        return Audio;
    }(widget_1.Widget));
    exports.Audio = Audio;
    Audio.init_Audio();
},
"cef8bc2777": /* models/html.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var markup_1 = require("@bokehjs/models/widgets/markup");
    function htmlDecode(input) {
        var doc = new DOMParser().parseFromString(input, "text/html");
        return doc.documentElement.textContent;
    }
    var HTMLView = /** @class */ (function (_super) {
        __extends(HTMLView, _super);
        function HTMLView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        HTMLView.prototype.render = function () {
            _super.prototype.render.call(this);
            var html = htmlDecode(this.model.text);
            if (!html) {
                this.markup_el.innerHTML = '';
                return;
            }
            this.markup_el.innerHTML = html;
            Array.from(this.markup_el.querySelectorAll("script")).forEach(function (oldScript) {
                var newScript = document.createElement("script");
                Array.from(oldScript.attributes)
                    .forEach(function (attr) { return newScript.setAttribute(attr.name, attr.value); });
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                if (oldScript.parentNode)
                    oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        };
        HTMLView.__name__ = "HTMLView";
        return HTMLView;
    }(markup_1.MarkupView));
    exports.HTMLView = HTMLView;
    var HTML = /** @class */ (function (_super) {
        __extends(HTML, _super);
        function HTML(attrs) {
            return _super.call(this, attrs) || this;
        }
        HTML.init_HTML = function () {
            this.prototype.default_view = HTMLView;
        };
        HTML.__name__ = "HTML";
        HTML.__module__ = "panel.models.markup";
        return HTML;
    }(markup_1.Markup));
    exports.HTML = HTML;
    HTML.init_HTML();
},
"7a3cc4b4c6": /* models/katex.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var markup_1 = require("@bokehjs/models/widgets/markup");
    var KaTeXView = /** @class */ (function (_super) {
        __extends(KaTeXView, _super);
        function KaTeXView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        KaTeXView.prototype.render = function () {
            _super.prototype.render.call(this);
            this.markup_el.innerHTML = this.model.text;
            if (!window.renderMathInElement) {
                return;
            }
            window.renderMathInElement(this.el, {
                delimiters: [
                    { left: "$$", right: "$$", display: true },
                    { left: "\\[", right: "\\]", display: true },
                    { left: "$", right: "$", display: false },
                    { left: "\\(", right: "\\)", display: false }
                ]
            });
        };
        KaTeXView.__name__ = "KaTeXView";
        return KaTeXView;
    }(markup_1.MarkupView));
    exports.KaTeXView = KaTeXView;
    var KaTeX = /** @class */ (function (_super) {
        __extends(KaTeX, _super);
        function KaTeX(attrs) {
            return _super.call(this, attrs) || this;
        }
        KaTeX.init_KaTeX = function () {
            this.prototype.default_view = KaTeXView;
        };
        KaTeX.__name__ = "KaTeX";
        KaTeX.__module__ = "panel.models.katex";
        return KaTeX;
    }(markup_1.Markup));
    exports.KaTeX = KaTeX;
    KaTeX.init_KaTeX();
},
"75803aafc7": /* models/mathjax.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var markup_1 = require("@bokehjs/models/widgets/markup");
    var MathJaxView = /** @class */ (function (_super) {
        __extends(MathJaxView, _super);
        function MathJaxView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        MathJaxView.prototype.initialize = function () {
            _super.prototype.initialize.call(this);
            this._hub = window.MathJax.Hub;
            this._hub.Config({
                tex2jax: { inlineMath: [['$', '$'], ['\\(', '\\)']] }
            });
        };
        MathJaxView.prototype.render = function () {
            _super.prototype.render.call(this);
            if (!this._hub) {
                return;
            }
            this.markup_el.innerHTML = this.model.text;
            this._hub.Queue(["Typeset", this._hub, this.markup_el]);
        };
        MathJaxView.__name__ = "MathJaxView";
        return MathJaxView;
    }(markup_1.MarkupView));
    exports.MathJaxView = MathJaxView;
    var MathJax = /** @class */ (function (_super) {
        __extends(MathJax, _super);
        function MathJax(attrs) {
            return _super.call(this, attrs) || this;
        }
        MathJax.init_MathJax = function () {
            this.prototype.default_view = MathJaxView;
        };
        MathJax.__name__ = "MathJax";
        MathJax.__module__ = "panel.models.mathjax";
        return MathJax;
    }(markup_1.Markup));
    exports.MathJax = MathJax;
    MathJax.init_MathJax();
},
"24a20e4790": /* models/player.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var dom_1 = require("@bokehjs/core/dom");
    var widget_1 = require("@bokehjs/models/widgets/widget");
    var PlayerView = /** @class */ (function (_super) {
        __extends(PlayerView, _super);
        function PlayerView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        PlayerView.prototype.connect_signals = function () {
            var _this = this;
            _super.prototype.connect_signals.call(this);
            this.connect(this.model.change, function () { return _this.render(); });
            this.connect(this.model.properties.value.change, function () { return _this.render(); });
            this.connect(this.model.properties.loop_policy.change, function () { return _this.set_loop_state(_this.model.loop_policy); });
        };
        PlayerView.prototype.get_height = function () {
            return 250;
        };
        PlayerView.prototype.render = function () {
            var _this = this;
            if (this.sliderEl == null) {
                _super.prototype.render.call(this);
            }
            else {
                this.sliderEl.style.width = "{this.model.width}px";
                this.sliderEl.min = String(this.model.start);
                this.sliderEl.max = String(this.model.end);
                this.sliderEl.value = String(this.model.value);
                return;
            }
            // Slider
            this.sliderEl = document.createElement('input');
            this.sliderEl.setAttribute("type", "range");
            this.sliderEl.style.width = this.model.width + 'px';
            this.sliderEl.value = String(this.model.value);
            this.sliderEl.min = String(this.model.start);
            this.sliderEl.max = String(this.model.end);
            this.sliderEl.onchange = function (ev) { return _this.set_frame(parseInt(ev.target.value)); };
            // Buttons
            var button_div = dom_1.div();
            button_div.style.cssText = "margin: 0 auto; display: table; padding: 5px";
            var button_style = "text-align: center; min-width: 40px; margin: 2px";
            var slower = document.createElement('button');
            slower.style.cssText = "text-align: center; min-width: 20px";
            slower.appendChild(document.createTextNode('–'));
            slower.onclick = function () { return _this.slower(); };
            button_div.appendChild(slower);
            var first = document.createElement('button');
            first.style.cssText = button_style;
            first.appendChild(document.createTextNode('\u275a\u25c0\u25c0'));
            first.onclick = function () { return _this.first_frame(); };
            button_div.appendChild(first);
            var previous = document.createElement('button');
            previous.style.cssText = button_style;
            previous.appendChild(document.createTextNode('\u275a\u25c0'));
            previous.onclick = function () { return _this.previous_frame(); };
            button_div.appendChild(previous);
            var reverse = document.createElement('button');
            reverse.style.cssText = button_style;
            reverse.appendChild(document.createTextNode('\u25c0'));
            reverse.onclick = function () { return _this.reverse_animation(); };
            button_div.appendChild(reverse);
            var pause = document.createElement('button');
            pause.style.cssText = button_style;
            pause.appendChild(document.createTextNode('\u275a\u275a'));
            pause.onclick = function () { return _this.pause_animation(); };
            button_div.appendChild(pause);
            var play = document.createElement('button');
            play.style.cssText = button_style;
            play.appendChild(document.createTextNode('\u25b6'));
            play.onclick = function () { return _this.play_animation(); };
            button_div.appendChild(play);
            var next = document.createElement('button');
            next.style.cssText = button_style;
            next.appendChild(document.createTextNode('\u25b6\u275a'));
            next.onclick = function () { return _this.next_frame(); };
            button_div.appendChild(next);
            var last = document.createElement('button');
            last.style.cssText = button_style;
            last.appendChild(document.createTextNode('\u25b6\u25b6\u275a'));
            last.onclick = function () { return _this.last_frame(); };
            button_div.appendChild(last);
            var faster = document.createElement('button');
            faster.style.cssText = "text-align: center; min-width: 20px";
            faster.appendChild(document.createTextNode('+'));
            faster.onclick = function () { return _this.faster(); };
            button_div.appendChild(faster);
            // Loop control
            this.loop_state = document.createElement('form');
            this.loop_state.style.cssText = "margin: 0 auto; display: table";
            var once = document.createElement('input');
            once.type = "radio";
            once.value = "once";
            once.name = "state";
            var once_label = document.createElement('label');
            once_label.innerHTML = "Once";
            once_label.style.cssText = "padding: 0 10px 0 5px; user-select:none;";
            var loop = document.createElement('input');
            loop.setAttribute("type", "radio");
            loop.setAttribute("value", "loop");
            loop.setAttribute("name", "state");
            var loop_label = document.createElement('label');
            loop_label.innerHTML = "Loop";
            loop_label.style.cssText = "padding: 0 10px 0 5px; user-select:none;";
            var reflect = document.createElement('input');
            reflect.setAttribute("type", "radio");
            reflect.setAttribute("value", "reflect");
            reflect.setAttribute("name", "state");
            var reflect_label = document.createElement('label');
            reflect_label.innerHTML = "Reflect";
            reflect_label.style.cssText = "padding: 0 10px 0 5px; user-select:none;";
            if (this.model.loop_policy == "once")
                once.checked = true;
            else if (this.model.loop_policy == "loop")
                loop.checked = true;
            else
                reflect.checked = true;
            // Compose everything
            this.loop_state.appendChild(once);
            this.loop_state.appendChild(once_label);
            this.loop_state.appendChild(loop);
            this.loop_state.appendChild(loop_label);
            this.loop_state.appendChild(reflect);
            this.loop_state.appendChild(reflect_label);
            this.el.appendChild(this.sliderEl);
            this.el.appendChild(button_div);
            this.el.appendChild(this.loop_state);
        };
        PlayerView.prototype.set_frame = function (frame) {
            if (this.model.value != frame)
                this.model.value = frame;
            if (this.sliderEl.value != String(frame))
                this.sliderEl.value = String(frame);
        };
        PlayerView.prototype.get_loop_state = function () {
            var button_group = this.loop_state.state;
            for (var i = 0; i < button_group.length; i++) {
                var button = button_group[i];
                if (button.checked)
                    return button.value;
            }
            return "once";
        };
        PlayerView.prototype.set_loop_state = function (state) {
            var button_group = this.loop_state.state;
            for (var i = 0; i < button_group.length; i++) {
                var button = button_group[i];
                if (button.value == state)
                    button.checked = true;
            }
        };
        PlayerView.prototype.next_frame = function () {
            this.set_frame(Math.min(this.model.end, this.model.value + this.model.step));
        };
        PlayerView.prototype.previous_frame = function () {
            this.set_frame(Math.max(this.model.start, this.model.value - this.model.step));
        };
        PlayerView.prototype.first_frame = function () {
            this.set_frame(this.model.start);
        };
        PlayerView.prototype.last_frame = function () {
            this.set_frame(this.model.end);
        };
        PlayerView.prototype.slower = function () {
            this.model.interval = Math.round(this.model.interval / 0.7);
            if (this.model.direction > 0)
                this.play_animation();
            else if (this.model.direction < 0)
                this.reverse_animation();
        };
        PlayerView.prototype.faster = function () {
            this.model.interval = Math.round(this.model.interval * 0.7);
            if (this.model.direction > 0)
                this.play_animation();
            else if (this.model.direction < 0)
                this.reverse_animation();
        };
        PlayerView.prototype.anim_step_forward = function () {
            if (this.model.value < this.model.end) {
                this.next_frame();
            }
            else {
                var loop_state = this.get_loop_state();
                if (loop_state == "loop") {
                    this.first_frame();
                }
                else if (loop_state == "reflect") {
                    this.last_frame();
                    this.reverse_animation();
                }
                else {
                    this.pause_animation();
                    this.last_frame();
                }
            }
        };
        PlayerView.prototype.anim_step_reverse = function () {
            if (this.model.value > this.model.start) {
                this.previous_frame();
            }
            else {
                var loop_state = this.get_loop_state();
                if (loop_state == "loop") {
                    this.last_frame();
                }
                else if (loop_state == "reflect") {
                    this.first_frame();
                    this.play_animation();
                }
                else {
                    this.pause_animation();
                    this.first_frame();
                }
            }
        };
        PlayerView.prototype.pause_animation = function () {
            this.model.direction = 0;
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
        };
        PlayerView.prototype.play_animation = function () {
            var _this = this;
            this.pause_animation();
            this.model.direction = 1;
            if (!this.timer)
                this.timer = setInterval(function () { return _this.anim_step_forward(); }, this.model.interval);
        };
        PlayerView.prototype.reverse_animation = function () {
            var _this = this;
            this.pause_animation();
            this.model.direction = -1;
            if (!this.timer)
                this.timer = setInterval(function () { return _this.anim_step_reverse(); }, this.model.interval);
        };
        PlayerView.__name__ = "PlayerView";
        return PlayerView;
    }(widget_1.WidgetView));
    exports.PlayerView = PlayerView;
    var Player = /** @class */ (function (_super) {
        __extends(Player, _super);
        function Player(attrs) {
            return _super.call(this, attrs) || this;
        }
        Player.init_Player = function () {
            this.prototype.default_view = PlayerView;
            this.define({
                direction: [p.Number, 0],
                interval: [p.Number, 500],
                start: [p.Number,],
                end: [p.Number,],
                step: [p.Number, 1],
                loop_policy: [p.Any, "once"],
                value: [p.Any, 0],
            });
            this.override({ width: 400 });
        };
        Player.__name__ = "Player";
        Player.__module__ = "panel.models.widgets";
        return Player;
    }(widget_1.Widget));
    exports.Player = Player;
    Player.init_Player();
},
"c864119ab3": /* models/plotly.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var object_1 = require("@bokehjs/core/util/object");
    var html_box_1 = require("@bokehjs/models/layouts/html_box");
    var _ = window._;
    var Plotly = window.Plotly;
    function isPlainObject(obj) {
        return Object.prototype.toString.call(obj) === '[object Object]';
    }
    var filterEventData = function (gd, eventData, event) {
        // Ported from dash-core-components/src/components/Graph.react.js
        var filteredEventData = Array.isArray(eventData) ? [] : {};
        if (event === "click" || event === "hover" || event === "selected") {
            var points = [];
            if (eventData === undefined || eventData === null) {
                return null;
            }
            /*
             * remove `data`, `layout`, `xaxis`, etc
             * objects from the event data since they're so big
             * and cause JSON stringify ciricular structure errors.
             *
             * also, pull down the `customdata` point from the data array
             * into the event object
             */
            var data = gd.data;
            for (var i = 0; i < eventData.points.length; i++) {
                var fullPoint = eventData.points[i];
                var pointData = {};
                for (var property in fullPoint) {
                    var val = fullPoint[property];
                    if (fullPoint.hasOwnProperty(property) &&
                        !Array.isArray(val) && !isPlainObject(val)) {
                        pointData[property] = val;
                    }
                }
                if (fullPoint !== undefined && fullPoint !== null) {
                    if (fullPoint.hasOwnProperty("curveNumber") &&
                        fullPoint.hasOwnProperty("pointNumber") &&
                        data[fullPoint["curveNumber"]].hasOwnProperty("customdata")) {
                        pointData["customdata"] =
                            data[fullPoint["curveNumber"]].customdata[fullPoint["pointNumber"]];
                    }
                    // specific to histogram. see https://github.com/plotly/plotly.js/pull/2113/
                    if (fullPoint.hasOwnProperty('pointNumbers')) {
                        pointData["pointNumbers"] = fullPoint.pointNumbers;
                    }
                }
                points[i] = pointData;
            }
            filteredEventData["points"] = points;
        }
        else if (event === 'relayout' || event === 'restyle') {
            /*
             * relayout shouldn't include any big objects
             * it will usually just contain the ranges of the axes like
             * "xaxis.range[0]": 0.7715822247381828,
             * "xaxis.range[1]": 3.0095292008680063`
             */
            for (var property in eventData) {
                if (eventData.hasOwnProperty(property)) {
                    filteredEventData[property] = eventData[property];
                }
            }
        }
        if (eventData.hasOwnProperty('range')) {
            filteredEventData["range"] = eventData["range"];
        }
        if (eventData.hasOwnProperty('lassoPoints')) {
            filteredEventData["lassoPoints"] = eventData["lassoPoints"];
        }
        return filteredEventData;
    };
    var PlotlyPlotView = /** @class */ (function (_super) {
        __extends(PlotlyPlotView, _super);
        function PlotlyPlotView() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this._settingViewport = false;
            _this._plotInitialized = false;
            _this._reacting = false;
            _this._relayouting = false;
            _this._end_relayouting = _.debounce(function () {
                _this._relayouting = false;
            }, 2000, { leading: false });
            return _this;
        }
        PlotlyPlotView.prototype.connect_signals = function () {
            _super.prototype.connect_signals.call(this);
            this.connect(this.model.properties.viewport_update_policy.change, this._updateSetViewportFunction);
            this.connect(this.model.properties.viewport_update_throttle.change, this._updateSetViewportFunction);
            this.connect(this.model.properties._render_count.change, this.render);
            this.connect(this.model.properties.viewport.change, this._updateViewportFromProperty);
        };
        PlotlyPlotView.prototype.render = function () {
            var _this = this;
            if (!window.Plotly) {
                return;
            }
            var data = [];
            for (var i = 0; i < this.model.data.length; i++) {
                data.push(this._get_trace(i, false));
            }
            var newLayout = _.cloneDeep(this.model.layout);
            if (this._relayouting) {
                var layout = this.el.layout;
                // For each xaxis* and yaxis* property of layout, if the value has a 'range'
                // property then use this in newLayout
                _.forOwn(layout, function (value, key) {
                    if (key.slice(1, 5) === "axis" && _.has(value, 'range')) {
                        newLayout[key].range = value.range;
                    }
                });
            }
            this._reacting = true;
            Plotly.react(this.el, data, newLayout, this.model.config).then(function () {
                _this._updateSetViewportFunction();
                _this._updateViewportProperty();
                if (!_this._plotInitialized) {
                    // Install callbacks
                    //  - plotly_relayout
                    (_this.el).on('plotly_relayout', function (eventData) {
                        if (eventData['_update_from_property'] !== true) {
                            _this.model.relayout_data = filterEventData(_this.el, eventData, 'relayout');
                            _this._updateViewportProperty();
                            _this._end_relayouting();
                        }
                    });
                    //  - plotly_relayouting
                    (_this.el).on('plotly_relayouting', function () {
                        if (_this.model.viewport_update_policy !== 'mouseup') {
                            _this._relayouting = true;
                            _this._updateViewportProperty();
                        }
                    });
                    //  - plotly_restyle
                    (_this.el).on('plotly_restyle', function (eventData) {
                        _this.model.restyle_data = filterEventData(_this.el, eventData, 'restyle');
                        _this._updateViewportProperty();
                    });
                    //  - plotly_click
                    (_this.el).on('plotly_click', function (eventData) {
                        _this.model.click_data = filterEventData(_this.el, eventData, 'click');
                    });
                    //  - plotly_hover
                    (_this.el).on('plotly_hover', function (eventData) {
                        _this.model.hover_data = filterEventData(_this.el, eventData, 'hover');
                    });
                    //  - plotly_selected
                    (_this.el).on('plotly_selected', function (eventData) {
                        _this.model.selected_data = filterEventData(_this.el, eventData, 'selected');
                    });
                    //  - plotly_clickannotation
                    (_this.el).on('plotly_clickannotation', function (eventData) {
                        delete eventData["event"];
                        delete eventData["fullAnnotation"];
                        _this.model.clickannotation_data = eventData;
                    });
                    //  - plotly_deselect
                    (_this.el).on('plotly_deselect', function () {
                        _this.model.selected_data = null;
                    });
                    //  - plotly_unhover
                    (_this.el).on('plotly_unhover', function () {
                        _this.model.hover_data = null;
                    });
                }
                _this._plotInitialized = true;
                _this._reacting = false;
            });
        };
        PlotlyPlotView.prototype._get_trace = function (index, update) {
            var trace = object_1.clone(this.model.data[index]);
            var cds = this.model.data_sources[index];
            for (var _i = 0, _a = cds.columns(); _i < _a.length; _i++) {
                var column = _a[_i];
                var shape = cds._shapes[column][0];
                var array = cds.get_array(column)[0];
                if (shape.length > 1) {
                    var arrays = [];
                    for (var s = 0; s < shape[0]; s++) {
                        arrays.push(array.slice(s * shape[1], (s + 1) * shape[1]));
                    }
                    array = arrays;
                }
                var prop_path = column.split(".");
                var prop = prop_path[prop_path.length - 1];
                var prop_parent = trace;
                for (var _b = 0, _c = prop_path.slice(0, -1); _b < _c.length; _b++) {
                    var k = _c[_b];
                    prop_parent = prop_parent[k];
                }
                if (update && prop_path.length == 1) {
                    prop_parent[prop] = [array];
                }
                else {
                    prop_parent[prop] = array;
                }
            }
            return trace;
        };
        PlotlyPlotView.prototype._updateViewportFromProperty = function () {
            var _this = this;
            if (!Plotly || this._settingViewport || this._reacting || !this.model.viewport) {
                return;
            }
            var fullLayout = this.el._fullLayout;
            // Call relayout if viewport differs from fullLayout
            _.forOwn(this.model.viewport, function (value, key) {
                if (!_.isEqual(_.get(fullLayout, key), value)) {
                    var clonedViewport = _.cloneDeep(_this.model.viewport);
                    clonedViewport['_update_from_property'] = true;
                    Plotly.relayout(_this.el, clonedViewport);
                    return false;
                }
                else {
                    return true;
                }
            });
        };
        PlotlyPlotView.prototype._updateViewportProperty = function () {
            var fullLayout = this.el._fullLayout;
            var viewport = {};
            // Get range for all xaxis and yaxis properties
            for (var prop in fullLayout) {
                if (!fullLayout.hasOwnProperty(prop)) {
                    continue;
                }
                var maybe_axis = prop.slice(0, 5);
                if (maybe_axis === 'xaxis' || maybe_axis === 'yaxis') {
                    viewport[prop + '.range'] = _.cloneDeep(fullLayout[prop].range);
                }
            }
            if (!_.isEqual(viewport, this.model.viewport)) {
                this._setViewport(viewport);
            }
        };
        PlotlyPlotView.prototype._updateSetViewportFunction = function () {
            var _this = this;
            if (this.model.viewport_update_policy === "continuous" ||
                this.model.viewport_update_policy === "mouseup") {
                this._setViewport = function (viewport) {
                    if (!_this._settingViewport) {
                        _this._settingViewport = true;
                        _this.model.viewport = viewport;
                        _this._settingViewport = false;
                    }
                };
            }
            else {
                this._setViewport = _.throttle(function (viewport) {
                    if (!_this._settingViewport) {
                        _this._settingViewport = true;
                        _this.model.viewport = viewport;
                        _this._settingViewport = false;
                    }
                }, this.model.viewport_update_throttle);
            }
        };
        PlotlyPlotView.__name__ = "PlotlyPlotView";
        return PlotlyPlotView;
    }(html_box_1.HTMLBoxView));
    exports.PlotlyPlotView = PlotlyPlotView;
    var PlotlyPlot = /** @class */ (function (_super) {
        __extends(PlotlyPlot, _super);
        function PlotlyPlot(attrs) {
            return _super.call(this, attrs) || this;
        }
        PlotlyPlot.init_PlotlyPlot = function () {
            this.prototype.default_view = PlotlyPlotView;
            this.define({
                data: [p.Array, []],
                layout: [p.Any, {}],
                config: [p.Any, {}],
                data_sources: [p.Array, []],
                relayout_data: [p.Any, {}],
                restyle_data: [p.Array, []],
                click_data: [p.Any, {}],
                hover_data: [p.Any, {}],
                clickannotation_data: [p.Any, {}],
                selected_data: [p.Any, {}],
                viewport: [p.Any, {}],
                viewport_update_policy: [p.String, "mouseup"],
                viewport_update_throttle: [p.Number, 200],
                _render_count: [p.Number, 0],
            });
        };
        PlotlyPlot.__name__ = "PlotlyPlot";
        PlotlyPlot.__module__ = "panel.models.plotly";
        return PlotlyPlot;
    }(html_box_1.HTMLBox));
    exports.PlotlyPlot = PlotlyPlot;
    PlotlyPlot.init_PlotlyPlot();
},
"1d01be8a6e": /* models/progress.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var __assign = (this && this.__assign) || function () {
        __assign = Object.assign || function (t) {
            for (var s, i = 1, n = arguments.length; i < n; i++) {
                s = arguments[i];
                for (var p in s)
                    if (Object.prototype.hasOwnProperty.call(s, p))
                        t[p] = s[p];
            }
            return t;
        };
        return __assign.apply(this, arguments);
    };
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
},
"4cbc2c8e7e": /* models/state.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var view_1 = require("@bokehjs/core/view");
    var array_1 = require("@bokehjs/core/util/array");
    var model_1 = require("@bokehjs/model");
    var receiver_1 = require("@bokehjs/protocol/receiver");
    function get_json(file, callback) {
        var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
        xobj.open('GET', file, true);
        xobj.onreadystatechange = function () {
            if (xobj.readyState == 4 && xobj.status == 200) {
                callback(xobj.responseText);
            }
        };
        xobj.send(null);
    }
    var StateView = /** @class */ (function (_super) {
        __extends(StateView, _super);
        function StateView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        StateView.prototype.renderTo = function () {
        };
        StateView.__name__ = "StateView";
        return StateView;
    }(view_1.View));
    exports.StateView = StateView;
    var State = /** @class */ (function (_super) {
        __extends(State, _super);
        function State(attrs) {
            var _this = _super.call(this, attrs) || this;
            _this._receiver = new receiver_1.Receiver();
            _this._cache = {};
            return _this;
        }
        State.prototype.apply_state = function (state) {
            this._receiver.consume(state.header);
            this._receiver.consume(state.metadata);
            this._receiver.consume(state.content);
            if (this._receiver.message && this.document) {
                this.document.apply_json_patch(this._receiver.message.content);
            }
        };
        State.prototype._receive_json = function (result, path) {
            var state = JSON.parse(result);
            this._cache[path] = state;
            var current = this.state;
            for (var _i = 0, _a = this.values; _i < _a.length; _i++) {
                var i = _a[_i];
                current = current[i];
            }
            if (current === path)
                this.apply_state(state);
            else if (this._cache[current])
                this.apply_state(this._cache[current]);
        };
        State.prototype.set_state = function (widget, value) {
            var _this = this;
            var values = array_1.copy(this.values);
            var index = this.widgets[widget.id];
            values[index] = value;
            var state = this.state;
            for (var _i = 0, values_1 = values; _i < values_1.length; _i++) {
                var i = values_1[_i];
                state = state[i];
            }
            this.values = values;
            if (this.json) {
                if (this._cache[state]) {
                    this.apply_state(this._cache[state]);
                }
                else {
                    get_json(state, function (result) { return _this._receive_json(result, state); });
                }
            }
            else {
                this.apply_state(state);
            }
        };
        State.init_State = function () {
            this.prototype.default_view = StateView;
            this.define({
                json: [p.Boolean, false],
                state: [p.Any, {}],
                widgets: [p.Any, {}],
                values: [p.Any, []],
            });
        };
        State.__name__ = "State";
        State.__module__ = "panel.models.state";
        return State;
    }(model_1.Model));
    exports.State = State;
    State.init_State();
},
"780561860e": /* models/vega.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var html_box_1 = require("@bokehjs/models/layouts/html_box");
    var VegaPlotView = /** @class */ (function (_super) {
        __extends(VegaPlotView, _super);
        function VegaPlotView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        VegaPlotView.prototype.connect_signals = function () {
            var _this = this;
            _super.prototype.connect_signals.call(this);
            this.connect(this.model.properties.data.change, this._plot);
            this.connect(this.model.properties.data_sources.change, function () { return _this._connect_sources(); });
            this._connected = [];
            this._connect_sources();
        };
        VegaPlotView.prototype._connect_sources = function () {
            for (var ds in this.model.data_sources) {
                var cds = this.model.data_sources[ds];
                if (this._connected.indexOf(ds) < 0) {
                    this.connect(cds.properties.data.change, this._plot);
                    this._connected.push(ds);
                }
            }
        };
        VegaPlotView.prototype._fetch_datasets = function () {
            var datasets = {};
            for (var ds in this.model.data_sources) {
                var cds = this.model.data_sources[ds];
                var data = [];
                var columns = cds.columns();
                for (var i = 0; i < cds.data[columns[0]].length; i++) {
                    var item = {};
                    for (var _i = 0, columns_1 = columns; _i < columns_1.length; _i++) {
                        var column = columns_1[_i];
                        item[column] = cds.data[column][i];
                    }
                    data.push(item);
                }
                datasets[ds] = data;
            }
            return datasets;
        };
        VegaPlotView.prototype.render = function () {
            _super.prototype.render.call(this);
            this._plot();
        };
        VegaPlotView.prototype._plot = function () {
            if (!this.model.data || !window.vegaEmbed)
                return;
            if (this.model.data_sources && (Object.keys(this.model.data_sources).length > 0)) {
                var datasets = this._fetch_datasets();
                if ('data' in datasets) {
                    this.model.data.data['values'] = datasets['data'];
                    delete datasets['data'];
                }
                this.model.data['datasets'] = datasets;
            }
            window.vegaEmbed(this.el, this.model.data, { actions: false });
        };
        VegaPlotView.__name__ = "VegaPlotView";
        return VegaPlotView;
    }(html_box_1.HTMLBoxView));
    exports.VegaPlotView = VegaPlotView;
    var VegaPlot = /** @class */ (function (_super) {
        __extends(VegaPlot, _super);
        function VegaPlot(attrs) {
            return _super.call(this, attrs) || this;
        }
        VegaPlot.init_VegaPlot = function () {
            this.prototype.default_view = VegaPlotView;
            this.define({
                data: [p.Any],
                data_sources: [p.Any],
            });
        };
        VegaPlot.__name__ = "VegaPlot";
        VegaPlot.__module__ = "panel.models.vega";
        return VegaPlot;
    }(html_box_1.HTMLBox));
    exports.VegaPlot = VegaPlot;
    VegaPlot.init_VegaPlot();
},
"4a2dcd4d15": /* models/video.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var widget_1 = require("@bokehjs/models/widgets/widget");
    var VideoView = /** @class */ (function (_super) {
        __extends(VideoView, _super);
        function VideoView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        VideoView.prototype.initialize = function () {
            _super.prototype.initialize.call(this);
            this._blocked = false;
            this._time = Date.now();
        };
        VideoView.prototype.connect_signals = function () {
            var _this = this;
            _super.prototype.connect_signals.call(this);
            this.connect(this.model.change, function () { return _this.render(); });
            this.connect(this.model.properties.loop.change, function () { return _this.set_loop(); });
            this.connect(this.model.properties.paused.change, function () { return _this.set_paused(); });
            this.connect(this.model.properties.time.change, function () { return _this.set_time(); });
            this.connect(this.model.properties.value.change, function () { return _this.set_value(); });
            this.connect(this.model.properties.volume.change, function () { return _this.set_volume(); });
        };
        VideoView.prototype.render = function () {
            var _this = this;
            if (this.videoEl)
                return;
            this.videoEl = document.createElement('video');
            if (!this.model.sizing_mode || this.model.sizing_mode === 'fixed') {
                if (this.model.height)
                    this.videoEl.height = this.model.height;
                if (this.model.width)
                    this.videoEl.width = this.model.width;
            }
            this.videoEl.style.objectFit = 'fill';
            this.videoEl.style.minWidth = '100%';
            this.videoEl.style.minHeight = '100%';
            this.videoEl.controls = true;
            this.videoEl.src = this.model.value;
            this.videoEl.currentTime = this.model.time;
            this.videoEl.loop = this.model.loop;
            if (this.model.volume != null)
                this.videoEl.volume = this.model.volume / 100;
            else
                this.model.volume = this.videoEl.volume * 100;
            this.videoEl.onpause = function () { return _this.model.paused = true; };
            this.videoEl.onplay = function () { return _this.model.paused = false; };
            this.videoEl.ontimeupdate = function () { return _this.update_time(_this); };
            this.videoEl.onvolumechange = function () { return _this.update_volume(_this); };
            this.el.appendChild(this.videoEl);
            if (!this.model.paused)
                this.videoEl.play();
        };
        VideoView.prototype.update_time = function (view) {
            if ((Date.now() - view._time) < view.model.throttle)
                return;
            view._blocked = true;
            view.model.time = view.videoEl.currentTime;
            view._time = Date.now();
        };
        VideoView.prototype.update_volume = function (view) {
            view._blocked = true;
            view.model.volume = view.videoEl.volume * 100;
        };
        VideoView.prototype.set_loop = function () {
            this.videoEl.loop = this.model.loop;
        };
        VideoView.prototype.set_paused = function () {
            if (!this.videoEl.paused && this.model.paused)
                this.videoEl.pause();
            if (this.videoEl.paused && !this.model.paused)
                this.videoEl.play();
        };
        VideoView.prototype.set_volume = function () {
            if (this._blocked) {
                this._blocked = false;
                return;
            }
            if (this.model.volume != null)
                this.videoEl.volume = this.model.volume / 100;
        };
        VideoView.prototype.set_time = function () {
            if (this._blocked) {
                this._blocked = false;
                return;
            }
            this.videoEl.currentTime = this.model.time;
        };
        VideoView.prototype.set_value = function () {
            this.videoEl.src = this.model.value;
        };
        VideoView.__name__ = "VideoView";
        return VideoView;
    }(widget_1.WidgetView));
    exports.VideoView = VideoView;
    var Video = /** @class */ (function (_super) {
        __extends(Video, _super);
        function Video(attrs) {
            return _super.call(this, attrs) || this;
        }
        Video.init_Video = function () {
            this.prototype.default_view = VideoView;
            this.define({
                loop: [p.Boolean, false],
                paused: [p.Boolean, true],
                time: [p.Number, 0],
                throttle: [p.Number, 250],
                value: [p.Any, ''],
                volume: [p.Number, null],
            });
        };
        Video.__name__ = "Video";
        Video.__module__ = "panel.models.widgets";
        return Video;
    }(widget_1.Widget));
    exports.Video = Video;
    Video.init_Video();
},
"cbedefa11b": /* models/videostream.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var widget_1 = require("@bokehjs/models/widgets/widget");
    var VideoStreamView = /** @class */ (function (_super) {
        __extends(VideoStreamView, _super);
        function VideoStreamView() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.constraints = {
                'audio': false,
                'video': true
            };
            return _this;
        }
        VideoStreamView.prototype.initialize = function () {
            _super.prototype.initialize.call(this);
            if (this.model.timeout !== null) {
                this.set_timeout();
            }
        };
        VideoStreamView.prototype.connect_signals = function () {
            var _this = this;
            _super.prototype.connect_signals.call(this);
            this.connect(this.model.properties.snapshot.change, function () { return _this.set_timeout(); });
            this.connect(this.model.properties.snapshot.change, function () { return _this.snapshot(); });
            this.connect(this.model.properties.paused.change, function () { return _this.model.paused ? _this.videoEl.pause() : _this.videoEl.play(); });
        };
        VideoStreamView.prototype.set_timeout = function () {
            var _this = this;
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
            if (this.model.timeout !== null) {
                this.timer = setInterval(function () { return _this.snapshot(); }, this.model.timeout);
            }
        };
        VideoStreamView.prototype.snapshot = function () {
            this.canvasEl.width = this.videoEl.videoWidth;
            this.canvasEl.height = this.videoEl.videoHeight;
            var context = this.canvasEl.getContext('2d');
            if (context)
                context.drawImage(this.videoEl, 0, 0, this.canvasEl.width, this.canvasEl.height);
            this.model.value = this.canvasEl.toDataURL("image/" + this.model.format, 0.95);
        };
        VideoStreamView.prototype.remove = function () {
            _super.prototype.remove.call(this);
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null;
            }
        };
        VideoStreamView.prototype.render = function () {
            var _this = this;
            _super.prototype.render.call(this);
            if (this.videoEl)
                return;
            this.videoEl = document.createElement('video');
            if (!this.model.sizing_mode || this.model.sizing_mode === 'fixed') {
                if (this.model.height)
                    this.videoEl.height = this.model.height;
                if (this.model.width)
                    this.videoEl.width = this.model.width;
            }
            this.videoEl.style.objectFit = 'fill';
            this.videoEl.style.minWidth = '100%';
            this.videoEl.style.minHeight = '100%';
            this.canvasEl = document.createElement('canvas');
            this.el.appendChild(this.videoEl);
            if (navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia(this.constraints)
                    .then(function (stream) {
                    _this.videoEl.srcObject = stream;
                    if (!_this.model.paused) {
                        _this.videoEl.play();
                    }
                })
                    .catch(console.error);
            }
        };
        VideoStreamView.__name__ = "VideoStreamView";
        return VideoStreamView;
    }(widget_1.WidgetView));
    exports.VideoStreamView = VideoStreamView;
    var VideoStream = /** @class */ (function (_super) {
        __extends(VideoStream, _super);
        function VideoStream(attrs) {
            return _super.call(this, attrs) || this;
        }
        VideoStream.init_VideoStream = function () {
            this.prototype.default_view = VideoStreamView;
            this.define({
                format: [p.String, 'png'],
                paused: [p.Boolean, false],
                snapshot: [p.Boolean, false],
                timeout: [p.Number, null],
                value: [p.Any,]
            });
            this.override({
                height: 240,
                width: 320
            });
        };
        VideoStream.__name__ = "VideoStream";
        VideoStream.__module__ = "panel.models.widgets";
        return VideoStream;
    }(widget_1.Widget));
    exports.VideoStream = VideoStream;
    VideoStream.init_VideoStream();
},
"d4af2357ca": /* models/vtk.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
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
},
"64e1d58d42": /* models/vtkvolume.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
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
},
}, "55dac5102b", {"index":"55dac5102b","models/index":"1d13522e8a","models/ace":"c167e0e33e","models/audio":"d2f2f8c2b2","models/html":"cef8bc2777","models/katex":"7a3cc4b4c6","models/mathjax":"75803aafc7","models/player":"24a20e4790","models/plotly":"c864119ab3","models/progress":"1d01be8a6e","models/state":"4cbc2c8e7e","models/vega":"780561860e","models/video":"4a2dcd4d15","models/videostream":"cbedefa11b","models/vtk":"d4af2357ca","models/vtkvolume":"64e1d58d42"}, {});
})

//# sourceMappingURL=panel.js.map
