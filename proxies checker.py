import tkinter as tk
from tkinter import filedialog
import requests
import time

def check_proxy(proxy):
    try:
        start_time = time.time()
        response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=0.5)
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            return True, elapsed_time
        else:
            return False, None
    except Exception:
        return False, None

def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]

def save_valid_proxy(proxy, file_path):
    with open(file_path, 'a') as file:
        file.write(proxy + '\n')

def main():
    root = tk.Tk()
    root.title("Proxy Checker")
    root.geometry("600x400")
    root.configure(bg="#f0f0f0")

    title_label = tk.Label(root, text="Proxy Checker", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    proxy_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
    proxy_entry.pack(pady=5)

    result_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#f0f0f0")
    result_label.pack(pady=5)

    # Create a frame to hold the Listbox and Scrollbar
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(pady=10)

    # Create the Listbox
    proxy_listbox = tk.Listbox(listbox_frame, width=70, height=15, font=("Helvetica", 10))
    proxy_listbox.pack(side=tk.LEFT)

    # Create the Scrollbar and link it to the Listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    proxy_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=proxy_listbox.yview)

    def check_button_click():
        proxy = proxy_entry.get()
        is_working, elapsed_time = check_proxy(proxy)
        if is_working:
            result_label.config(text=f"Proxy works! Response time: {elapsed_time:.2f} seconds", fg="green")
            save_valid_proxy(proxy, 'valid.txt')
            proxy_listbox.insert(tk.END, f"{proxy} - {elapsed_time:.2f} seconds")
            proxy_listbox.itemconfig(tk.END, {'fg':'green'})
        else:
            result_label.config(text="Proxy does not work.", fg="red")
            proxy_listbox.insert(tk.END, f"{proxy} - does not work")
            proxy_listbox.itemconfig(tk.END, {'fg':'red'})

    def check_proxies_from_file():
        file_path = filedialog.askopenfilename(title="Select Proxy File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            proxies = read_proxies_from_file(file_path)
            if proxies:
                valid_proxies = []
                for proxy in proxies:
                    if ":" in proxy:  # Ensure the proxy is in the format server:port
                        is_working, elapsed_time = check_proxy(proxy)
                        if is_working:
                            valid_proxies.append(proxy)
                            result_label.config(text=f"Proxy {proxy} works! Response time: {elapsed_time:.2f} seconds", fg="green")
                            save_valid_proxy(proxy, 'valid.txt')
                            proxy_listbox.insert(tk.END, f"{proxy} - {elapsed_time:.2f} seconds")
                            proxy_listbox.itemconfig(tk.END, {'fg':'green'})
                        else:
                            result_label.config(text=f"Proxy {proxy} does not work.", fg="red")
                            proxy_listbox.insert(tk.END, f"{proxy} - does not work")
                            proxy_listbox.itemconfig(tk.END, {'fg':'red'})
                        root.update()  # Update the UI to show the result of each proxy check
                if not valid_proxies:
                    result_label.config(text="No valid proxies found.", fg="red")
            else:
                result_label.config(text="No proxies found in file.", fg="red")
        else:
            result_label.config(text="No file selected.", fg="red")

    check_button = tk.Button(root, text="Check Proxy", command=check_button_click, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    check_button.pack(pady=5)

    check_file_button = tk.Button(root, text="Check Proxies from File", command=check_proxies_from_file, font=("Helvetica", 12), bg="#2196F3", fg="white", padx=10, pady=5)
    check_file_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()