"""Main application window for EasyBank."""

import gettext
import locale
import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Gdk", "4.0")

from gi.repository import Adw, Gdk, Gio, GLib, Gtk

from easybank.budget import (
    CATEGORIES,
    add_income,
    add_transaction,
    clear_transactions,
    get_balance,
    get_balance_fraction,
    get_expenses_by_category,
    get_total_expenses,
    load_budget,
    save_budget,
)
from easybank.icons import get_svg_bytes

# i18n setup
LOCALE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "po")
try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass

gettext.bindtextdomain("easybank", LOCALE_DIR)
gettext.textdomain("easybank")
_ = gettext.gettext


def _load_svg_paintable(icon_name, size=64):
    """Load an SVG icon as a Gdk.Texture."""
    svg_bytes = get_svg_bytes(icon_name)
    gbytes = GLib.Bytes.new(svg_bytes)
    try:
        texture = Gdk.Texture.new_from_bytes(gbytes)
        return texture
    except Exception:
        return None


def _make_icon_image(icon_name, size=64):
    """Create a Gtk.Image from an SVG icon name."""
    texture = _load_svg_paintable(icon_name, size)
    if texture:
        image = Gtk.Image.new_from_paintable(texture)
    else:
        image = Gtk.Image.new_from_icon_name("image-missing")
    image.set_pixel_size(size)
    return image


class EasyBankWindow(Adw.ApplicationWindow):
    """Main window for EasyBank budget application."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("EasyBank")
        self.set_default_size(500, 750)

        self.data = load_budget()

        # Main layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(self.main_box)

        # Header bar
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="EasyBank"))

        # New month button
        new_month_btn = Gtk.Button(label=_("New Month"))
        new_month_btn.add_css_class("destructive-action")
        new_month_btn.connect("clicked", self._on_new_month)
        header.pack_end(new_month_btn)

        self.main_box.append(header)

        # Warning bar (hidden by default)
        self.warning_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.warning_bar.set_margin_start(12)
        self.warning_bar.set_margin_end(12)
        self.warning_bar.set_margin_top(8)
        self.warning_bar.set_visible(False)
        self.warning_bar.add_css_class("warning-bar")
        self.main_box.append(self.warning_bar)

        # Scrollable content
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.main_box.append(scroll)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content.set_margin_start(16)
        content.set_margin_end(16)
        content.set_margin_top(16)
        content.set_margin_bottom(16)
        scroll.set_child(content)

        # === Balance section ===
        balance_frame = Gtk.Frame()
        balance_frame.add_css_class("card")
        balance_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        balance_box.set_margin_start(16)
        balance_box.set_margin_end(16)
        balance_box.set_margin_top(16)
        balance_box.set_margin_bottom(16)
        balance_frame.set_child(balance_box)
        content.append(balance_frame)

        # Mood icon shows financial status
        self.mood_image = _make_icon_image("happy", 72)
        balance_box.append(self.mood_image)

        # Balance label
        self.balance_label = Gtk.Label()
        self.balance_label.add_css_class("title-1")
        balance_box.append(self.balance_label)

        # Progress bar for balance
        self.balance_bar = Gtk.ProgressBar()
        self.balance_bar.set_show_text(False)
        self.balance_bar.set_size_request(-1, 24)
        balance_box.append(self.balance_bar)

        # Sub labels
        sub_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        sub_box.set_halign(Gtk.Align.CENTER)
        balance_box.append(sub_box)

        self.income_label = Gtk.Label()
        self.income_label.add_css_class("dim-label")
        sub_box.append(self.income_label)

        sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        sub_box.append(sep)

        self.expenses_label = Gtk.Label()
        self.expenses_label.add_css_class("dim-label")
        sub_box.append(self.expenses_label)

        # === Income section ===
        income_frame = Gtk.Frame()
        income_frame.add_css_class("card")
        income_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        income_box.set_margin_start(16)
        income_box.set_margin_end(16)
        income_box.set_margin_top(16)
        income_box.set_margin_bottom(16)
        income_frame.set_child(income_box)
        content.append(income_frame)

        income_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        income_header.append(_make_icon_image("money", 40))
        income_title = Gtk.Label(label=_("Income"))
        income_title.add_css_class("title-2")
        income_header.append(income_title)
        income_box.append(income_header)

        income_input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        income_box.append(income_input_box)

        self.income_spin = Gtk.SpinButton()
        self.income_spin.set_range(0, 999999)
        self.income_spin.set_increments(100, 1000)
        self.income_spin.set_digits(0)
        self.income_spin.set_value(self.data["income"])
        self.income_spin.set_hexpand(True)
        self.income_spin.set_size_request(-1, 48)
        income_input_box.append(self.income_spin)

        kr_label = Gtk.Label(label="kr")
        kr_label.add_css_class("title-3")
        income_input_box.append(kr_label)

        save_income_btn = Gtk.Button(label=_("Save"))
        save_income_btn.add_css_class("suggested-action")
        save_income_btn.set_size_request(100, 48)
        save_income_btn.connect("clicked", self._on_save_income)
        income_input_box.append(save_income_btn)

        # === Add expense section ===
        expense_frame = Gtk.Frame()
        expense_frame.add_css_class("card")
        expense_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        expense_box.set_margin_start(16)
        expense_box.set_margin_end(16)
        expense_box.set_margin_top(16)
        expense_box.set_margin_bottom(16)
        expense_frame.set_child(expense_box)
        content.append(expense_frame)

        expense_title = Gtk.Label(label=_("Add Expense"))
        expense_title.add_css_class("title-2")
        expense_title.set_halign(Gtk.Align.START)
        expense_box.append(expense_title)

        # Category buttons in a grid
        cat_grid = Gtk.FlowBox()
        cat_grid.set_max_children_per_line(4)
        cat_grid.set_min_children_per_line(3)
        cat_grid.set_selection_mode(Gtk.SelectionMode.SINGLE)
        cat_grid.set_homogeneous(True)
        cat_grid.set_row_spacing(8)
        cat_grid.set_column_spacing(8)
        expense_box.append(cat_grid)

        self.selected_category = None
        self.cat_buttons = {}

        for cat_id, cat_info in CATEGORIES.items():
            btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            btn_box.set_halign(Gtk.Align.CENTER)

            icon = _make_icon_image(cat_info["icon"], 48)
            btn_box.append(icon)

            label = Gtk.Label(label=cat_info["sv"])
            label.add_css_class("caption")
            btn_box.append(label)

            self.cat_buttons[cat_id] = btn_box
            cat_grid.append(btn_box)

        cat_grid.connect("child-activated", self._on_category_selected)

        # Amount input
        amount_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        expense_box.append(amount_box)

        self.expense_spin = Gtk.SpinButton()
        self.expense_spin.set_range(0, 99999)
        self.expense_spin.set_increments(10, 100)
        self.expense_spin.set_digits(0)
        self.expense_spin.set_hexpand(True)
        self.expense_spin.set_size_request(-1, 48)
        amount_box.append(self.expense_spin)

        kr_label2 = Gtk.Label(label="kr")
        kr_label2.add_css_class("title-3")
        amount_box.append(kr_label2)

        add_btn = Gtk.Button(label=_("Add"))
        add_btn.add_css_class("suggested-action")
        add_btn.set_size_request(120, 48)
        add_btn.connect("clicked", self._on_add_expense)
        amount_box.append(add_btn)

        # === Expenses breakdown ===
        breakdown_frame = Gtk.Frame()
        breakdown_frame.add_css_class("card")
        self.breakdown_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.breakdown_box.set_margin_start(16)
        self.breakdown_box.set_margin_end(16)
        self.breakdown_box.set_margin_top(16)
        self.breakdown_box.set_margin_bottom(16)
        breakdown_frame.set_child(self.breakdown_box)
        content.append(breakdown_frame)

        breakdown_title = Gtk.Label(label=_("Expenses"))
        breakdown_title.add_css_class("title-2")
        breakdown_title.set_halign(Gtk.Align.START)
        self.breakdown_box.append(breakdown_title)

        # Apply CSS
        self._apply_css()

        # Update display
        self._update_display()

    def _apply_css(self):
        css = b"""
        .balance-good progressbar > trough > progress {
            background-color: #4CAF50;
            border-radius: 8px;
            min-height: 20px;
        }
        .balance-ok progressbar > trough > progress {
            background-color: #FF9800;
            border-radius: 8px;
            min-height: 20px;
        }
        .balance-bad progressbar > trough > progress {
            background-color: #F44336;
            border-radius: 8px;
            min-height: 20px;
        }
        progressbar > trough {
            min-height: 20px;
            border-radius: 8px;
        }
        .warning-bar {
            background-color: #FFF3E0;
            border: 2px solid #E65100;
            border-radius: 12px;
            padding: 12px;
        }
        .warning-bar-critical {
            background-color: #FFEBEE;
            border: 2px solid #C62828;
            border-radius: 12px;
            padding: 12px;
        }
        spinbutton {
            font-size: 18px;
        }
        .title-1 {
            font-size: 28px;
        }
        .card {
            border-radius: 16px;
        }
        flowboxchild:selected {
            border-radius: 12px;
            outline: 3px solid @accent_color;
        }
        button.suggested-action, button.destructive-action {
            font-size: 16px;
            border-radius: 12px;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _update_display(self):
        """Refresh all display elements based on current data."""
        balance = get_balance(self.data)
        fraction = get_balance_fraction(self.data)
        total_expenses = get_total_expenses(self.data)

        # Balance label
        self.balance_label.set_text(f"{int(balance)} kr {_('kvar')}")

        # Progress bar
        self.balance_bar.set_fraction(fraction)

        # Remove old CSS classes
        for cls in ("balance-good", "balance-ok", "balance-bad"):
            self.balance_bar.remove_css_class(cls)

        # Set color and mood based on balance
        if fraction > 0.5:
            self.balance_bar.add_css_class("balance-good")
            self._set_mood("happy")
            self._hide_warning()
        elif fraction > 0.2:
            self.balance_bar.add_css_class("balance-ok")
            self._set_mood("happy")
            self._show_warning(
                _("You are running out of money. Please be careful!"),
                critical=False,
            )
        else:
            self.balance_bar.add_css_class("balance-bad")
            self._set_mood("sad")
            self._show_warning(
                _("Varning! Mycket lite pengar kvar!"),
                critical=True,
            )
            self._play_warning_sound()

        # Sub labels
        self.income_label.set_text(f"{_('Inkomst')}: {int(self.data['income'])} kr")
        self.expenses_label.set_text(f"{_('Utgifter')}: {int(total_expenses)} kr")

        # Update breakdown
        self._update_breakdown()

    def _set_mood(self, mood):
        """Update the mood icon."""
        parent = self.mood_image.get_parent()
        if parent:
            new_image = _make_icon_image(mood, 72)
            idx = 0
            child = parent.get_first_child()
            while child and child != self.mood_image:
                idx += 1
                child = child.get_next_sibling()
            parent.remove(self.mood_image)
            self.mood_image = new_image
            # Insert at position by re-adding (simplified: prepend)
            if idx == 0:
                parent.prepend(self.mood_image)
            else:
                parent.append(self.mood_image)

    def _show_warning(self, message, critical=False):
        """Show visual warning bar."""
        # Clear existing children
        child = self.warning_bar.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.warning_bar.remove(child)
            child = next_child

        self.warning_bar.remove_css_class("warning-bar")
        self.warning_bar.remove_css_class("warning-bar-critical")

        if critical:
            self.warning_bar.add_css_class("warning-bar-critical")
            icon = _make_icon_image("sad", 40)
        else:
            self.warning_bar.add_css_class("warning-bar")
            icon = _make_icon_image("warning", 40)

        self.warning_bar.append(icon)

        label = Gtk.Label(label=message)
        label.set_wrap(True)
        label.add_css_class("heading")
        self.warning_bar.append(label)

        self.warning_bar.set_visible(True)

    def _hide_warning(self):
        self.warning_bar.set_visible(False)

    def _play_warning_sound(self):
        """Play system bell as warning sound."""
        display = self.get_display()
        if display:
            display.beep()

    def _update_breakdown(self):
        """Update expense breakdown list."""
        # Remove old items (keep title)
        child = self.breakdown_box.get_first_child()
        first = True
        while child:
            next_child = child.get_next_sibling()
            if not first:
                self.breakdown_box.remove(child)
            first = False
            child = next_child

        expenses = get_expenses_by_category(self.data)
        if not expenses:
            empty_label = Gtk.Label(label=_("No expenditure yet"))
            empty_label.add_css_class("dim-label")
            self.breakdown_box.append(empty_label)
            return

        for cat_id, amount in sorted(expenses.items(), key=lambda x: -x[1]):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            row.set_margin_top(4)
            row.set_margin_bottom(4)

            cat_info = CATEGORIES.get(cat_id, CATEGORIES["other"])
            icon = _make_icon_image(cat_info["icon"], 36)
            row.append(icon)

            name = Gtk.Label(label=cat_info["sv"])
            name.set_hexpand(True)
            name.set_halign(Gtk.Align.START)
            name.add_css_class("heading")
            row.append(name)

            amount_label = Gtk.Label(label=f"{int(amount)} kr")
            amount_label.add_css_class("title-3")
            row.append(amount_label)

            self.breakdown_box.append(row)

    def _on_save_income(self, button):
        amount = self.income_spin.get_value()
        self.data = add_income(self.data, amount)
        self._update_display()

    def _on_category_selected(self, flowbox, child):
        """Store selected category."""
        idx = child.get_index()
        cat_ids = list(CATEGORIES.keys())
        if 0 <= idx < len(cat_ids):
            self.selected_category = cat_ids[idx]

    def _on_add_expense(self, button):
        amount = self.expense_spin.get_value()
        if amount <= 0:
            return
        category = self.selected_category or "other"
        self.data = add_transaction(self.data, amount, category)
        self.expense_spin.set_value(0)
        self._update_display()

    def _on_new_month(self, button):
        """Reset transactions for a new month."""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=_("New month?"),
            body=_("Do you want to remove all expenses and start over?"),
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("confirm", _("Yes, start over"))
        dialog.set_response_appearance("confirm", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", self._on_new_month_response)
        dialog.present()

    def _on_new_month_response(self, dialog, response):
        if response == "confirm":
            self.data = clear_transactions(self.data)
            self._update_display()
