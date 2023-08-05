import * as p from "@bokehjs/core/properties";
import { Widget, WidgetView } from "@bokehjs/models/widgets/widget";
export declare class ProgressView extends WidgetView {
    model: Progress;
    protected progressEl: HTMLProgressElement;
    connect_signals(): void;
    render(): void;
    setCSS(): void;
    setValue(): void;
    setMax(): void;
    _update_layout(): void;
}
export declare namespace Progress {
    type Attrs = p.AttrsOf<Props>;
    type Props = Widget.Props & {
        active: p.Property<boolean>;
        bar_color: p.Property<string>;
        style: p.Property<{
            [key: string]: string;
        }>;
        max: p.Property<number | null>;
        value: p.Property<number | null>;
    };
}
export interface Progress extends Progress.Attrs {
}
export declare class Progress extends Widget {
    properties: Progress.Props;
    constructor(attrs?: Partial<Progress.Attrs>);
    static __module__: string;
    static init_Progress(): void;
}
