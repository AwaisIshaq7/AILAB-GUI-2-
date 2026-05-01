import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

BG        = "#000000"
CARD      = "#16213e"
FIELD_BG  = "#0f3460"
ACCENT    = "#e94560"
GOLD      = "#f5a623"
TEXT      = "#87CEEB"
MUTED     = "#8899aa"
GREEN     = "#00c896"
BORDER    = "#87CEEB"
WHITE     = "#ffffff"
RECEIPT   = "#fdfdf5"
REC_TEXT  = "#1a1a1a"

PRODUCTS = {
    "Rice (1kg)":         120,
    "Sugar (1kg)":        900,
    "Cooking Oil (1L)":   280,
    "Wheat Flour (1kg)":   80,
    "Milk (1L)":          200,
    "Tea Bags (100pcs)":  350,
    "Biscuits (Pack)":    110,
    "Eggs (Dozen)":       280,
    "Soap Bar":            60,
    "Shampoo (200ml)":    320,
}

# ── AI Rule 1 : Related item suggestions ─────────────────────
SUGGESTIONS = {
    "Rice (1kg)":         "Cooking Oil (1L)  or  Lentils",
    "Sugar (1kg)":        "Tea Bags (100pcs)  or  Biscuits (Pack)",
    "Cooking Oil (1L)":   "Rice (1kg)  or  Wheat Flour (1kg)",
    "Wheat Flour (1kg)":  "Cooking Oil (1L)  or  Sugar (1kg)",
    "Milk (1L)":          "Tea Bags (100pcs)  or  Biscuits (Pack)",
    "Tea Bags (100pcs)":  "Milk (1L)  or  Sugar (1kg)",
    "Biscuits (Pack)":    "Tea Bags (100pcs)  or  Milk (1L)",
    "Eggs (Dozen)":       "Cooking Oil (1L)  or  Wheat Flour (1kg)",
    "Soap Bar":           "Shampoo (200ml)",
    "Shampoo (200ml)":    "Soap Bar",
}

# ── AI Rule 2 : Discount logic ───────────────────────────────
def get_discount(subtotal, qty):
    """
    Rule-based AI decision for discount:
      qty  >= 10           →  15%  Bulk Purchase Discount
      total >= 2000        →  10%  Loyalty Discount
      total >= 1000        →   5%  Standard Discount
      otherwise            →   0%  No Discount
    Returns (percentage, rule label)
    """
    if qty >= 10:
        return 15, "Bulk Purchase (qty >= 10)"
    elif subtotal >= 2000:
        return 10, "Loyalty Discount (total >= PKR 2,000)"
    elif subtotal >= 1000:
        return 5,  "Standard Discount (total >= PKR 1,000)"
    else:
        return 0,  "No Discount Applicable"

# Tax rate (fixed)
TAX_RATE = 0.05   # 5% sales tax

root = tk.Tk()
root.title("Smart Billing System")
root.geometry("920x660")
root.configure(bg=BG)
root.resizable(False, False)

# ── Thin accent bar at top ───────────────────────────────────
tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")

# ── Header bar ───────────────────────────────────────────────
header = tk.Frame(root, bg=CARD, pady=10)
header.pack(fill="x")

tk.Label(
    header,
    text="🛒  Smart Billing System",
    font=("Georgia", 16, "bold"),
    bg=CARD, fg=TEXT
).pack(side="left", padx=22)

tk.Label(
    header,
    text="AI-Based Decision Rules  •  Grocery & Retail",
    font=("Courier", 9),
    bg=CARD, fg=MUTED
).pack(side="left")

# Live clock (professional feature – date/time display)
clock_var = tk.StringVar()
tk.Label(
    header,
    textvariable=clock_var,
    font=("Courier", 9),
    bg=CARD, fg=GOLD
).pack(side="right", padx=22)

def tick():
    clock_var.set(datetime.now().strftime("%d %b %Y   %I:%M:%S %p"))
    root.after(1000, tick)

tick()

tk.Frame(root, bg=ACCENT, height=2).pack(fill="x")

body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True, padx=16, pady=12)

# Left panel – input form
left = tk.Frame(body, bg=CARD)
left.pack(side="left", fill="both", expand=True, padx=(0, 8))

# Right panel – receipt preview
right = tk.Frame(body, bg=RECEIPT)
right.pack(side="left", fill="both", expand=True, padx=(8, 0))

def section_heading(parent, text):
    tk.Label(
        parent, text=text,
        font=("Georgia", 10, "bold"),
        bg=CARD, fg=GOLD
    ).pack(anchor="w", padx=18, pady=(14, 2))
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=18, pady=(0, 8))

# ── Helper : labelled entry field ────────────────────────────
def labelled_entry(parent, label_text):
    tk.Label(
        parent, text=label_text,
        font=("Courier", 9),
        bg=CARD, fg=MUTED
    ).pack(anchor="w", padx=18)

    box = tk.Frame(
        parent, bg=FIELD_BG,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    box.pack(fill="x", padx=18, pady=(3, 9))

    entry = tk.Entry(
        box,
        font=("Courier", 11),
        bg=FIELD_BG, fg=TEXT,
        insertbackground=ACCENT,
        relief="flat", bd=7
    )
    entry.pack(fill="x")
    return entry

# ── Helper : styled button with hover ────────────────────────
def make_button(parent, text, command, bg_color, hover_color, width=12):
    btn = tk.Button(
        parent, text=text, command=command,
        font=("Georgia", 10, "bold"),
        bg=bg_color, fg=WHITE,
        activebackground=hover_color,
        activeforeground=WHITE,
        relief="flat", padx=10, pady=8,
        cursor="hand2", width=width
    )
    btn.pack(side="left", padx=5)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    return btn

# ════════════════════════════════════════════════════════════
#  LEFT PANEL CONTENTS
# ════════════════════════════════════════════════════════════

# ── Customer information section ─────────────────────────────
section_heading(left, "  Customer Information")
name_entry    = labelled_entry(left, "Customer Name")
contact_entry = labelled_entry(left, "Contact Number")

# ── Product selection section ────────────────────────────────
section_heading(left, "  Product Selection")

tk.Label(left, text="Select Item",
         font=("Courier", 9), bg=CARD, fg=MUTED).pack(anchor="w", padx=18)

# Combobox styling
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Dark.TCombobox",
    fieldbackground=FIELD_BG,
    background=FIELD_BG,
    foreground=TEXT,
    arrowcolor=ACCENT,
    bordercolor=BORDER,
    selectbackground=FIELD_BG,
    selectforeground=TEXT
)

product_var = tk.StringVar(value=list(PRODUCTS.keys())[0])
combo = ttk.Combobox(
    left,
    textvariable=product_var,
    values=list(PRODUCTS.keys()),
    state="readonly",
    font=("Courier", 11),
    style="Dark.TCombobox"
)
combo.pack(fill="x", padx=18, pady=(3, 9))

qty_entry = labelled_entry(left, "Quantity")

# Unit price display (updates with product selection)
price_display = tk.StringVar(value=f"Unit Price:  PKR {list(PRODUCTS.values())[0]:,.0f}")
tk.Label(
    left, textvariable=price_display,
    font=("Courier", 9, "bold"),
    bg=CARD, fg=GREEN
).pack(anchor="w", padx=18)

# AI suggestion display
suggestion_var = tk.StringVar()
tk.Label(
    left, textvariable=suggestion_var,
    font=("Courier", 8, "italic"),
    bg=CARD, fg=GOLD,
    wraplength=340, justify="left"
).pack(anchor="w", padx=18, pady=(3, 0))

# Update price + suggestion when item changes
def on_product_change(event=None):
    item  = product_var.get()
    price = PRODUCTS[item]
    price_display.set(f"Unit Price:  PKR {price:,.0f}")
    suggestion_var.set(f"💡 AI Tip: You may also need → {SUGGESTIONS[item]}")

combo.bind("<<ComboboxSelected>>", on_product_change)
on_product_change()   # set initial values

# ── Validation message ───────────────────────────────────────
val_var = tk.StringVar()
val_label = tk.Label(
    left, textvariable=val_var,
    font=("Courier", 8),
    bg=CARD, fg=ACCENT,
    wraplength=340, justify="left"
)
val_label.pack(anchor="w", padx=18, pady=(10, 0))

# ── Action buttons ───────────────────────────────────────────
btn_frame = tk.Frame(left, bg=CARD)
btn_frame.pack(fill="x", padx=18, pady=14)

# ════════════════════════════════════════════════════════════
#  BILLING LOGIC
# ════════════════════════════════════════════════════════════
def generate_bill():
    """Validate inputs, apply AI rules, calculate bill, render receipt."""
    val_var.set("")

    # Read inputs
    name     = name_entry.get().strip()
    contact  = contact_entry.get().strip()
    item     = product_var.get()
    qty_text = qty_entry.get().strip()

    # ── Input validation ─────────────────────────────────────
    if not name:
        val_var.set("⚠  Customer name is required.")
        return
    if any(ch.isdigit() for ch in name):
        val_var.set("⚠  Name must not contain numbers.")
        return
    if not contact:
        val_var.set("⚠  Contact number is required.")
        return
    if not contact.isdigit() or len(contact) < 10:
        val_var.set("⚠  Contact must be numeric and at least 10 digits.")
        return
    if not qty_text:
        val_var.set("⚠  Quantity is required.")
        return
    try:
        qty = int(qty_text)
        if qty <= 0:
            raise ValueError
    except ValueError:
        val_var.set("⚠  Quantity must be a positive whole number.")
        return

    # ── Billing calculations ──────────────────────────────────
    unit_price   = PRODUCTS[item]
    subtotal     = unit_price * qty                     # before discount & tax

    disc_pct, disc_rule = get_discount(subtotal, qty)   # AI discount rule
    disc_amount  = round(subtotal * disc_pct / 100, 2)

    after_disc   = subtotal - disc_amount
    tax_amount   = round(after_disc * TAX_RATE, 2)     # 5% tax on discounted price
    final_total  = round(after_disc + tax_amount, 2)

    bill_no      = f"SB-{datetime.now().strftime('%H%M%S')}"
    date_time    = datetime.now().strftime("%d %b %Y   %I:%M %p")
    suggestion   = SUGGESTIONS.get(item, "—")

    # ── Receipt generation ────────────────────────────────────
    receipt.config(state="normal")
    receipt.delete("1.0", tk.END)

    L  = "─" * 40
    DL = "═" * 40

    receipt.insert(tk.END, f"\n{'SMART BILLING SYSTEM':^40}\n",   "title")
    receipt.insert(tk.END, f"{'Grocery & Retail Store':^40}\n",    "sub")
    receipt.insert(tk.END, f"{DL}\n",                              "sep")
    receipt.insert(tk.END, f" Bill No   : {bill_no}\n",            "info")
    receipt.insert(tk.END, f" Date/Time : {date_time}\n",          "info")
    receipt.insert(tk.END, f"{L}\n",                               "sep")
    receipt.insert(tk.END, f" Customer  : {name}\n",               "info")
    receipt.insert(tk.END, f" Contact   : {contact}\n",            "info")
    receipt.insert(tk.END, f"{L}\n",                               "sep")
    receipt.insert(tk.END, f" Item      : {item}\n",               "info")
    receipt.insert(tk.END, f" Qty       : {qty} unit(s)\n",        "info")
    receipt.insert(tk.END, f" Unit Price: PKR {unit_price:>8,.2f}\n", "info")
    receipt.insert(tk.END, f"{L}\n",                               "sep")
    receipt.insert(tk.END, f" Subtotal  : PKR {subtotal:>8,.2f}\n","info")

    # Discount row
    if disc_pct > 0:
        receipt.insert(tk.END, f"\n ✦ AI RULE APPLIED\n",             "ai_head")
        receipt.insert(tk.END, f"   {disc_rule}\n",                    "ai_body")
        receipt.insert(tk.END, f" Discount  : -{disc_pct}%"
                               f"   PKR {disc_amount:>7,.2f}\n",       "disc")
    else:
        receipt.insert(tk.END, f"\n ✦ AI: {disc_rule}\n",             "nodis")

    # Tax row
    receipt.insert(tk.END, f" Tax (5%)  : PKR {tax_amount:>8,.2f}\n", "tax")
    receipt.insert(tk.END, f"\n{DL}\n",                               "sep")
    receipt.insert(tk.END, f" TOTAL     : PKR {final_total:>8,.2f}\n","total")
    receipt.insert(tk.END, f"{DL}\n",                                 "sep")

    # AI suggestion
    receipt.insert(tk.END, f"\n 💡 AI Suggestion:\n",                 "ai_head")
    receipt.insert(tk.END, f"    {suggestion}\n",                     "ai_body")
    receipt.insert(tk.END, f"\n{'Thank you for shopping!':^40}\n",    "sub")
    receipt.insert(tk.END, f"{'Please visit again.':^40}\n",          "sub")

    receipt.config(state="disabled")


# ── Clear / Reset all fields and receipt ─────────────────────
def clear_all():
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    product_var.set(list(PRODUCTS.keys())[0])
    on_product_change()
    val_var.set("")
    receipt.config(state="normal")
    receipt.delete("1.0", tk.END)
    receipt.insert(tk.END,
        "\n\n\n      Fill in the form and click\n"
        "      Generate Bill  to see\n"
        "      the receipt here.")
    receipt.config(state="disabled")


# ── Exit with confirmation (professional feature) ─────────────
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit the billing system?"):
        root.destroy()


# Place buttons
make_button(btn_frame, "Generate Bill", generate_bill, ACCENT,    "#c73652", width=14)
make_button(btn_frame, "Clear",         clear_all,     FIELD_BG,  "#0a2a4a", width=9)
make_button(btn_frame, "Exit",          exit_app,      "#2a2a3e", "#3a3a4e", width=7)

# ════════════════════════════════════════════════════════════
#  RIGHT PANEL CONTENTS  –  Receipt Text widget
# ════════════════════════════════════════════════════════════
tk.Label(
    right, text="  RECEIPT PREVIEW",
    font=("Georgia", 10, "bold"),
    bg=RECEIPT, fg=REC_TEXT
).pack(anchor="w", padx=12, pady=(10, 2))

tk.Frame(right, bg="#ccccbb", height=1).pack(fill="x", padx=12)

# Text widget for receipt (read-only to user)
receipt = tk.Text(
    right,
    font=("Courier", 10),
    bg=RECEIPT, fg=REC_TEXT,
    relief="flat", bd=0,
    padx=10, pady=10,
    state="disabled",
    wrap="word",
    cursor="arrow"
)
receipt.pack(fill="both", expand=True, padx=12, pady=8)

# Receipt text tags for styled output
receipt.tag_config("title",   font=("Georgia", 12, "bold"), foreground="#1a1a1a")
receipt.tag_config("sub",     font=("Courier", 9),          foreground="#666655")
receipt.tag_config("sep",                                   foreground="#aaaaaa")
receipt.tag_config("info",                                  foreground=REC_TEXT)
receipt.tag_config("total",   font=("Georgia", 13, "bold"), foreground="#c0392b")
receipt.tag_config("ai_head", font=("Courier", 9, "bold"),  foreground="#0f6e4e")
receipt.tag_config("ai_body", font=("Courier", 9, "italic"),foreground="#0f6e4e")
receipt.tag_config("disc",    font=("Courier", 10, "bold"), foreground="#c0392b")
receipt.tag_config("tax",     font=("Courier", 10),         foreground="#555555")
receipt.tag_config("nodis",   font=("Courier", 9),          foreground="#999988")

# Initial placeholder text
clear_all()

# Press Enter to generate bill quickly
root.bind("<Return>", lambda e: generate_bill())

root.mainloop()