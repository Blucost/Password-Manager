import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # JSON Files to save passwords and PINs
        self.passwords_file = None
        self.pin_file = "pin.json"

        # Directory to store account files
        self.accounts_directory = "accounts"
        if not os.path.exists(self.accounts_directory):
            os.makedirs(self.accounts_directory)

        # Variables for user input
        self.login_pin_var = tk.StringVar()
        self.section_name_var = tk.StringVar()
        self.password_name_var = tk.StringVar()
        self.new_password_var = tk.StringVar()

        # Start with the login UI
        self.login_ui()

    def login_ui(self):
        """Set up the login UI."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame for login
        login_frame = ttk.LabelFrame(self.root, text="Login")
        login_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(login_frame, text="Enter PIN:").pack(side="left", padx=5, pady=5)
        pin_entry = ttk.Entry(login_frame, textvariable=self.login_pin_var, show="*")
        pin_entry.pack(side="left", padx=5, pady=5)

        login_button = ttk.Button(login_frame, text="Login", command=self.login_account)
        login_button.pack(side="left", padx=5, pady=5)

        create_account_button = ttk.Button(login_frame, text="Create Account", command=self.create_account_ui)
        create_account_button.pack(side="left", padx=5, pady=5)

    def create_account_ui(self):
        """Set up the UI for account creation."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame for creating account
        account_frame = ttk.LabelFrame(self.root, text="Create Account")
        account_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(account_frame, text="Enter PIN (4 digits):").pack(side="left", padx=5, pady=5)
        pin_entry = ttk.Entry(account_frame, textvariable=self.login_pin_var, show="*")
        pin_entry.pack(side="left", padx=5, pady=5)

        create_account_button = ttk.Button(account_frame, text="Create Account", command=self.create_account)
        create_account_button.pack(side="left", padx=5, pady=5)

        back_button = ttk.Button(account_frame, text="Back", command=self.login_ui)
        back_button.pack(side="left", padx=5, pady=5)

    def main_ui(self):
        """Set up the main UI for the password manager."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame for adding sections
        section_frame = ttk.LabelFrame(self.root, text="Add Section")
        section_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(section_frame, text="Section Name:").pack(side="left", padx=5, pady=5)
        section_entry = ttk.Entry(section_frame, textvariable=self.section_name_var)
        section_entry.pack(side="left", padx=5, pady=5)

        add_section_button = ttk.Button(section_frame, text="Add Section", command=self.add_section)
        add_section_button.pack(side="left", padx=5, pady=5)

        # Treeview to display sections and passwords
        self.sections_tree = ttk.Treeview(self.root, columns=("Password"), show="tree headings")
        self.sections_tree.heading("#0", text="Sections / Passwords")
        self.sections_tree.heading("Password", text="Password")
        self.sections_tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Frame for adding passwords
        password_frame = ttk.LabelFrame(self.root, text="Add Password")
        password_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(password_frame, text="Password Name:").grid(row=0, column=0, padx=5, pady=5)
        password_name_entry = ttk.Entry(password_frame, textvariable=self.password_name_var)
        password_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(password_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        new_password_entry = ttk.Entry(password_frame, textvariable=self.new_password_var, show="*")
        new_password_entry.grid(row=1, column=1, padx=5, pady=5)

        add_password_button = ttk.Button(password_frame, text="Add Password", command=self.add_password)
        add_password_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Delete button
        delete_button = ttk.Button(self.root, text="Delete Selected", command=self.delete_selected)
        delete_button.pack(pady=10)

        logout_button = ttk.Button(self.root, text="Logout", command=self.login_ui)
        logout_button.pack(pady=10)

        # Load sections from the JSON file
        self.load_sections()

    def load_passwords(self):
        """Load passwords from the JSON file."""
        if os.path.exists(self.passwords_file):
            with open(self.passwords_file, "r") as file:
                return json.load(file)
        return {}

    def save_passwords(self, passwords):
        """Save passwords to the JSON file."""
        with open(self.passwords_file, "w") as file:
            json.dump(passwords, file, indent=4)

    def load_sections(self):
        """Load sections and passwords into the Treeview."""
        passwords = self.load_passwords()
        for section, items in passwords.items():
            section_id = self.sections_tree.insert("", "end", text=section, open=True)
            for password_name, password in items.items():
                self.sections_tree.insert(section_id, "end", text=password_name, values=(password,))

    def add_section(self):
        """Add a new section."""
        section_name = self.section_name_var.get().strip()

        if not section_name:
            messagebox.showerror("Error", "Section name cannot be empty.")
            return

        passwords = self.load_passwords()

        if section_name in passwords:
            messagebox.showerror("Error", f"Section '{section_name}' already exists.")
            return

        passwords[section_name] = {}
        self.save_passwords(passwords)

        self.sections_tree.insert("", "end", text=section_name, open=True)
        self.section_name_var.set("")

    def add_password(self):
        """Add a new password to the selected section."""
        selected_section = self.sections_tree.selection()

        if not selected_section:
            messagebox.showerror("Error", "Please select a section to add the password.")
            return

        section_id = selected_section[0]
        password_name = self.password_name_var.get().strip()
        password = self.new_password_var.get().strip()

        if not password_name or not password:
            messagebox.showerror("Error", "Please fill out both the password name and password fields.")
            return

        passwords = self.load_passwords()

        section_name = self.sections_tree.item(section_id, "text")
        if section_name in passwords:
            passwords[section_name][password_name] = password
            self.save_passwords(passwords)
            self.sections_tree.insert(section_id, "end", text=password_name, values=(password,))
            self.password_name_var.set("")
            self.new_password_var.set("")
        else:
            messagebox.showerror("Error", "The selected section does not exist in the database.")

    def delete_selected(self):
        """Delete the selected section or password."""
        selected_item = self.sections_tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a section or password to delete.")
            return

        selected_id = selected_item[0]
        parent_id = self.sections_tree.parent(selected_id)
        item_name = self.sections_tree.item(selected_id, "text")

        passwords = self.load_passwords()

        if parent_id == "":
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the section '{item_name}'?"):
                passwords.pop(item_name, None)
                self.save_passwords(passwords)
                self.sections_tree.delete(selected_id)
        else:
            parent_name = self.sections_tree.item(parent_id, "text")
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the password '{item_name}'?"):
                passwords[parent_name].pop(item_name, None)
                self.save_passwords(passwords)
                self.sections_tree.delete(selected_id)

    def login_account(self):
        """Log into an account using a PIN."""
        pin = self.login_pin_var.get().strip()

        if not pin:
            messagebox.showerror("Error", "Please enter your PIN.")
            return

        account_path = os.path.join(self.accounts_directory, f"{pin}.json")
        if os.path.exists(account_path):
            self.passwords_file = account_path
            self.main_ui()
        else:
            messagebox.showerror("Error", "Account with this PIN does not exist.")

    def create_account(self):
        """Create a new account with a 4-digit PIN."""
        pin = self.login_pin_var.get().strip()

        if len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN must be a 4-digit number.")
            return

        account_path = os.path.join(self.accounts_directory, f"{pin}.json")
        if os.path.exists(account_path):
            messagebox.showerror("Error", "Account with this PIN already exists.")
            return

        account_data = {"pin": pin, "passwords": {}}
        with open(account_path, "w") as file:
            json.dump(account_data, file, indent=4)

        messagebox.showinfo("Success", "Account created successfully!")
        self.login_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
