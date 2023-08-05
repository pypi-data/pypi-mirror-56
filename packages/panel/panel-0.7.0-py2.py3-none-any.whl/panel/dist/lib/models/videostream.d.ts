import * as p from "@bokehjs/core/properties";
import { Widget, WidgetView } from "@bokehjs/models/widgets/widget";
export declare class VideoStreamView extends WidgetView {
    model: VideoStream;
    protected videoEl: HTMLVideoElement;
    protected canvasEl: HTMLCanvasElement;
    protected constraints: {
        'audio': boolean;
        'video': boolean;
    };
    protected timer: any;
    initialize(): void;
    connect_signals(): void;
    set_timeout(): void;
    snapshot(): void;
    remove(): void;
    render(): void;
}
export declare namespace VideoStream {
    type Attrs = p.AttrsOf<Props>;
    type Props = Widget.Props & {
        format: p.Property<string>;
        paused: p.Property<boolean>;
        snapshot: p.Property<boolean>;
        timeout: p.Property<number | null>;
        value: p.Property<any>;
    };
}
export interface VideoStream extends VideoStream.Attrs {
}
export declare abstract class VideoStream extends Widget {
    properties: VideoStream.Props;
    constructor(attrs?: Partial<VideoStream.Attrs>);
    static __module__: string;
    static init_VideoStream(): void;
}
