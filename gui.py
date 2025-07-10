import tkinter as tk
from tkinter import ttk
import math

# Function to apply color based on error range
def apply_color(labels, color):
    for label in labels:
        label.config(foreground=color)

# Function to process data and update the table
def process_data(file_path1, file_path2, velocity_cols, height_col, output_window):
    data_rows1 = []
    data_rows2 = []

    with open(file_path1, 'r') as file1:
        lines1 = file1.readlines()
        for line1 in lines1:
            row1 = list(map(float, line1.strip().split()))
            data_rows1.append(row1)

    with open(file_path2, 'r') as file2:
        lines2 = file2.readlines()
        for line2 in lines2:
            row2 = list(map(float, line2.strip().split()))
            data_rows2.append(row2)

    # Combine data from both files
    combined_data = []
    list1 = [[data_rows1[0][0], data_rows1[0][2]]]
    for i in range(len(data_rows1) - 1):
        if data_rows1[i][0] == data_rows1[i + 1][0]:
            continue
        else:
            list1.append([data_rows1[i + 1][0], data_rows1[i + 1][2]])

    for i in range(len(list1)):
        j = 0
        while data_rows2[j][0] < list1[i][1]:
            j += 1
        height = data_rows2[j][height_col - 1]
        vx = data_rows2[j][velocity_cols[0] - 1]
        vy = data_rows2[j][velocity_cols[1] - 1]
        vz = data_rows2[j][velocity_cols[2] - 1]
        velocity = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
        combined_data.append([list1[i][1], list1[i][0], velocity, height, "", "",""])  # Initialize with empty strings for "Description" and "error msg"

    combined_data[0][4] = "Lift off"
    combined_data[1][4] = "Cut off"

    # Create a canvas in the output window
    canvas = tk.Canvas(output_window)
    canvas.grid(row=0, column=0, sticky="nsew")

    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(output_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create another frame inside the canvas to hold the table
    table_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=table_frame, anchor="nw")

    # Clear existing labels in the output window
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Create header labels
    columns = ('TIME', 'EVENT NO.', 'VELOCITY', 'HEIGHT', 'Description', 'error msg')
    for idx, col in enumerate(columns):
        label = ttk.Label(table_frame, text=col, style="Header.TLabel")
        label.grid(row=0, column=idx, sticky="nsew")

    # Create data labels and store them by row for coloring
    rows_labels = []
    for i, row in enumerate(combined_data):
        row_labels = []
        for j, value in enumerate(row):
            label = ttk.Label(table_frame, text=value, style="Data.TLabel")
            label.grid(row=i + 1, column=j, sticky="nsew")
            row_labels.append(label)
        rows_labels.append(row_labels)

    # Set uniform row height
    for i in range(len(combined_data) + 1):  # +1 for header row
        table_frame.grid_rowconfigure(i, minsize=30)  # Adjust minsize as needed

    # Configure grid column weights
    for i in range(len(columns)):
        table_frame.grid_columnconfigure(i, weight=1)

    # Apply initial colors based on conditions
    for i, row in enumerate(combined_data):
        if row[1] == 2:
            if 26 <= row[2] <= 35 and 9.37 <= row[3] <= 11.3:
                combined_data[i][5] = "both in range"
                color = 'green'
            else:
                if 26 <= row[2] <= 35:
                    combined_data[i][5] = "height not in range"
                    color = 'red'
                elif row[3] <= 11.3:
                    combined_data[i][5] = "velocity not in range"
                    color = 'red'
                else:
                    combined_data[i][5] = "both not in range"
                    color = 'red'
        else:
            combined_data[i][5] = "both in range"
            color = 'green'
        
        rows_labels[i][5].config(text=combined_data[i][5])

        apply_color(rows_labels[i], color)

    # Update scrollregion of the canvas
    table_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Bind mouse scroll to canvas
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/10)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Allow the canvas to expand within the output window
    output_window.grid_rowconfigure(0, weight=1)
    output_window.grid_columnconfigure(0, weight=1)

# Function to start data processing
def start_processing():
    file_path1 = file1_entry.get() + '.dat'
    file_path2 = file2_entry.get() + '.dat'
    velocity_cols = list(map(int, velocity_entry.get().split(',')))
    height_col = int(height_entry.get())
    output_window = tk.Toplevel(root)
    output_window.title("Telemetry Data Table")
    output_window.geometry("800x400")
    process_data(file_path1, file_path2, velocity_cols, height_col, output_window)

# Create the main window
root = tk.Tk()
root.title("Input Data")
root.geometry("400x200")
root.configure(bg='#102542')

# Create input fields for file names and columns
input_frame = tk.Frame(root, bg='#102542')
input_frame.grid(row=0, column=0, padx=10, pady=10)

file1_label = tk.Label(input_frame, text="File Name 1:", bg='#102542', fg='white')
file1_label.grid(row=0, column=0, padx=5, pady=5)
file1_entry = tk.Entry(input_frame)
file1_entry.grid(row=0, column=1, padx=5, pady=5)

file2_label = tk.Label(input_frame, text="File Name 2:", bg='#102542', fg='white')
file2_label.grid(row=1, column=0, padx=5, pady=5)
file2_entry = tk.Entry(input_frame)
file2_entry.grid(row=1, column=1, padx=5, pady=5)

velocity_label = tk.Label(input_frame, text="Velocity Columns (comma-separated):", bg='#102542', fg='white')
velocity_label.grid(row=2, column=0, padx=5, pady=5)
velocity_entry = tk.Entry(input_frame)
velocity_entry.grid(row=2, column=1, padx=5, pady=5)

height_label = tk.Label(input_frame, text="Height Column:", bg='#102542', fg='white')
height_label.grid(row=3, column=0, padx=5, pady=5)
height_entry = tk.Entry(input_frame)
height_entry.grid(row=3, column=1, padx=5, pady=5)

start_button = tk.Button(input_frame, text="Start Processing", command=start_processing)
start_button.grid(row=4, columnspan=2, pady=10)

# Define style for headers and data cells
header_style = ttk.Style()
header_style.configure("Header.TLabel", background="white", foreground="black", relief="raised", anchor="center", font=('Arial', 12, 'bold'))
data_style = ttk.Style()
data_style.configure("Data.TLabel", background="white", foreground="black", relief="ridge", anchor="center", font=('Arial', 10))

# Start the Tkinter event loop
root.mainloop()
