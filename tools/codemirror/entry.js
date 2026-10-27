// The run panel's code editor (W349): CodeMirror 6 with Python, bundled by
// tools/codemirror/build.sh into docs/javascripts/vendor/codemirror.min.js, which
// run-python.js loads on the first open of a run panel. It exposes window.dvqEditor.
import { EditorState, StateEffect, StateField, RangeSet } from "@codemirror/state";
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter,
         drawSelection, gutter, GutterMarker } from "@codemirror/view";
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { HighlightStyle, syntaxHighlighting, indentOnInput, bracketMatching } from "@codemirror/language";
import { python } from "@codemirror/lang-python";
import { tags as t } from "@lezer/highlight";

// The site's code colours (Material's variables, overridden in extra.css), so the editor
// matches the code blocks in both schemes.
const v = (name) => `var(--md-code-hl-${name}-color)`;
const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.controlKeyword, t.definitionKeyword, t.moduleKeyword, t.operatorKeyword], color: v("keyword") },
  { tag: [t.string, t.special(t.string)], color: v("string") },
  { tag: [t.number, t.bool, t.null], color: v("number") },
  { tag: t.comment, color: v("comment"), fontStyle: "italic" },
  { tag: [t.function(t.variableName), t.function(t.propertyName), t.definition(t.function(t.variableName))], color: v("function") },
  { tag: [t.className, t.definition(t.className)], color: v("constant") },
  { tag: [t.operator, t.punctuation, t.bracket], color: v("punctuation") },
  { tag: t.self, color: v("special") },
]);

const theme = EditorView.theme({
  "&": { fontSize: "0.72rem", backgroundColor: "var(--md-code-bg-color)", color: "var(--md-code-fg-color)",
         borderRadius: "var(--radius-s, 0.3rem)" },
  "&.cm-focused": { outline: "2px solid var(--site-focus-ring)", outlineOffset: "1px" },
  ".cm-scroller": { fontFamily: "var(--md-code-font-family)", lineHeight: "1.6", maxHeight: "26rem" },
  ".cm-content": { padding: "0.5rem 0", caretColor: "var(--md-code-fg-color)" },
  ".cm-gutters": { backgroundColor: "transparent", color: "var(--md-code-hl-comment-color)", border: "0" },
  ".cm-activeLine, .cm-activeLineGutter": { backgroundColor: "var(--md-code-hl-color--light)" },
  ".cm-dvq-mark": { width: "1.1em", textAlign: "center", fontWeight: "700" },
  ".cm-dvq-ok": { color: "var(--diff-easy)" },
  ".cm-dvq-bad": { color: "var(--adm-trap)" },
  ".cm-dvq-error-line": { backgroundColor: "color-mix(in srgb, var(--adm-trap) 16%, transparent)" },
});

// Check marks beside the print lines (W352): one marker per line, set after every run.
class Mark extends GutterMarker {
  constructor(ok, title) { super(); this.ok = ok; this.title = title; }
  eq(other) { return other.ok === this.ok && other.title === this.title; }
  toDOM() {
    const s = document.createElement("span");
    s.className = this.ok ? "cm-dvq-ok" : "cm-dvq-bad";
    s.textContent = this.ok ? "✓" : "✗";
    s.title = this.title;
    return s;
  }
}
const setMarks = StateEffect.define();
const marks = StateField.define({
  create: () => RangeSet.empty,
  update(value, tr) {
    value = value.map(tr.changes);
    for (const e of tr.effects) if (e.is(setMarks)) value = e.value;
    return tr.docChanged ? RangeSet.empty : value;     // an edit makes the old marks stale
  },
});
const markGutter = gutter({ class: "cm-dvq-mark", markers: (view) => view.state.field(marks) });

function create(parent, doc, { label, onRun }) {
  const view = new EditorView({
    parent,
    state: EditorState.create({
      doc,
      extensions: [
        lineNumbers(), highlightActiveLineGutter(), markGutter, marks, history(), drawSelection(),
        indentOnInput(), bracketMatching(), highlightActiveLine(), python(),
        syntaxHighlighting(highlight), theme, EditorState.tabSize.of(4),
        keymap.of([{ key: "Mod-Enter", run: () => { onRun(); return true; } },
                   indentWithTab, ...defaultKeymap, ...historyKeymap]),
        // tabindex 0 makes the editable content count as the scroll area's keyboard access
        // for axe (scrollable-region-focusable); it is the editor's own tab stop anyway
        EditorView.contentAttributes.of({ "aria-label": label, dir: "ltr", tabindex: "0" }),
      ],
    }),
  });
  return {
    view,
    get value() { return view.state.doc.toString(); },
    set value(text) { view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } }); },
    // [{ line, ok, title }]: a ✓ or ✗ in the gutter of each line
    setMarks(list) {
      const doc = view.state.doc;
      const ranges = list.filter((m) => m.line >= 1 && m.line <= doc.lines)
        .sort((a, b) => a.line - b.line)
        .map((m) => new Mark(m.ok, m.title).range(doc.line(m.line).from));
      view.dispatch({ effects: setMarks.of(RangeSet.of(ranges)) });
    },
    // put the cursor on a line, select it and scroll to it (an error's line number)
    goToLine(n) {
      const doc = view.state.doc;
      if (n < 1 || n > doc.lines) return;
      const line = doc.line(n);
      view.dispatch({ selection: { anchor: line.from, head: line.to }, scrollIntoView: true });
      view.focus();
    },
  };
}

window.dvqEditor = { create };
