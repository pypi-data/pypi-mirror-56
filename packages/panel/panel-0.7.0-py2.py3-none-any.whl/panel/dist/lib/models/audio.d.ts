import * as p from "@bokehjs/core/properties";
import { Widget, WidgetView } from "@bokehjs/models/widgets/widget";
export declare class AudioView extends WidgetView {
    model: Audio;
    protected audioEl: HTMLAudioElement;
    protected dialogEl: HTMLElement;
    private _blocked;
    private _time;
    initialize(): void;
    connect_signals(): void;
    render(): void;
    update_time(view: AudioView): void;
    update_volume(view: AudioView): void;
    set_loop(): void;
    set_paused(): void;
    set_volume(): void;
    set_time(): void;
    set_value(): void;
}
export declare namespace Audio {
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
export interface Audio extends Audio.Attrs {
}
export declare abstract class Audio extends Widget {
    properties: Audio.Props;
    constructor(attrs?: Partial<Audio.Attrs>);
    static __module__: string;
    static init_Audio(): void;
}
