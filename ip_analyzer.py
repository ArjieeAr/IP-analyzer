"""
IP Analyzer Application - GUI Version
-----------------------------------------
This program provides a graphical user interface to retrieve a computer's
public IPv4 and IPv6 addresses and provides additional network details
such as ISP, ASN, and location.

APIs Used:
1. ipify.org  - for retrieving the current public IP addresses (IPv4 & IPv6)
2. ip-api.com - for retrieving geolocation, ISP, and ASN information

Author: NovaTech
Version: 2.0 (GUI)
"""

"""
IP Analyzer Application - GUI Version
-----------------------------------------
This program provides a graphical user interface to retrieve a computer's
public IPv4 and IPv6 addresses and provides additional network details
such as ISP, ASN, and location.

APIs Used:
1. ipify.org  - for retrieving the current public IP addresses (IPv4 & IPv6)
2. ip-api.com - for retrieving geolocation, ISP, and ASN information

Author: NovaTech
Version: 2.0 (GUI)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading


class IPAnalyzerGUI:
    """GUI Application for IP Analysis"""
    
    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("IP Analyzer")
        self.root.geometry("420x700")
        self.root.resizable(False, False)
        
        # Color palette
        self.colors = {
            'bg': '#F5F6FA',
            'panel': '#FFFFFF',
            'border': '#D9D9D9',
            'primary': '#4A90E2',
            'accent': '#27AE60',
            'success': '#2ECC71',
            'text': '#333333',
            'text_secondary': '#555555'
        }
        
        # Store current results for clipboard
        self.current_results = ""
        
        # Configure style
        self.setup_styles()
        
        # Set background color
        self.root.configure(bg=self.colors['bg'])
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title Label
        title_label = ttk.Label(
            self.main_frame, 
            text="IP Analyzer", 
            font=("Helvetica", 14, "bold"),
            foreground=self.colors['text']
        )
        title_label.pack(pady=(0, 10))
        
        # Button Frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Analyze Button (Primary)
        self.analyze_button = ttk.Button(
            button_frame,
            text="Analyze IP",
            command=self.on_analyze_click,
            style='Primary.TButton'
        )
        self.analyze_button.pack(side=tk.LEFT, expand=True, padx=4)
        
        # Clear Button (Secondary)
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self.on_clear_click,
            style='Secondary.TButton'
        )
        self.clear_button.pack(side=tk.LEFT, expand=True, padx=4)
        
        # Copy to Clipboard Button (Secondary)
        self.copy_button = ttk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self.on_copy_click,
            style='Secondary.TButton'
        )
        self.copy_button.pack(side=tk.LEFT, expand=True, padx=4)
        
        # Status Frame (Full width with background)
        self.status_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['primary'],
            height=35
        )
        self.status_frame.pack(fill=tk.X, pady=(0, 15))
        self.status_frame.pack_propagate(False)
        
        # Status Label
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            foreground='white',
            font=("Helvetica", 10, "bold"),
            bg=self.colors['primary']
        )
        self.status_label.pack(expand=True, pady=8)
        
        # Results Frame
        results_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['panel'],
            relief=tk.FLAT,
            bd=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results label inside frame
        results_label = tk.Label(
            results_frame,
            text="Results",
            bg=self.colors['panel'],
            fg=self.colors['text'],
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=5
        )
        results_label.pack(anchor='w')
        
        # Separator
        separator = tk.Frame(
            results_frame,
            bg=self.colors['border'],
            height=1
        )
        separator.pack(fill=tk.X)
        
        # Scrollable frame for results
        self.scrollable_frame = tk.Frame(
            results_frame,
            bg=self.colors['panel']
        )
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Footer separator and label
        footer_separator = tk.Frame(
            self.main_frame,
            bg=self.colors['border'],
            height=1
        )
        footer_separator.pack(fill=tk.X, pady=(10, 0))

        footer_label = tk.Label(
            self.main_frame,
            text="© NovaTech 2025 — All rights reserved",
            bg=self.colors['bg'],
            fg=self.colors['text_secondary'],
            font=("Helvetica", 8)
        )
        footer_label.pack(pady=(6, 0))
    
    def setup_styles(self):
        """Setup custom ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure main frame style
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text'])
        
        # Primary Button Style
        style.configure('Primary.TButton',
                       font=('Helvetica', 10, 'bold'),
                       foreground='white',
                       background=self.colors['primary'],
                       borderwidth=1,
                       relief='solid',
                       padding=6)
        
        style.map('Primary.TButton',
                 background=[('active', '#357ABD'), ('pressed', '#2E5A99')])
        
        # Secondary Button Style
        style.configure('Secondary.TButton',
                       font=('Helvetica', 10),
                       foreground=self.colors['primary'],
                       background=self.colors['panel'],
                       borderwidth=2,
                       relief='solid',
                       padding=6)
        
        style.map('Secondary.TButton',
                 background=[('active', '#E8F0FE'), ('pressed', '#D0E1FB')],
                 foreground=[('active', '#2E5A99')])
    
    def get_ip(self, version="ipv4"):
        """
        Retrieves the public IP address for the specified version (IPv4 or IPv6).
        
        Parameters:
            version (str): The IP version to retrieve ("ipv4" or "ipv6").
        
        Returns:
            str: The public IP address or an error message if retrieval fails.
        """
        try:
            if version == "ipv6":
                url = "https://api64.ipify.org?format=json"
            else:
                url = "https://api.ipify.org?format=json"

            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json().get("ip")
        
        except Exception as e:
            return f"Error: {e}"
    
    def get_ip_info(self):
        """
        Retrieves geolocation and ISP information using ip-api.com.
        This API has better rate limits for free tier usage.
        
        Returns:
            dict: A dictionary containing location, ISP, and timezone information.
        """
        try:
            # Using ip-api.com which has better free tier rate limits
            response = requests.get("http://ip-api.com/json/", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Check if the API returned an error
            if data.get('status') == 'fail':
                return {"error": data.get('message', 'API error')}
            
            return data
        except Exception as e:
            return {"error": str(e)}
    
    def clear_results(self):
        """Clear all result labels"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def add_label(self, text, is_header=False):
        """Add a label to the results frame"""
        if is_header:
            # Add separator before header
            separator = tk.Frame(
                self.scrollable_frame,
                bg=self.colors['border'],
                height=1
            )
            separator.pack(fill=tk.X, pady=(15, 10))
            
            label = tk.Label(
                self.scrollable_frame,
                text=text,
                font=("Helvetica", 10, "bold"),
                foreground=self.colors['primary'],
                bg=self.colors['panel'],
                anchor='w',
                justify='left',
                wraplength=0
            )
            label.pack(anchor=tk.W, pady=(0, 8), fill=tk.X)
        else:
            label = tk.Label(
                self.scrollable_frame,
                text=text,
                font=("Helvetica", 9),
                foreground=self.colors['text_secondary'],
                bg=self.colors['panel'],
                anchor='w',
                justify='left'
            )
            label.pack(anchor=tk.W, pady=4, fill=tk.X)
    
    def display_results(self, ipv4, ipv6, info):
        """Display the results in the GUI"""
        self.clear_results()
        
        if "error" in info:
            error_label = tk.Label(
                self.scrollable_frame,
                text=f"Error: {info['error']}",
                font=("Helvetica", 10),
                foreground='#E74C3C',
                bg=self.colors['panel']
            )
            error_label.pack(anchor=tk.W, pady=10)
            self.current_results = f"Error: {info['error']}"
            return
        
        # Build results text for clipboard
        results_text = []
        results_text.append(f"IPv4 Address: {ipv4}")
        results_text.append(f"IPv6 Address: {ipv6}")
        results_text.append("")
        results_text.append("Location Information")
        results_text.append(f"City: {info.get('city', 'N/A')}")
        results_text.append(f"Region: {info.get('region', 'N/A')}")
        results_text.append(f"Country: {info.get('country', 'N/A')}")
        results_text.append(f"Country Code: {info.get('countryCode', 'N/A')}")
        results_text.append(f"Postal Code: {info.get('zip', 'N/A')}")
        results_text.append("")
        results_text.append("Geographic Coordinates")
        results_text.append(f"Latitude: {info.get('lat', 'N/A')}")
        results_text.append(f"Longitude: {info.get('lon', 'N/A')}")
        results_text.append("")
        results_text.append("Network Information")
        results_text.append(f"ISP: {info.get('isp', 'N/A')}")
        results_text.append(f"Timezone: {info.get('timezone', 'N/A')}")
        
        self.current_results = "\n".join(results_text)
        
        # Display on GUI
        # IPv4 and IPv6
        ipv4_label = tk.Label(
            self.scrollable_frame,
            text=f"IPv4 Address: {ipv4}",
            font=("Helvetica", 9),
            foreground=self.colors['primary'],
            bg=self.colors['panel'],
            anchor='w',
            justify='left'
        )
        ipv4_label.pack(anchor=tk.W, pady=4, fill=tk.X)
        
        ipv6_label = tk.Label(
            self.scrollable_frame,
            text=f"IPv6 Address: {ipv6}",
            font=("Helvetica", 9),
            foreground=self.colors['primary'],
            bg=self.colors['panel'],
            anchor='w',
            justify='left'
        )
        ipv6_label.pack(anchor=tk.W, pady=4, fill=tk.X)
        
        # Location Information
        self.add_label("📍  Location Information", is_header=True)
        self.add_label(f"City: {info.get('city', 'N/A')}")
        self.add_label(f"Region: {info.get('region', 'N/A')}")
        self.add_label(f"Country: {info.get('country', 'N/A')}")
        self.add_label(f"Country Code: {info.get('countryCode', 'N/A')}")
        self.add_label(f"Postal Code: {info.get('zip', 'N/A')}")
        
        # Geographic Coordinates
        self.add_label("🗺️  Geographic Coordinates", is_header=True)
        self.add_label(f"Latitude: {info.get('lat', 'N/A')}")
        self.add_label(f"Longitude: {info.get('lon', 'N/A')}")
        
        # Network Information
        self.add_label("🌐  Network Information", is_header=True)
        self.add_label(f"ISP: {info.get('isp', 'N/A')}")
        self.add_label(f"Timezone: {info.get('timezone', 'N/A')}")
    
    def analyze_in_background(self):
        """Perform IP analysis in a background thread"""
        try:
            self.update_status("Fetching IPv4 address...", "loading")
            ipv4 = self.get_ip("ipv4")
            
            self.update_status("Fetching IPv6 address...", "loading")
            ipv6 = self.get_ip("ipv6")
            
            self.update_status("Fetching location and ISP information...", "loading")
            info = self.get_ip_info()
            
            # Display results
            self.display_results(ipv4, ipv6, info)
            self.update_status("Analysis complete!", "success")
            
        except Exception as e:
            error_msg = f"An error occurred: {e}"
            self.clear_results()
            error_label = tk.Label(
                self.scrollable_frame,
                text=error_msg,
                font=("Helvetica", 10),
                foreground='#E74C3C',
                bg=self.colors['panel']
            )
            error_label.pack(anchor=tk.W, pady=10)
            self.update_status("Error occurred", "error")
            messagebox.showerror("Error", error_msg)
    
    def update_status(self, message, status_type="default"):
        """Update the status label with background color
        
        Args:
            message (str): The status message
            status_type (str): Type of status - 'default', 'loading', 'success', or 'error'
        """
        color_map = {
            'default': self.colors['primary'],
            'loading': '#3498DB',  # Light blue
            'success': self.colors['success'],  # Green
            'error': '#E74C3C'  # Red
        }
        
        bg_color = color_map.get(status_type, self.colors['primary'])
        self.status_frame.config(bg=bg_color)
        self.status_label.config(text=message, bg=bg_color, foreground='white')
        self.root.update_idletasks()
    
    def on_analyze_click(self):
        """Handle analyze button click"""
        self.analyze_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        self.copy_button.config(state=tk.DISABLED)
        
        # Run analysis in background thread
        thread = threading.Thread(target=self.analyze_in_background, daemon=True)
        thread.start()
        
        # Re-enable buttons after thread completes
        def enable_buttons():
            if thread.is_alive():
                self.root.after(100, enable_buttons)
            else:
                self.analyze_button.config(state=tk.NORMAL)
                self.clear_button.config(state=tk.NORMAL)
                self.copy_button.config(state=tk.NORMAL)
        
        enable_buttons()
    
    def on_clear_click(self):
        """Handle clear button click"""
        self.clear_results()
        self.current_results = ""
        self.update_status("Ready", "default")
    
    def on_copy_click(self):
        """Handle copy to clipboard button click"""
        if not self.current_results:
            messagebox.showinfo("Copy", "No results to copy. Please run analysis first.")
            return
        
        try:
            # Copy to clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_results)
            self.root.update()
            messagebox.showinfo("Copy", "Results copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy to clipboard: {e}")


def main():
    """Main function to launch the GUI application"""
    root = tk.Tk()
    app = IPAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
