"""Resolve merge-conflict hunks: keep XueLuoPDF branding, take upstream 0.7.1 logic.

Each entry is (file, list of resolutions), where a resolution is the exact text of one conflict
hunk (from `<<<<<<<` to `>>>>>>>`, inclusive) and the text that replaces it.
"""
import io
import os

ROOT = r"D:\sakura\sakura_homework\XueLuoPDF"

RESOLUTIONS = {
    "crates/annot/src/lib.rs": [(
        """<<<<<<< HEAD
    let d = annot_dict(doc, r);
    let drawn_elsewhere =
        d.get(b"AP").is_some_and(|ap| doc.resolve(ap).as_dict().is_some_and(|ap| ap.contains(b"N"))) && pdfcraft_fonts::undrawn_mark(&d).is_none();
    if drawn_elsewhere && let Some((what, c)) = appearance::undrawable_text(&d) {
        return Err(AnnotError::Undrawable(format!(
            "XueLuoPDF can't redraw this comment: the standard fonts can't draw \\"{}\\" (U+{:04X}) in {what}, which would then show as ? (the comment was left as it is)",
            c.escape_debug(),
            u32::from(c)
        )));
    }
=======
    refuse_foreign_text(doc, &annot_dict(doc, r))?;
>>>>>>> main""",
        "    refuse_foreign_text(doc, &annot_dict(doc, r))?;",
    )],
    "crates/automation/src/tools.rs": [(
        """<<<<<<< HEAD
        t("link_open", "Open a linked PDF", "Follow a local GoToR link in XueLuoPDF: open the referenced PDF as a new document, respecting --root. page and index use link_list numbering. Named destinations are reported but not applied.")
=======
        t("link_open", "Open a linked PDF", "Follow a local GoToR link in PdfCraft: open the referenced PDF as a new document, respecting --root. page and index use link_list numbering. Named destinations are reported but not applied. Absolute file specifications require allow_absolute: true after reviewing the target; relative links need no opt-in.")
>>>>>>> main""",
        """        t("link_open", "Open a linked PDF", "Follow a local GoToR link in XueLuoPDF: open the referenced PDF as a new document, respecting --root. page and index use link_list numbering. Named destinations are reported but not applied. Absolute file specifications require allow_absolute: true after reviewing the target; relative links need no opt-in.")""",
    )],
    "crates/ui-egui/src/chrome.rs": [(
        """<<<<<<< HEAD
use crate::{Dialog, Mode, XueLuoPDFApp, PropsTab, RightPanel, icons, widgets};
=======
use crate::{Dialog, Mode, PdfCraftApp, PropsTab, RightPanel, icons, widgets, window_controls};
>>>>>>> main""",
        "use crate::{Dialog, Mode, XueLuoPDFApp, PropsTab, RightPanel, icons, widgets, window_controls};",
    )],
    "crates/ui-egui/src/combine_grid.rs": [(
        """<<<<<<< HEAD
pub(crate) fn grid(app: &mut XueLuoPDFApp, ui: &mut egui::Ui, t: &Tokens, checks: &[Result<usize, String>], selected: &[bool]) -> Option<RowAction> {
=======
pub(crate) fn grid(
    app: &mut PdfCraftApp,
    ui: &mut egui::Ui,
    t: &Tokens,
    checks: &[Result<usize, String>],
    selected: &[bool],
    twice: &[bool],
) -> Option<RowAction> {
>>>>>>> main""",
        """pub(crate) fn grid(
    app: &mut XueLuoPDFApp,
    ui: &mut egui::Ui,
    t: &Tokens,
    checks: &[Result<usize, String>],
    selected: &[bool],
    twice: &[bool],
) -> Option<RowAction> {""",
    )],
    "crates/ui-egui/src/dialogs.rs": [(
        """<<<<<<< HEAD
                                ui.label(egui::RichText::new(pdfcraft_engine::links::APP_NAME).font(theme::semibold(20.0)));
                                ui.label(crate::i18n::fmt(tl!("Version {v}"), &[("v", env!("CARGO_PKG_VERSION"))]));
=======
                                ui.label(egui::RichText::new("PdfCraft").font(theme::semibold(20.0)));
                                ui.label(crate::i18n::fmt(tl!("Version {v}"), &[("v", &pdfcraft_engine::build_info::version())]));
>>>>>>> main""",
        """                                ui.label(egui::RichText::new(pdfcraft_engine::links::APP_NAME).font(theme::semibold(20.0)));
                                ui.label(crate::i18n::fmt(tl!("Version {v}"), &[("v", &pdfcraft_engine::build_info::version())]));""",
    )],
    "crates/ui-egui/tests/content.rs": [(
        """<<<<<<< HEAD
fn harness() -> Harness<'static, XueLuoPDFApp> {
    let mut h = Harness::builder().with_size(egui::vec2(1400.0, 900.0)).build_eframe(|_cc| {
        let mut app = XueLuoPDFApp::new();
=======
fn harness() -> Harness<'static, PdfCraftApp> {
    harness_bytes(include_bytes!("data/form.pdf").to_vec())
}

fn harness_bytes(bytes: Vec<u8>) -> Harness<'static, PdfCraftApp> {
    let mut h = Harness::builder().with_size(egui::vec2(1400.0, 900.0)).build_eframe(move |_cc| {
        let mut app = PdfCraftApp::new();
>>>>>>> main""",
        """fn harness() -> Harness<'static, XueLuoPDFApp> {
    harness_bytes(include_bytes!("data/form.pdf").to_vec())
}

fn harness_bytes(bytes: Vec<u8>) -> Harness<'static, XueLuoPDFApp> {
    let mut h = Harness::builder().with_size(egui::vec2(1400.0, 900.0)).build_eframe(move |_cc| {
        let mut app = XueLuoPDFApp::new();""",
    )],
    "crates/ui-egui/tests/ui_group/text_select.rs": [(
        """<<<<<<< HEAD
fn harness(setup: impl FnOnce(&mut XueLuoPDFApp) + 'static) -> (Harness<'static, XueLuoPDFApp>, Pos2) {
=======
fn harness(setup: impl FnOnce(&mut PdfCraftApp) + 'static) -> (Harness<'static, PdfCraftApp>, Pos2) {
    harness_with(two_lines(), setup)
}

/// `harness` with another document; the pointer ends over glyph 5 of its first page.
fn harness_with(pdf: Vec<u8>, setup: impl FnOnce(&mut PdfCraftApp) + 'static) -> (Harness<'static, PdfCraftApp>, Pos2) {
>>>>>>> main""",
        """fn harness(setup: impl FnOnce(&mut XueLuoPDFApp) + 'static) -> (Harness<'static, XueLuoPDFApp>, Pos2) {
    harness_with(two_lines(), setup)
}

/// `harness` with another document; the pointer ends over glyph 5 of its first page.
fn harness_with(pdf: Vec<u8>, setup: impl FnOnce(&mut XueLuoPDFApp) + 'static) -> (Harness<'static, XueLuoPDFApp>, Pos2) {""",
    )],
    "crates/ui-egui/tests/ui_group/xfa.rs": [(
        """<<<<<<< HEAD
    for _ in 0..40 {
        h.run_steps(2);
        if !h.state().render_pending() {
            break;
        }
        std::thread::sleep(std::time::Duration::from_millis(5));
    }
    let names = |h: &Harness<'static, XueLuoPDFApp>| {
=======
    wait_for_pages(&mut h);
    let names = |h: &Harness<'static, PdfCraftApp>| {
>>>>>>> main""",
        """    wait_for_pages(&mut h);
    let names = |h: &Harness<'static, XueLuoPDFApp>| {""",
    )],
}

for rel, pairs in RESOLUTIONS.items():
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    for old, new in pairs:
        if old not in text:
            raise SystemExit(f"NOT FOUND in {rel}: {old.splitlines()[0][:70]!r}")
        text = text.replace(old, new, 1)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

print("resolved:", len(RESOLUTIONS), "files")
left = []
for rel in RESOLUTIONS:
    path = os.path.join(ROOT, rel)
    with io.open(path, encoding="utf-8", newline="") as f:
        n = f.read().count("\n<<<<<<< ")
    if n:
        left.append((rel, n))
print("still conflicted:", left)
