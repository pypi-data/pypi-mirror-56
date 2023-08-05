import * as p from "@bokehjs/core/properties";
import { DType } from "@bokehjs/core/util/serialization";
import { HTMLBox, HTMLBoxView } from "@bokehjs/models/layouts/html_box";
declare type VolumeType = {
    buffer: string;
    dims: number[];
    dtype: DType;
    spacing: number[];
    origin: number[] | null;
    extent: number[] | null;
};
export declare class VTKVolumePlotView extends HTMLBoxView {
    model: VTKVolumePlot;
    protected _container: HTMLDivElement;
    protected _rendererEl: any;
    protected _controllerWidget: any;
    after_layout(): void;
    _create_source(): any;
    _plot(): void;
}
export declare namespace VTKVolumePlot {
    type Attrs = p.AttrsOf<Props>;
    type Props = HTMLBox.Props & {
        data: p.Property<VolumeType>;
        actor: p.Property<any>;
    };
}
export interface VTKVolumePlot extends VTKVolumePlot.Attrs {
}
export declare class VTKVolumePlot extends HTMLBox {
    properties: VTKVolumePlot.Props;
    constructor(attrs?: Partial<VTKVolumePlot.Attrs>);
    static __module__: string;
    static init_VTKVolumePlot(): void;
}
export {};
