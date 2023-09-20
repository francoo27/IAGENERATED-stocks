import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from datetime import datetime

# Function to parse the HTML file and extract headers and data
def parse_html_file(filename):
    with open(filename, "r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")

    headers = [
        "Fecha Transacción",
        "Fecha Liquidación",
        "Boleto",
        "Mercado",
        "Tipo Transacción",
        "Numero de Cuenta",
        "Descripción",
        "Especie",
        "Simbolo",
        "Cantidad",
        "Moneda",
        "Precio Ponderado",
        "Monto",
        "Comisión y Derecho de Mercado",
        "Iva Impuesto",
        "Total"
    ]

    data = []

    header_row = table.find("tr")
    header_cells = header_row.find_all("td")
    for cell in header_cells:
        headers.append(cell.text.strip())

    table_rows = table.find_all("tr")[1:]
    for row in table_rows:
        row_data = [cell.text.strip() for cell in row.find_all("td")]
        data.append(row_data)

    return headers, data

# Function to convert the Fecha Transacción column to datetime for sorting
def convert_fecha_transaccion(row):
    try:
        fecha_transaccion = datetime.strptime(row[0], "%d/%m/%Y %H:%M:%S")
    except ValueError:
        fecha_transaccion = datetime.min
    return fecha_transaccion

# Function to sort the Treeview by a specific column in descending order
def treeview_sort_column(tv, col, reverse):
    l = [(convert_fecha_transaccion(tv.item(k)["values"]), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # Rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # Reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

# Function to update the Treeview with filtered and sorted data
def update_treeview():
    # Clear the existing rows
    for item in tree_tab2.get_children():
        tree_tab2.delete(item)

    # Filter and sort the data
    filtered_data = [row for row in data_tab2 if date_filter_var.get() == "" or row[0].startswith(date_filter_var.get())]
    sorted_data = sorted(filtered_data, key=lambda row: convert_fecha_transaccion(row), reverse=True)

    # Insert filtered and sorted data into the Treeview
    for row in sorted_data:
        tree_tab2.insert('', 'end', values=row)

# Function to create the "Operaciones Finalizadas" tab
def create_operaciones_finalizadas_tab(notebook):
    # Create a "Operaciones Finalizadas" tab
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Operaciones Finalizadas")

    # Parse the HTML file to get headers and data for "Operaciones Finalizadas" tab
    headers, data = parse_html_file("OperacionesFinalizadas.html")

    # Create a Treeview widget for "Operaciones Finalizadas" tab
    tree_tab1 = ttk.Treeview(tab1, columns=headers, show="headings")
    tree_tab1.pack(fill=tk.BOTH, expand=True)

    # Add headers to the Treeview and make columns sortable for "Operaciones Finalizadas" tab
    for header in headers:
        tree_tab1.heading(header, text=header, command=lambda col=header: treeview_sort_column(tree_tab1, col, False))
        tree_tab1.column(header, width=100)  # Adjust the column width as needed

    # Insert data rows into the Treeview for "Operaciones Finalizadas" tab
    for row in data:
        tree_tab1.insert('', 'end', values=row)

