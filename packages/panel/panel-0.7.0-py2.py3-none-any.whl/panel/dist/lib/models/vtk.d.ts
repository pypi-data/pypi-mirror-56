import * as p from "@bokehjs/core/properties";
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
export declare class VTKPlotView extends HTMLBoxView {
    model: VTKPlot;
    protected _container: HTMLDivElement;
    protected _rendererEl: any;
    protected _renderer: any;
    protected _camera: any;
    protected _interactor: any;
    protected _setting: boolean;
    protected _orientationWidget: any;
    protected _widgetManager: any;
    initialize(): void;
    _create_orientation_widget(): void;
    after_layout(): void;
    _orientation_widget_visbility(visbility: boolean): void;
    connect_signals(): void;
    _remove_default_key_binding(): void;
    _get_camera_state(): void;
    _set_camera_state(): void;
    _plot(): void;
    _delete_all_actors(): void;
}
export declare namespace VTKPlot {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        data: p.Property<string>;
        camera: p.Property<any>;
        enable_keybindings: p.Property<boolean>;
        orientation_widget: p.Property<boolean>;
    };
}
export interface VTKPlot extends VTKPlot.Attrs {
}
export declare class VTKPlot extends HTMLBox {
    properties: VTKPlot.Props;
    renderer_el: any;
    outline: any;
    outline_actor: any;
    constructor(attrs?: Partial<VTKPlot.Attrs>);
    getActors(): [any];
    static __module__: string;
    static init_VTKPlot(): void;
}
