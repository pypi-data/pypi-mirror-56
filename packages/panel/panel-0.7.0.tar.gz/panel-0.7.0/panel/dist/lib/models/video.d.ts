import * as p from "@bokehjs/core/properties";
import { Widget, WidgetView } from "@bokehjs/models/widgets/widget";
export declare class VideoView extends WidgetView {
    model: Video;
    protected videoEl: HTMLVideoElement;
    protected dialogEl: HTMLElement;
    private _blocked;
    private _time;
    initialize(): void;
    connect_signals(): void;
    render(): void;
    update_time(view: VideoView): void;
    update_volume(view: VideoView): void;
    set_loop(): void;
    set_paused(): void;
    set_volume(): void;
    set_time(): void;
    set_value(): void;
}
export declare namespace Video {
    type Attrs = p.AttrsOf<Props>;
    type Props = Widget.Props & {
        loop: p.Property<boolean>;
        paused: p.Property<boolean>;
        time: p.Property<number>;
        throttle: p.Property<number>;
        value: p.Property<any>;
        volume: p.Property<number | null>;
    };
}
export interface Video extends Video.Attrs {
}
export declare abstract class Video extends Widget {
    properties: Video.Props;
    constructor(attrs?: Partial<Video.Attrs>);
    static __module__: string;
    static init_Video(): void;
}
