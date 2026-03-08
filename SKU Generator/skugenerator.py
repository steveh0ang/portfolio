# Author: Steve Hoang
# GitHub username: steveh0ang
# Description: Customer SKU generator app

import tkinter as tk
from tkinter import ttk
import re


PRODUCT_TYPES = [
    "TEE",
    "HOODIE",
    "CREWNECK",
    "LONGSLEEVE",
    "TANKTOP",
    "ZIPHOODIE",
]

SIZES = ["OS", "XS", "S", "M", "L", "XL", "2X", "3X"]


def sanitize_text(text):
    """
    Removes spaces and special characters.
    Keeps only letters and numbers.
    Converts to ALL CAPS.
    """
    text = text.upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text


def parse_colors(color_string):
    """
    Splits colors separated by commas.
    """
    if color_string.strip() == "":
        return []

    colors = color_string.split(",")

    cleaned = []
    for color in colors:
        c = sanitize_text(color)
        if c:
            cleaned.append(c)

    return cleaned


def generate_skus(brand, name, product_type, colors, sizes):

    brand = sanitize_text(brand)
    name = sanitize_text(name)
    product_type = sanitize_text(product_type)

    skus = []

    if colors:
        for color in colors:
            for size in sizes:
                sku = f"{brand}-{name}-{product_type}-{color}-{size}"
                skus.append(sku)
    else:
        for size in sizes:
            sku = f"{brand}-{name}-{product_type}-{size}"
            skus.append(sku)

    return skus


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("SKU Generator")

        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        # BRAND
        ttk.Label(main, text="BRAND").grid(row=0, column=0, sticky="w")
        self.brand_entry = ttk.Entry(main, width=20)
        self.brand_entry.grid(row=1, column=0, padx=5)

        # NAME
        ttk.Label(main, text="NAME").grid(row=0, column=1, sticky="w")
        self.name_entry = ttk.Entry(main, width=25)
        self.name_entry.grid(row=1, column=1, padx=5)

        # PRODUCT TYPE
        ttk.Label(main, text="PRODUCT TYPE").grid(row=0, column=2, sticky="w")
        self.type_combo = ttk.Combobox(main, values=PRODUCT_TYPES, state="readonly")
        self.type_combo.current(0)
        self.type_combo.grid(row=1, column=2, padx=5)

        # COLORS
        ttk.Label(main, text="COLOR(S)").grid(row=0, column=3, sticky="w")
        self.color_entry = ttk.Entry(main, width=25)
        self.color_entry.grid(row=1, column=3, padx=5)

        # SIZE LIST
        ttk.Label(main, text="SIZE").grid(row=0, column=4, sticky="w")

        self.size_list = tk.Listbox(main, selectmode=tk.MULTIPLE, height=8)
        for s in SIZES:
            self.size_list.insert(tk.END, s)

        self.size_list.grid(row=1, column=4)

        # GENERATE BUTTON
        generate_btn = ttk.Button(main, text="Generate SKUs", command=self.generate)
        generate_btn.grid(row=2, column=0, columnspan=5, pady=15)

        # OUTPUT
        self.output = tk.Text(main, height=15, width=80)
        self.output.grid(row=3, column=0, columnspan=5)

    def get_selected_sizes(self):

        selections = self.size_list.curselection()

        sizes = []

        for i in selections:
            sizes.append(self.size_list.get(i))

        return sizes

    def generate(self):

        brand = self.brand_entry.get()
        name = self.name_entry.get()
        product_type = self.type_combo.get()
        color_input = self.color_entry.get()

        colors = parse_colors(color_input)
        sizes = self.get_selected_sizes()

        skus = generate_skus(brand, name, product_type, colors, sizes)

        self.output.delete("1.0", tk.END)

        for sku in skus:
            self.output.insert(tk.END, sku + "\n")


root = tk.Tk()
app = App(root)
root.mainloop()
