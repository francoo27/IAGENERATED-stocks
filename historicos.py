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
        "Nro. de Mov.",
        "Nro. de Boleto",
        "Tipo Mov.",
        "Concert.",
        "Liquid.",
        "Est",
        "Cant. titulos",
        "Precio",
        "Comis.",
        "Iva Com.",
        "Otros Imp.",
        "Monto",
        "Observaciones",
        "Tipo Cuenta"
    ]

    data = []

    table_rows = table.find_all("tr")
    for row in table_rows[2:]:  # Start from the third row
        row_data = [cell.text.strip() for cell in row.find_all("td")]
        data.append(row_data)

    return headers, data

# Function to convert the Fecha Transacción column to datetime for sorting
def convert_fecha_transaccion(row):
    try:
        fecha_transaccion = datetime.strptime(row[3], "%d/%m/%y")
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
    filtered_data = [row for row in data_tab2 if date_filter_var.get() == "" or row[3].startswith(date_filter_var.get())]
    sorted_data = sorted(filtered_data, key=lambda row: convert_fecha_transaccion(row), reverse=True)

    # Insert filtered and sorted data into the Treeview
    for row in sorted_data:
        tree_tab2.insert('', 'end', values=row)

# Function to create the "Históricos" tab
def create_historicos_tab(notebook):
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Históricos")

    # Parse the HTML file to get headers and data for "Históricos" tab
    headers_tab2, data_tab2 = parse_html_file("MovimientosHistoricos.html")

    # Create a Treeview widget for "Históricos" tab
    tree_tab2 = ttk.Treeview(tab2, columns=headers_tab2, show="headings")
    tree_tab2.pack(side="left", fill=tk.BOTH, expand=True)

    # Create vertical scrollbar on the right side
    vsb = ttk.Scrollbar(tab2, orient="vertical", command=tree_tab2.yview)
    vsb.pack(side="right", fill="y")

    # Add headers to the Treeview and make columns sortable for "Históricos" tab
    for header in headers_tab2:
        tree_tab2.heading(header, text=header, command=lambda col=header: treeview_sort_column(tree_tab2, col, False))
        tree_tab2.column(header, width=100)  # Adjust the column width as needed

    # Link scrollbars to Treeview
    tree_tab2.configure(yscrollcommand=vsb.set)


    # Insert data rows into the Treeview for "Históricos" tab
    for row in data_tab2:
        tree_tab2.insert('', 'end', values=row)

    # Calculate and display the total row
    total_row = ["Total"]
    for i in range(1, len(headers_tab2)):
        if all(cell.replace(",", "").replace(".", "").isdigit() for cell in data_tab2[0]):
            column_data = [float(row[i].replace(",", ".")) for row in data_tab2]
            total = sum(column_data)
            total_row.append(f"{total:.2f}")
        else:
            total_row.append("")  # Leave empty for non-numeric columns

    tree_tab2.insert('', 'end', values=total_row)

# Note: The main tkinter loop is not included here. It should be added in your main.py file.

# This function will be called in your main.py file to create the "Históricos" tab
# create_historicos_tab(notebook)
