import * as p from "@bokehjs/core/properties";
import { Markup, MarkupView } from "@bokehjs/models/widgets/markup";
export declare class MathJaxView extends MarkupView {
    model: MathJax;
    private _hub;
    initialize(): void;
    render(): void;
}
export declare namespace MathJax {
    type Attrs = p.AttrsOf<Props>;
    type Props = Markup.Props & {
        text: p.Property<string>;
    };
}
export interface MathJax extends MathJax.Attrs {
}
export declare class MathJax extends Markup {
    properties: MathJax.Props;
    constructor(attrs?: Partial<MathJax.Attrs>);
    static __module__: string;
    static init_MathJax(): void;
}
