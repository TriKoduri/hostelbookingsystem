import tkinter as tk
import re
from tkinter import ttk,messagebox,Label
from PIL import Image, ImageTk
import sqlite3
COLOR_PRIMARY = "#4CAF50"  # green
COLOR_SECONDARY = "#008CBA"  # blue
COLOR_LIGHT_BACKGROUND = "#F5F5F5"  # light gray
COLOR_DARK_TEXT = "#212121"  # dark gray
COLOR_LIGHT_TEXT = "#FFFFFF"  # white
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
class signup_page(CenteredFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(expand=True, fill="both")
        # Create left frame
        self.left_frame = self.LeftFrame(self)
        # Create right frame
        self.right_frame = self.RightFrame(self)

    class LeftFrame(tk.Frame):
        def __init__(self, master, *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.configure(bg="lightblue")
            self.pack(side="left", fill="both", expand=True)
            
            # Load and display the image
            self.img = Image.open("C:/python project/new.jpg")
            self.resized_image = self.resize_image(self.img, 740, 560)
            self.img_label = tk.Label(self, image=self.resized_image, border=0, bg='white')
            self.img_label.place(relx=0.5, rely=0.5, anchor="center")
            
        def resize_image(self, image, width, height):
            aspect_ratio = min(width / image.width, height / image.height)
            new_width = max(1, int(image.width * aspect_ratio * 0.6))
            new_height = max(1, int(image.height * aspect_ratio * 0.6))
            resized_image = image.resize((new_width, new_height))
            return ImageTk.PhotoImage(resized_image)

    class RightFrame(tk.Frame):
        def __init__(self, master, *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.pack(side="right", fill="both", expand=True)
            conn = sqlite3.connect("hosteldb1.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users(user_name TEXT PRIMARY KEY,password NUMBER NOT NULL,confirm_pass NUMBER NOT NULL)")
            conn.close( )
            img = Image.open("C:/python project/logo.jpeg")
            img = img.resize((550, 110))  # Resize the image if needed
            photo = ImageTk.PhotoImage(img)
            image_label = Label(self, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.place(relx=0.5, rely=0, anchor="n")
            img2 = Image.open("C:/python project/person login.png")
            img2 = img2.resize((100, 100))  # Resize the image if needed
            photo = ImageTk.PhotoImage(img2)
            image_label = Label(self, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.place(relx=0.5, rely=0.36, anchor="n")
            # Create and place widgets in the right frame
            self.signin_label = tk.Label(self, text="Sign Up / Login", font=("Arial", 15, "bold"), fg="black",)
            self.signin_label.place(relx=0.5, rely=0.28, anchor="center")
            self.username_entry = tk.Entry(self, width=30)
            self.username_entry.place(relx=0.6, rely=0.6, anchor="center")
            self.password_entry = tk.Entry(self, show="*", width=30)
            self.password_entry.place(relx=0.6, rely=0.67, anchor="center")
            self.confirm_password_entry = tk.Entry(self, show="*", width=30)
            self.confirm_password_entry.place(relx=0.6, rely=0.73, anchor="center")

            # Labels for username, password, and confirm password
            tk.Label(self, text="Username:", font=("Arial", 12), fg="black", bg="lightblue").place(relx=0.4, rely=0.6, anchor="e")
            tk.Label(self, text="Password:", font=("Arial", 12), fg="black", bg="lightblue").place(relx=0.4, rely=0.67, anchor="e")
            tk.Label(self, text="Conform Password:", font=("Arial", 12), fg="black", bg="lightblue").place(relx=0.4, rely=0.73, anchor="e")

            # Submit button
            self.submit_button = ttk.Button(self, text="Submit", command=self.validate_signup)
            self.submit_button.place(relx=0.6, rely=0.8, anchor="center")
            self.login_button = tk.Button(self, text="Login",fg="blue", command=self.switch_to_login_page)
            self.login_button.place(relx=0.6, rely=0.85, anchor="center")
        def validate_signup(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()

            if all((username, password, confirm_password)):
                conn = sqlite3.connect("hosteldb1.db")
                cursor = conn.cursor()
                cursor.execute('SELECT user_name FROM users WHERE user_name=?',[username])
                if cursor.fetchone() is not None:
                    messagebox.showerror("Error","Username already exists.")
                else:
                    cursor.execute('INSERT INTO users(user_name, password, confirm_pass) VALUES(?,?,?)',[username,password,confirm_password])
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success","Account has been created")
                    self.master.switch_frame(LoginPage)
                    self.master.switch_frame(signup_page.LoginPage) 
            if not all((username, password, confirm_password)):
                messagebox.showerror("Error", "Please fill in all fields.")
            elif password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match.")
            else:
                # Handle sign-up process here
                messagebox.showinfo("Success", "Sign-up successful!")
        def switch_to_login_page(self):
            self.master.switch_frame(LoginPage)
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()
        new_frame.pack(expand=True, fill="both")
class LoginPage(CenteredFrame):
        def __init__(self, master=None):
            super().__init__(master)
            self.create_widgets()
        def create_widgets(self):
            self.login1_image = Image.open("C:/python project/svecw1.png")
            self.login1_photo = ImageTk.PhotoImage(self.login1_image)
            self.image1_label = tk.Label(self, image=self.login1_photo)
            self.image1_label.image = self.login1_photo
            self.image1_label.pack(fill="both", expand=True)
        
            overlay_image = Image.open("C:/python project/logo.jpeg")
            overlay_photo = ImageTk.PhotoImage(overlay_image)
            overlay_label = tk.Label(self, image=overlay_photo)
            overlay_label.image = overlay_photo
            overlay_label.place(relx=0.5, rely=0.2, anchor="center")
            tk.Label(self, text="Hostel Booking System", font=("Helvetica", 12, "bold"), background=COLOR_LIGHT_BACKGROUND).pack()
    
            username_label = tk.Label(self,text="Username:", font=("Helvetica", 14,"bold"))
            password_label = tk.Label(self,text="Password:", font=("Helvetica", 14,"bold"))
        
            self.username_entry = tk.Entry(self,  font=("Arial", 14))
            self.password_entry = tk.Entry(self, show="*",  font=("Arial", 14))
        
        
            self.login_button = tk.Button(self, text="Submit", command=self.login, bg="#008CBA", fg=COLOR_LIGHT_TEXT, font=("Helvetica", 14))
        
            username_label.place(relx=0.4, rely=0.4, anchor="e") 
            password_label.place(relx=0.4, rely=0.55, anchor="e")
            self.username_entry.place(relx=0.5, rely=0.4, anchor="center")  
            self.password_entry.place(relx=0.5, rely=0.55, anchor="center")
            self.login_button.place(relx=0.5, rely=0.7, anchor="center")

        def login(self):
            entered_username = self.username_entry.get()
            entered_password = self.password_entry.get()
            if entered_username and entered_password:
                conn = sqlite3.connect("hosteldb1.db")
                cursor = conn.cursor()
                cursor.execute('SELECT user_name, password FROM users WHERE user_name=? AND password=?',[entered_username,entered_password])
                user = cursor.fetchone()
                conn.close
                self.destroy()
                self.master.hostel_selection_page = HostelSelectionPage(self.master)
                if user:
                    messagebox.showinfo("Success","login successful")
                else:
                    messagebox.showerror("Error","Invalid username or password.")
            else:
                messagebox.showerror("Error","Enter both username and password")
class Hostel:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

hostels_data = [
    Hostel("Medha", "A cozy hostel with modern amenities.", "138000"),
    Hostel("Sarada", "Spacious rooms with beautiful views.", "80000"),
    Hostel("Vaishnavi", "Comfortable stay with recreational facilities.", "90000"),
    Hostel("Manasa", "Tranquil atmosphere and high-quality services.", "75000"),
    Hostel("Green Meadows", "Beautiful hostel surrounded by lush green meadows.", "100000"),
    Hostel("Srujana", "A hostel known for its serene environment ", "85000"),
    Hostel("Nirmala", "Modern hostel with state-of-the-art facilities.", "60000"),
    Hostel("Rohini", "Elegant hostel offering a peaceful stay ", "70000")
]
class HostelSelectionPage(CenteredFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        # Background image
        self.bg_image = Image.open("C:/python project/svecw2.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        tk.Label(self, text="Choose Your Hostel", font=("Helvetica", 14, "bold"), background=COLOR_LIGHT_BACKGROUND).place(relx=0.5, rely=0.05, anchor="n")

        hostel_image = tk.PhotoImage(file="C:/python project/logo.jpeg")  
        image_label = tk.Label(self, image=hostel_image)
        image_label.image = hostel_image  
        image_label.place(relx=0.5, rely=0.1, anchor="n")

        table_frame = tk.Frame(self, background=COLOR_LIGHT_BACKGROUND)
        table_frame.place(relx=0.5, rely=0.3, anchor="n")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))  
        style.configure("Treeview", font=("Helvetica", 12))  

        self.hostel_table = ttk.Treeview(table_frame, columns=("Name", "Description", "Price"), show="headings", height=10)
        self.hostel_table.heading("Name", text="Name")
        self.hostel_table.heading("Description", text="Description")
        self.hostel_table.heading("Price", text="Price")
        self.hostel_table.column("Name", width=200)  
        self.hostel_table.column("Description", width=400) 
        self.hostel_table.column("Price", width=100)  

        for hostel in hostels_data:
            self.hostel_table.insert("", "end", values=(hostel.name, hostel.description, hostel.price))
        self.hostel_table.pack(side="left", fill="both", expand=True)
        select_button = tk.Button(self, text="Select Hostel",font=("Arial",12,"bold"),command=self.select_hostel, bg=COLOR_PRIMARY, fg=COLOR_LIGHT_TEXT)
        select_button.place(relx=0.5, rely=0.8, anchor="s")

    def select_hostel(self):
        selected_item = self.hostel_table.focus()
        if selected_item:
            selected_hostel_name = self.hostel_table.item(selected_item, "values")[0]
            self.destroy()
            self.master.hostel_page = HostelPage(self.master, selected_hostel_name)
        else:
            messagebox.showwarning("Selection Error","Please select a hostel before submitting.")
class HostelPage(CenteredFrame):
    def __init__(self, master=None, hostel_name=None):
        super().__init__(master)
        self.hostel_name = hostel_name
        self.create_widgets()

    def create_widgets(self):
        self.pack(fill="both", expand=True)

        left_frame = tk.Frame(self, background="#ADD8E6")
        left_frame.pack(side="left", fill="both", expand=True)
        right_frame = tk.Frame(self, background="#000080")
        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(left_frame, text=f"Welcome to {self.hostel_name} Hostel!", font=("Helvetica", 16, "bold"), background="#ADD8E6").pack(pady=9, anchor="w")

        description_frame = tk.Frame(left_frame, background="#ADD8E6")
        description_frame.pack(pady=5, padx=10, anchor="w")
        tk.Label(description_frame, text="Description:", font=("Helvetica", 12, "bold"), background="#ADD8E6").pack(anchor="w")
        description_text = self.get_description(self.hostel_name)
        description_label = tk.Label(description_frame, text=description_text, wraplength=400, justify="left", background="#ADD8E6",font=("Helvetica", 12))
        description_label.pack(anchor="w")

        amenities_frame = tk.Frame(left_frame, background="#ADD8E6")
        amenities_frame.pack(pady=5, padx=10, anchor="w")
        tk.Label(amenities_frame, text="Amenities:", font=("Helvetica", 12, "bold"), background="#ADD8E6").pack(anchor="w")
        amenities_text = self.get_amenities(self.hostel_name)
        amenities_label = tk.Label(amenities_frame, text=amenities_text, wraplength=400, justify="left", background="#ADD8E6",font=("Helvetica", 12))
        amenities_label.pack(anchor="w")

        reviews_frame = tk.Frame(left_frame, background="#ADD8E6")
        reviews_frame.pack(pady=5, padx=10, anchor="w")
        tk.Label(reviews_frame, text="Reviews and Feedback:", font=("Helvetica", 12, "bold"), background="#ADD8E6").pack(anchor="w")
        feedback_text = self.get_feedback(self.hostel_name)
        feedback_label = tk.Label(reviews_frame, text=feedback_text, wraplength=400, justify="left", background="#ADD8E6",font=("Helvetica", 12))
        feedback_label.pack(anchor="w")

        tk.Button(right_frame, text="Go Back", command=self.go_back, bg="#808080",  font=("Helvetica", 12),fg="white").pack(side=tk.BOTTOM, padx=10, pady=10)
        tk.Button(right_frame, text="Book Now", command=self.open_registration_form, bg="#4CAF50",  font=("Helvetica", 12),fg="white").pack(side=tk.BOTTOM, padx=10, pady=10)

        image_path = f"C:/python project/{self.hostel_name.lower()}.jpg"
        image = Image.open(image_path)
        hostel_image = ImageTk.PhotoImage(image)
        image_label = tk.Label(right_frame, image=hostel_image)
        image_label.image = hostel_image
        image_label.pack(side="right", padx=20, pady=20)

    def go_back(self):
        self.destroy()
        self.master.hostel_selection_page = HostelSelectionPage(self.master)

    def open_registration_form(self):
        self.destroy()
        self.master.registration_form = RegistrationForm(self.master, selected_hostel=self.hostel_name)

    def get_description(self, hostel_name):
        descriptions = {
            "Medha": "Medha Hostel offers a serene and welcoming environment conducive to both academic and personal growth. Situated amidst lush greenery, the hostel provides a tranquil atmosphere that promotes focus and relaxation. The architecture boasts modern design elements, ensuring residents' comfort and convenience.Amenities:",
            "Sarada": "Sarada Hostel is renowned for its picturesque views and welcoming atmosphere. Situated in a serene environment, it offers spacious rooms equipped with modern amenities to ensure a comfortable stay for its residents. The hostel provides a conducive environment for both academic pursuits and relaxation.",
            "Vaishnavi": "Vaishnavi Hostel is renowned for its comfortable accommodations and recreational facilities, providing residents with an enriching living experience. Located in a vibrant setting, the hostel offers a range of amenities aimed at enhancing the well-being and convenience of its residents.",
            "Manasa": "Manasa Hostel is renowned for its tranquil atmosphere and commitment to providing high-quality services to its residents. Situated amidst serene surroundings, the hostel offers a peaceful and conducive environment for academic pursuits and personal growth. With a range of amenities and facilities, Manasa Hostel aims to ensure the well-being and comfort of its residents.",
            "Green Meadows": "Green Meadows Hostel is aptly named for its scenic location surrounded by verdant meadows, creating a tranquil and refreshing atmosphere for its residents. The hostel is designed to provide a peaceful retreat away from the hustle and bustle of urban life, allowing residents to immerse themselves in nature's beauty while enjoying modern amenities and comfortable accommodations.",
            "Srujana": "Srujana Hostel is characterized by its warm and inviting ambiance, offering residents a home away from home. The hostel is designed to foster a sense of community and camaraderie among its residents, creating a supportive environment where individuals can thrive and grow. With its emphasis on creating a welcoming atmosphere, Srujana Hostel is a popular choice among students seeking a comfortable and inclusive living experience.",
            "Nirmala": "Nirmala Hostel is renowned for its contemporary amenities and high-quality services, providing residents with a comfortable and conducive living environment. The hostel is designed to meet the diverse needs of its residents, offering modern facilities and conveniences to enhance their living experience. With its focus on providing a safe, secure, and supportive environment, Nirmala Hostel is a preferred choice among students seeking quality accommodation.",
            "Rohini": "Rohini Hostel is characterized by its peaceful atmosphere and sophisticated amenities, offering residents a refined and comfortable living space. The hostel is designed to promote relaxation and well-being, providing a tranquil retreat for residents amidst their academic pursuits. With its elegant architecture and thoughtful design, Rohini Hostel exudes a sense of sophistication and charm, making it a preferred choice for students seeking a tranquil and elegant living environment."
        }
        return descriptions.get(hostel_name, "")

    def get_amenities(self, hostel_name):
        amenities = {
            "Medha":"Medha Hostel offers a comfortable and modern living environment for its residents. With amenities such as WiFi connectivity, laundry services, and well-equipped gym facilities, residents can enjoy a convenient lifestyle. Additionally, common rooms provide spaces for socializing and relaxation, contributing to a cozy atmosphere within the hostel.",
            "Sarada": "Sarada Hostel provides residents with spacious accommodations and essential amenities for a pleasant stay. Along with WiFi connectivity and laundry facilities, the hostel offers common rooms and study areas where students can engage in academic pursuits or socialize with peers. The hostel's serene surroundings and beautiful views enhance the overall living experience.",
            "Vaishnavi": "Vaishnavi Hostel prioritizes the well-being and recreational needs of its residents. Offering WiFi access and laundry services, the hostel also features common rooms and sports facilities, providing opportunities for leisure activities and relaxation. Residents can enjoy a comfortable stay with access to various amenities for their enjoyment.",
            "Manasa": "Manasa Hostel fosters a tranquil atmosphere and focuses on providing high-quality services to its residents. With amenities such as WiFi connectivity, laundry facilities, and dedicated study areas, students can pursue their academic goals effectively while enjoying a peaceful environment. Recreational rooms offer additional spaces for relaxation and socializing.",
            "Green Meadows": "Surrounded by lush greenery, Green Meadows Hostel offers a serene living environment with access to essential amenities. Residents can benefit from WiFi connectivity, laundry services, and well-equipped gym facilities. Additionally, outdoor activities provide opportunities for residents to explore and enjoy the natural surroundings.",
            "Srujana": " Srujana Hostel is known for its friendly atmosphere and serene environment, providing a comfortable living space for residents. With amenities such as WiFi connectivity, laundry services, and common rooms, students can enjoy a pleasant stay while socializing with peers. The hostel's music room offers a unique space for relaxation and creativity.",
            "Nirmala": "Nirmala Hostel offers modern facilities and amenities to ensure a comfortable living experience for its residents. With WiFi access, laundry services, and well-equipped gym facilities, residents can enjoy convenience and relaxation. The hostel's dining hall provides nutritious meals, contributing to overall well-being.",
            "Rohini": " Rohini Hostel provides a peaceful and elegant ambiance, offering essential amenities for residents' comfort and relaxation. With WiFi connectivity, laundry services, and common rooms, students can enjoy a comfortable stay while socializing with peers. The hostel's garden area provides a tranquil outdoor space for relaxation and contemplation."
        }
        return amenities.get(hostel_name, "")

    def get_feedback(self, hostel_name):
        feedback = {
            "Medha": "Medha Hostel garners positive feedback from residents for its well-maintained facilities, conducive environment for study and relaxation, and the availability of diverse amenities. Residents appreciate the thoughtful provisions such as the reading room, 24-hour power supply, and recreational facilities, which contribute to a fulfilling hostel experience.",
            "Sarada": "Students commend the hostel for its spacious rooms with beautiful views and the friendly staff. However, some suggest improvements in laundry facilities to better cater to their needs.",
            "Vaishnavi": "The hostel is praised for its vibrant atmosphere and excellent recreational facilities. However, some students mention noise issues in the common areas, affecting their study environment.",
            "Manasa": " Highly rated for its peaceful environment and high-quality services. Students appreciate the availability of study areas but suggest adding more to accommodate all residents effectively.",
            "Green Meadows": "Students enjoy the beautiful surroundings and the tranquility of the hostel. However, there are occasional issues with Wi-Fi connectivity, which can be inconvenient for academic and personal use.",
            "Srujana": "Known for its friendly atmosphere and helpful staff, students feel supported in their academic and personal endeavors. Some suggest improvements in the cleanliness of the dining hall to enhance their dining experience.",
            "Nirmala": "Students value the modern facilities provided by the hostel. However, there are concerns about maintenance in common areas, which could impact the overall living experience.",
            "Rohini": "Praised for its peaceful ambiance and elegant design, the hostel provides a conducive environment for academic pursuits. Some students suggest adding more social activities to foster a stronger sense of community among residents."
        }
        return feedback.get(hostel_name, "")
class RegistrationForm(CenteredFrame):
    def __init__(self, master=None, selected_hostel=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(expand=True, fill="both")

        # Left frame
        left_frame = tk.Frame(self, bg="#87CEEB")
        left_frame.pack(side="left", fill="both", expand=True)
        image1_path = "C:/python project/registration.png"
        image1 = Image.open(image1_path)
        resized_image = self.resize_image(image1, 740, 560)
        img_label = tk.Label(left_frame, image=resized_image, border=0, bg='white')
        img_label.image = resized_image 
        img_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right frame
        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True)
        self.selected_hostel = selected_hostel
        self.create_right_widgets(right_frame)

    def create_right_widgets(self, right_frame):
        title_label = tk.Label(right_frame, text=f"Book Your Slot for {self.selected_hostel}", font=("Helvetica", 16), background=COLOR_LIGHT_BACKGROUND)
        title_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

        labels = ['Name', 'Email', 'Branch', 'Phone Number', "Father's Name", "Father's Phone Number", "Mother's Name", "Mother's Phone Number", 'Hostel', 'State', 'City']
        for i, label_text in enumerate(labels):
            label = tk.Label(right_frame, text=label_text, font=("Helvetica", 12, "bold"))
            label.place(relx=0.45, rely=0.1+0.05*i, anchor=tk.E)

        branches = ['CSE', 'AIML', 'AIDS', 'ECE', 'EEE', 'Civil', 'Mech']
        self.branch_combobox = ttk.Combobox(right_frame, values=branches, state="readonly")
        self.branch_combobox.place(relx=0.5, rely=0.2, anchor=tk.W)

        self.name_entry = tk.Entry(right_frame, bg="white")
        self.name_entry.place(relx=0.5, rely=0.1, anchor=tk.W)
        self.email_entry = tk.Entry(right_frame, bg="white")
        self.email_entry.place(relx=0.5, rely=0.15, anchor=tk.W)
        self.phno_entry = tk.Entry(right_frame, bg="white")
        self.phno_entry.place(relx=0.5, rely=0.25, anchor=tk.W)
        self.father_name_entry = tk.Entry(right_frame, bg="white")
        self.father_name_entry.place(relx=0.5, rely=0.3, anchor=tk.W)
        self.father_phno_entry = tk.Entry(right_frame, bg="white")
        self.father_phno_entry.place(relx=0.5, rely=0.35, anchor=tk.W)
        self.mother_name_entry = tk.Entry(right_frame, bg="white")
        self.mother_name_entry.place(relx=0.5, rely=0.4, anchor=tk.W)
        self.mother_phno_entry = tk.Entry(right_frame, bg="white")
        self.mother_phno_entry.place(relx=0.5, rely=0.45, anchor=tk.W)
        self.hostel_entry = tk.Entry(right_frame, bg="white")
        self.hostel_entry.insert(tk.END, self.selected_hostel)
        self.hostel_entry.config(state="readonly")
        self.hostel_entry.place(relx=0.5, rely=0.5, anchor=tk.W)
        self.state_entry = tk.Entry(right_frame, bg="white")
        self.state_entry.place(relx=0.5, rely=0.55, anchor=tk.W)
        self.city_entry = tk.Entry(right_frame, bg="white")
        self.city_entry.place(relx=0.5, rely=0.6, anchor=tk.W)
        self.submit_button = tk.Button(right_frame, text="Submit", command=self.register, bg=COLOR_PRIMARY, fg=COLOR_LIGHT_TEXT, font=("Helvetica", 12))
        self.submit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        self.go_back_button = tk.Button(right_frame, text="Go Back", command=self.go_back, bg=COLOR_SECONDARY, fg=COLOR_LIGHT_TEXT, font=("Helvetica", 12))
        self.go_back_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

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

        self.save_to_database(name, email, branch, phno, father_name, father_phno, mother_name, mother_phno, hostel, state, city)
        self.destroy()
        self.master.thank_you_page = ThankYouPage(self.master, hostel_name=self.selected_hostel)

    def save_to_database(self, name, email, branch, phno, father_name, father_phno, mother_name, mother_phno, hostel, state, city):
        conn = sqlite3.connect('C:/python project/hosteldb.db')
        cursor=conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        branch TEXT,
                        phone_number INTEGER NOT NULL,
                        fathers_name TEXT,
                        fathers_phone_number INTEGER NOT NULL,
                        mothers_name TEXT,
                        mothers_phone_number INTEGER NOT NULL,
                        hostel TEXT,
                        state TEXT,
                        city TEXT
                            )''')
        cursor.execute('''INSERT INTO registrations 
                    (name, email, branch, phone_number, fathers_name, fathers_phone_number, mothers_name, mothers_phone_number, hostel, state, city)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name, email, branch, phno, father_name, father_phno, mother_name, mother_phno, hostel, state, city))
        conn.commit()
        conn.close()

    def go_back(self):
        self.destroy()
        self.master.hostel_page = HostelPage(self.master, hostel_name=self.selected_hostel)

    def resize_image(self, image, width, height):
        aspect_ratio = min(width / image.width, height / image.height)
        new_width = max(1, int(image.width * aspect_ratio * 0.6))
        new_height = max(1, int(image.height * aspect_ratio * 0.6))
        resized_image = image.resize((new_width, new_height))
        return ImageTk.PhotoImage(resized_image)
class ThankYouPage(CenteredFrame):
    def __init__(self, master=None, hostel_name=None):
        super().__init__(master)
        self.hostel_name = hostel_name
        self.create_widgets()

    def create_widgets(self):
        blue_frame = tk.Frame(self, bg="#87CEEB")
        blue_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        bg_image_path = "C:/python project/svecw6.png"
        original_image = Image.open(bg_image_path)
        resized_image = original_image.resize((800, 600))
        self.bg1_photo = ImageTk.PhotoImage(resized_image)
        self.bg1_label = tk.Label(blue_frame, image=self.bg1_photo)
        self.bg1_label.place(relx=0.5, rely=0.5, anchor="center")
        thank_you_label = tk.Label(blue_frame, text="Thank You!", font=("Helvetica", 16, "bold"), bg="#FFFFFF")
        thank_you_label.place(relx=0.5, rely=0.3, anchor="center")
        success_label = tk.Label(blue_frame, text=f"Your slot for {self.hostel_name} has been booked successfully.", font=("Helvetica", 12), bg="#FFFFFF")
        success_label.place(relx=0.5, rely=0.4, anchor="center")
        notification_label = tk.Label(blue_frame, text="You will be notified soon.", font=("Helvetica", 12), bg="#FFFFFF")
        notification_label.place(relx=0.5, rely=0.5, anchor="center")
        logout_button = tk.Button(blue_frame, text="Logout", command=self.logout, bg="green", fg="white")
        logout_button.place(relx=0.5, rely=0.6, anchor="center")
    def logout(self):
        self.destroy()
        self.master.switch_frame(signup_page)
root=tk.Tk()
root.title("Hostel booking system")
app = signup_page(root)
app.center_on_screen(1250,550)
root.iconbitmap("C:/python project/login logo.ico")
root.mainloop()