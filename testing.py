import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re
import sqlite3

# Define colors
COLOR_PRIMARY = "#4CAF50"
COLOR_SECONDARY = "#008CBA"
COLOR_LIGHT_BACKGROUND = "#F5F5F5"
COLOR_DARK_TEXT = "#212121"
COLOR_LIGHT_TEXT = "#FFFFFF"

# Default login credentials
default_username = "svecw"
default_password = "1233"

# Hostel data
hostels_data = [
    ("Medha", "A cozy hostel with modern amenities.", "138000"),
    ("Sarada", "Spacious rooms with beautiful views.", "80000"),
    ("Vaishnavi", "Comfortable stay with recreational facilities.", "90000"),
    ("Manasa", "Tranquil atmosphere and high-quality services.", "75000"),
    ("Green Meadows", "Beautiful hostel surrounded by lush green meadows.", "100000"),
    ("Srujana", "A hostel known for its serene environment and friendly atmosphere.", "85000"),
    ("Nirmala", "Modern hostel with state-of-the-art facilities.", "60000"),
    ("Rohini", "Elegant hostel offering a peaceful stay with great amenities.", "70000")
]

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
        self.master.title("Hostel Booking System")

        login_image = Image.open("C:/Users/trish/Downloads/logo.jpeg")
        login_image = ImageTk.PhotoImage(login_image)
        login_image_label = tk.Label(self, image=login_image, background=COLOR_LIGHT_BACKGROUND)
        login_image_label.image = login_image
        login_image_label.pack(pady=10)

        tk.Label(self, text="Hostel Booking System", font=("Helvetica", 12, "bold"), background=COLOR_LIGHT_BACKGROUND).pack()

        username_label = tk.Label(self, text="Username:", background=COLOR_LIGHT_BACKGROUND)
        password_label = tk.Label(self, text="Password:", background=COLOR_LIGHT_BACKGROUND)
        self.username_entry = tk.Entry(self, bg="white")
        self.password_entry = tk.Entry(self, show="*", bg="white")
        self.login_button = tk.Button(self, text="Login", command=self.login, bg=COLOR_PRIMARY, fg=COLOR_LIGHT_TEXT)

        username_label.place(relx=0.5, rely=0.4, anchor="center")
        password_label.place(relx=0.5, rely=0.5, anchor="center")
        self.username_entry.place(relx=0.5, rely=0.45, anchor="center")
        self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")

    def login(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if entered_username == default_username and entered_password == default_password:
            self.destroy()
            self.master.hostel_selection_page = HostelSelectionPage(self.master)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class HostelSelectionPage(CenteredFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Choose Your Hostel", font=("Helvetica", 14, "bold"), background=COLOR_LIGHT_BACKGROUND).pack(pady=10)

        hostel_image = Image.open("C:/Users/trish/Downloads/logo.jpeg")
        hostel_image = ImageTk.PhotoImage(hostel_image)
        hostel_image_label = tk.Label(self, image=hostel_image, background=COLOR_LIGHT_BACKGROUND)
        hostel_image_label.image = hostel_image
        hostel_image_label.pack(pady=10)

        table_frame = tk.Frame(self)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.hostel_table = ttk.Treeview(table_frame, columns=("Name", "Description", "Price"), show="headings")
        self.hostel_table.heading("Name", text="Name")
        self.hostel_table.heading("Description", text="Description")
        self.hostel_table.heading("Price", text="Price")

        for hostel in hostels_data:
            self.hostel_table.insert("", "end", values=hostel)

        self.hostel_table.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.hostel_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.hostel_table.configure(yscrollcommand=scrollbar.set)

        select_button = tk.Button(self, text="Select Hostel", command=self.select_hostel, bg=COLOR_PRIMARY, fg=COLOR_LIGHT_TEXT)
        select_button.pack(pady=10)

    def select_hostel(self):
        selected_item = self.hostel_table.selection()
        if selected_item:
            selected_hostel_name = self.hostel_table.item(selected_item, "values")[0]
            self.destroy()
            self.master.hostel_page = HostelPage(self.master, selected_hostel_name)
        else:
            messagebox.showwarning("Selection Error", "Please select a hostel before submitting.")

class HostelPage(CenteredFrame):
    def __init__(self, master=None, hostel_name=None):
        super().__init__(master)
        self.hostel_name = hostel_name
        self.create_widgets()

    def create_widgets(self):
        content_frame = tk.Frame(self, background=COLOR_LIGHT_BACKGROUND)
        content_frame.pack(fill="both", expand=True)

        tk.Label(content_frame, text=f"Welcome to {self.hostel_name} Hostel!", font=("Helvetica", 16, "bold"), background=COLOR_LIGHT_BACKGROUND).pack(pady=10, anchor="w")

        description_frame = tk.Frame(content_frame, background=COLOR_LIGHT_BACKGROUND)
        description_frame.pack(pady=5, padx=10, anchor="w")
        tk.Label(description_frame, text="Description:", font=("Helvetica", 12, "bold"), background=COLOR_LIGHT_BACKGROUND).pack(anchor="w")
        description_text = self.get_description(self.hostel_name)
        description_label = tk.Label(description_frame, text=description_text, wraplength=400, justify="left", background=COLOR_LIGHT_BACKGROUND)
        description_label.pack(anchor="w")

        
        amenities_frame = tk.Frame(content_frame, background=COLOR_LIGHT_BACKGROUND)
        amenities_frame.pack(pady=5, padx=10, anchor="w")
        tk.Label(amenities_frame, text="Amenities:", font=("Helvetica", 12, "bold"), background=COLOR_LIGHT_BACKGROUND).pack(anchor="w")
        amenities_text = self.get_amenities(self.hostel_name)
        amenities_label = tk.Label(amenities_frame, text=amenities_text, wraplength=400, justify="left", background=COLOR_LIGHT_BACKGROUND)
        amenities_label.pack(anchor="w")

        
        reviews_frame = tk.Frame(content_frame, background=COLOR_LIGHT_BACKGROUND)
        reviews_frame.pack(pady=5, padx=10, anchor="w")
        tk.Label(reviews_frame, text="Reviews and Feedback:", font=("Helvetica", 12, "bold"), background=COLOR_LIGHT_BACKGROUND).pack(anchor="w")
        feedback_text = self.get_feedback(self.hostel_name)
        feedback_label = tk.Label(reviews_frame, text=feedback_text, wraplength=400, justify="left", background=COLOR_LIGHT_BACKGROUND)
        feedback_label.pack(anchor="w")

        tk.Button(self, text="Go Back", command=self.go_back, bg="#808080", fg="white").pack(pady=10)
        tk.Button(self, text="Book Now", command=self.open_registration_form, bg="#4CAF50", fg="white").pack(pady=10)

        image = Image.open("C:/Users/trish/Downloads/hostels.jpg")
        hostel_image = ImageTk.PhotoImage(image)
        image_label = tk.Label(content_frame, image=hostel_image)
        image_label.image = hostel_image
        image_label.place(relx=1, rely=0, anchor="ne")

    def go_back(self):
        self.destroy()
        self.master.hostel_selection_page = HostelSelectionPage(self.master)

    def open_registration_form(self):
        self.destroy()
        self.master.registration_form = RegistrationForm(self.master, selected_hostel=self.hostel_name)
    def get_description(self, hostel_name):
        descriptions = {
            "Medha": "A cozy hostel with modern amenities.",
            "Sarada": "Spacious rooms with beautiful views.",
            "Vaishnavi": "Comfortable stay with recreational facilities.",
            "Manasa": "Tranquil atmosphere and high-quality services.",
            "Green Meadows": "Beautiful hostel surrounded by lush green meadows.",
            "Srujana": "A hostel known for its serene environment and friendly atmosphere.",
            "Nirmala": "Modern hostel with state-of-the-art facilities.",
            "Rohini": "Elegant hostel offering a peaceful stay with great amenities."
        }
        return descriptions.get(hostel_name, "")

    def get_amenities(self, hostel_name):
        amenities = {
            "Medha": "WiFi, Laundry, Gym Facilities, Common Rooms",
            "Sarada": "WiFi, Laundry, Common Rooms, Study Areas",
            "Vaishnavi": "WiFi, Laundry, Common Rooms, Sports Facilities",
            "Manasa": "WiFi, Laundry, Study Areas, Recreational Rooms",
            "Green Meadows": "WiFi, Laundry, Gym Facilities, Outdoor Activities",
            "Srujana": "WiFi, Laundry, Common Rooms, Music Room",
            "Nirmala": "WiFi, Laundry, Gym Facilities, Dining Hall",
            "Rohini": "WiFi, Laundry, Common Rooms, Garden"
        }
        return amenities.get(hostel_name, "")

    def get_feedback(self, hostel_name):
        feedback = {
            "Medha": "Positive feedback about cleanliness and atmosphere.",
            "Sarada": "Great views and friendly staff.",
            "Vaishnavi": "Students enjoy the recreational facilities.",
            "Manasa": "Highly rated for services and peaceful environment.",
            "Green Meadows": "Beautiful surroundings and good amenities.",
            "Srujana": "Friendly atmosphere and helpful staff.",
            "Nirmala": "Modern facilities and good maintenance.",
            "Rohini": "Peaceful and elegant ambiance."
        }
        return feedback.get(hostel_name, "")

class RegistrationForm(CenteredFrame):
    def __init__(self, master=None, selected_hostel=None):
        super().__init__(master)
        self.selected_hostel = selected_hostel
        self.create_widgets()
        conn=sqlite3.connect("hosteldb.db")
        cursor=conn.cursor()
        cursor.execute(('''CREATE TABLE IF NOT EXISTS hostel (
    name TEXT ,
    email TEXT,
    branch TEXT,
    phone_number INTEGER NOT NULL,  
    fathers_name TEXT,
    fathers_phone_number INTEGER NOT NULL,
    mothers_name TEXT,
    mothers_phone_number INTEGER NOT NULL,
    hostel TEXT,
    state TEXT,
    city TEXT)'''))
        conn.close()
        
    def create_widgets(self):
        
        registration_image = Image.open("C:/Users/trish/Downloads/logobig.jpg")
        registration_image = registration_image.resize((100, 100))
        registration_image = ImageTk.PhotoImage(registration_image)
        registration_image_label = tk.Label(self, image=registration_image, background=COLOR_LIGHT_BACKGROUND)
        registration_image_label.image = registration_image
        registration_image_label.pack(pady=20, padx=20, anchor="nw")

        
        title_label = tk.Label(self, text="Book Your Slot", font=("Helvetica", 16), background=COLOR_LIGHT_BACKGROUND)
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        
        labels = ['Name', 'Email', 'Branch', 'Phone Number', "Father's Name", "Father's Phone Number", "Mother's Name", "Mother's Phone Number", 'Hostel', 'State', 'City']
        for i, label in enumerate(labels):
            tk.Label(self, text=label, background=COLOR_LIGHT_BACKGROUND).place(relx=0.45, rely=0.1+0.05*i, anchor=tk.E)

        branches = ['CSE', 'AIML', 'AIDS', 'ECE', 'EEE', 'Civil', 'Mech']
        self.branch_combobox = ttk.Combobox(self, values=branches, state="readonly")
        self.branch_combobox.place(relx=0.5, rely=0.2, anchor=tk.W)
        

        self.name_entry = tk.Entry(self, bg="white")
        self.name_entry.place(relx=0.5, rely=0.1, anchor=tk.W)
        self.email_entry = tk.Entry(self, bg="white")
        self.email_entry.place(relx=0.5, rely=0.15, anchor=tk.W)
        self.phno_entry = tk.Entry(self, bg="white")
        self.phno_entry.place(relx=0.5, rely=0.25, anchor=tk.W)
        self.father_name_entry = tk.Entry(self, bg="white")
        self.father_name_entry.place(relx=0.5, rely=0.3, anchor=tk.W)
        self.father_phno_entry = tk.Entry(self, bg="white")
        self.father_phno_entry.place(relx=0.5, rely=0.35, anchor=tk.W)
        self.mother_name_entry = tk.Entry(self, bg="white")
        self.mother_name_entry.place(relx=0.5, rely=0.4, anchor=tk.W)
        self.mother_phno_entry = tk.Entry(self, bg="white")
        self.mother_phno_entry.place(relx=0.5, rely=0.45, anchor=tk.W)
        self.hostel_entry = tk.Entry(self, bg="white")
        self.hostel_entry.insert(tk.END, self.selected_hostel)
        self.hostel_entry.place(relx=0.5, rely=0.5, anchor=tk.W)
        self.state_entry = tk.Entry(self, bg="white")
        self.state_entry.place(relx=0.5, rely=0.55, anchor=tk.W)
        self.city_entry = tk.Entry(self, bg="white")
        self.city_entry.place(relx=0.5, rely=0.6, anchor=tk.W)

        submit_button = tk.Button(self, text="Submit", command=self.register, bg=COLOR_PRIMARY, fg=COLOR_LIGHT_TEXT)
        submit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        go_back_button = tk.Button(self, text="Go Back", command=self.go_back, bg=COLOR_SECONDARY, fg=COLOR_LIGHT_TEXT)
        go_back_button.place(relx=0.1, rely=0.8, anchor=tk.W)

    def register(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        branch = self.branch_combobox.get()
        phno = self.phno_entry.get()
        father_name = self.father_name_entry.get()
        father_phno = self.father_phno_entry.get()
        mother_name = self.mother_name_entry.get()
        mother_phno = self.mother_phno_entry.get()
        hostel = self.hostel_entry.get()
        state = self.state_entry.get()
        city = self.city_entry.get()

        if not all((name, email, branch, phno, father_name, father_phno, mother_name, mother_phno, hostel, state, city)):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email address!")
            return

        if not re.match(r"^\d{10}$", phno):
            messagebox.showerror("Error", "Invalid phone number! Please enter 10 digits.")
            return

        # Connect to the database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute('''INSERT INTO hostel 
                            (name, email, branch, phone_number, fathers_name, fathers_phone_number, mothers_name, mothers_phone_number, hostel, state, city)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (name, email, branch, phno, father_name, father_phno, mother_name, mother_phno, hostel, state, city))
        conn.commit()
        cursor.execute('''SELECT * FROM hostel''')
        conn.commit()
        conn.close()

        self.destroy()
        self.master.thank_you_page = ThankYouPage(self.master, hostel_name=self.selected_hostel)

    def go_back(self):
        self.destroy()
        self.master.hostel_page = HostelPage(self.master, self.selected_hostel)

class ThankYouPage(CenteredFrame):
    def __init__(self, master=None, hostel_name=None):
        super().__init__(master)
        self.hostel_name = hostel_name
        self.create_widgets()

    def create_widgets(self):
        thank_you_image = Image.open("C:/Users/trish/Downloads/logo.jpeg")
        thank_you_image = ImageTk.PhotoImage(thank_you_image)
        thank_you_image_label = tk.Label(self, image=thank_you_image, background=COLOR_LIGHT_BACKGROUND)
        thank_you_image_label.image = thank_you_image
        thank_you_image_label.pack(pady=10)

        tk.Label(self, text="Thank You!", font=("Helvetica", 16, "bold"), background=COLOR_LIGHT_BACKGROUND).pack(pady=10)
        tk.Label(self, text=f"Your slot for {self.hostel_name} has been booked successfully.", font=("Helvetica", 12), background=COLOR_LIGHT_BACKGROUND).pack(pady=5)
        tk.Label(self, text="You will be notified soon.", font=("Helvetica", 12), background=COLOR_LIGHT_BACKGROUND).pack(pady=5)

# Main application window
root = tk.Tk()
root.configure(background=COLOR_LIGHT_BACKGROUND)
login_page = LoginPage(master=root)
login_page.center_on_screen(400, 600)
root.mainloop()
