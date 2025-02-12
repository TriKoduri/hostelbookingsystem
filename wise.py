import tkinter as tk
from tkinter import ttk, messagebox

# Default username and password
default_username = "svecw"
default_password = "1233"

class CenteredFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(expand=True, fill="both")

    def center_on_screen(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x_position}+{y_position}")

class LoginPage(CenteredFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Login")  # Set the title of the window
        username_label = tk.Label(self, text="Username:")
        password_label = tk.Label(self, text="Password:")
        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Login", command=self.login)

        # Place widgets in the middle of the frame
        username_label.place(relx=0.5, rely=0.4, anchor="center")
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.username_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")

    def login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if entered_username == default_username and entered_password == default_password:
            # Hide login page widgets
            self.destroy()

            # Show hostel selection page
            self.master.hostel_selection_page = HostelSelectionPage(self.master)

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class HostelSelectionPage(CenteredFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Your Hostel:").pack(pady=10)

        hostels_data = [
            {"name": "Medha", "description": "A cozy hostel with modern amenities.", "price": "Rs138000 per year"},
            {"name": "Sarada", "description": "Spacious rooms with beautiful views.", "price": "Rs850000 per year"},
            {"name": "Vaishnavi", "description": "Comfortable stay with recreational facilities.", "price": "Rs80000 per year"},
            {"name": "Manasa", "description": "Tranquil atmosphere and high-quality services.", "price": "Rs80000 per year"},
            {"name": "Green Meadows", "description": "Beautiful hostel surrounded by lush green meadows.", "price": "Rs120000 per year"},
            {"name": "Srujana", "description": "A hostel known for its serene environment and friendly atmosphere.", "price": "Rs95000 per year"},
            {"name": "Nirmala", "description": "Modern hostel with state-of-the-art facilities.", "price": "Rs110000 per year"},
            {"name": "Rohini", "description": "Elegant hostel offering a peaceful stay with great amenities.", "price": "Rs105000 per year"}
        ]

        self.create_hostel_table(hostels_data)

        submit_button = tk.Button(self, text="Submit", command=self.submit_hostel)
        submit_button.pack(pady=10)

    def create_hostel_table(self, hostels_data):
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10)

        self.hostel_table = ttk.Treeview(table_frame, columns=("Name", "Description", "Price"), show="headings")
        self.hostel_table.heading("Name", text="Name")
        self.hostel_table.heading("Description", text="Description")
        self.hostel_table.heading("Price", text="Price")

        for hostel_data in hostels_data:
            self.hostel_table.insert("", "end", values=(hostel_data["name"], hostel_data["description"], hostel_data["price"]))

        self.hostel_table.pack(side="left", padx=10)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.hostel_table.yview)
        scrollbar.pack(side="right", fill="y")

        self.hostel_table.configure(yscrollcommand=scrollbar.set)

    def submit_hostel(self):
        selected_item = self.hostel_table.selection()
        if selected_item:
            selected_hostel_name = self.hostel_table.item(selected_item, "values")[0]
            messagebox.showinfo("Hostel Selected", f"You have selected {selected_hostel_name} Hostel.")
            # Destroy the current frame
            self.destroy()
            # Show the new page for the selected hostel
            self.master.hostel_page = HostelPage(self.master, selected_hostel_name)
        else:
            messagebox.showwarning("Selection Error", "Please select a hostel before submitting.")

class HostelPage(CenteredFrame):
    def __init__(self, master=None, hostel_name=None):
        super().__init__(master)
        self.hostel_name = hostel_name
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Welcome to {self.hostel_name} Hostel!", font=("Helvetica", 16, "bold")).pack(pady=10, padx=10, anchor="w")
        
        description_frame = tk.Frame(self)
        description_frame.pack(pady=10, padx=10, anchor="w")
        tk.Label(description_frame, text="Description:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        tk.Text(description_frame, width=50, height=5).pack(anchor="w")

        amenities_frame = tk.Frame(self)
        amenities_frame.pack(pady=10, padx=10, anchor="w")
        tk.Label(amenities_frame, text="Amenities:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        tk.Text(amenities_frame, width=50, height=5).pack(anchor="w")

        reviews_frame = tk.Frame(self)
        reviews_frame.pack(pady=10, padx=10, anchor="w")
        tk.Label(reviews_frame, text="Reviews and Feedback:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        tk.Text(reviews_frame, width=50, height=5).pack(anchor="w")

        tk.Button(self, text="Go Back", command=self.go_back).pack(pady=10)
        tk.Button(self, text="Book Now", command=self.book_now).pack(pady=10)

    def go_back(self):
        # Destroy the current frame
        self.destroy()
        # Show the hostel selection page again
        self.master.hostel_selection_page = HostelSelectionPage(self.master)

    def book_now(self):
        messagebox.showinfo("Book Now", "Booking functionality will be implemented soon!")

# Create the main window
root = tk.Tk()

# Create login page
login_page = LoginPage(master=root)
login_page.center_on_screen(400, 200)

# Run the application
root.mainloop()
