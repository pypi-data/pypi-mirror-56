import * as p from "@bokehjs/core/properties";
import { Markup, MarkupView } from "@bokehjs/models/widgets/markup";
export declare class KaTeXView extends MarkupView {
    model: KaTeX;
    render(): void;
}
export declare namespace KaTeX {
    type Attrs = p.AttrsOf<Props>;
    type Props = Markup.Props & {
        text: p.Property<string>;
    };
}
export interface KaTeX extends KaTeX.Attrs {
}
export declare class KaTeX extends Markup {
    properties: KaTeX.Props;
    constructor(attrs?: Partial<KaTeX.Attrs>);
    static __module__: string;
    static init_KaTeX(): void;
}
