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

def scrape_proxies():
    url = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=ipport&format=text"  # Example API to scrape proxies from
    response = requests.get(url)
    proxies = []
    if response.status_code == 200:
        proxies = response.text.split('\n')
        proxies = [proxy.strip() for proxy in proxies if proxy.strip()]
    else:
        print(f"Failed to retrieve the proxies. Status code: {response.status_code}")
    return proxies

def main():
    root = tk.Tk()
    root.title("Proxy Checker")
    root.geometry("600x640")
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

    # Create the Listbox with custom appearance
    proxy_listbox = tk.Listbox(
        listbox_frame, 
        width=70, 
        height=15, 
        font=("Helvetica", 10), 
        bg="#ffffff",  # Background color
        fg="#000000",  # Foreground (text) color
        selectbackground="#cce7ff",  # Background color of selected item
        selectforeground="#000000",  # Foreground color of selected item
        highlightbackground="#d9d9d9",  # Border color
        highlightcolor="#d9d9d9"  # Border color when focused
    )
    proxy_listbox.pack(side=tk.LEFT)

    # Create the Scrollbar and link it to the Listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    proxy_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=proxy_listbox.yview)

    # Labels to display the count of working and dead proxies
    working_proxies_label = tk.Label(root, text="Working Proxies: 0", font=("Helvetica", 12), bg="#f0f0f0", fg="green")
    working_proxies_label.pack(pady=5)
    dead_proxies_label = tk.Label(root, text="Dead Proxies: 0", font=("Helvetica", 12), bg="#f0f0f0", fg="red")
    dead_proxies_label.pack(pady=5)

    # Counters for working and dead proxies
    working_proxies_count = 0
    dead_proxies_count = 0

    def update_proxy_counts():
        working_proxies_label.config(text=f"Working Proxies: {working_proxies_count}")
        dead_proxies_label.config(text=f"Dead Proxies: {dead_proxies_count}")
        root.update_idletasks()  # Ensure the UI is updated

    def check_button_click():
        nonlocal working_proxies_count, dead_proxies_count
        proxy = proxy_entry.get()
        is_working, elapsed_time = check_proxy(proxy)
        if is_working:
            result_label.config(text=f"Proxy works! Response time: {elapsed_time:.2f} seconds", fg="green")
            save_valid_proxy(proxy, 'valid.txt')
            proxy_listbox.insert(tk.END, f"{proxy} - {elapsed_time:.2f} seconds")
            proxy_listbox.itemconfig(tk.END, {'fg':'green'})
            working_proxies_count += 1
        else:
            result_label.config(text="Proxy does not work.", fg="red")
            proxy_listbox.insert(tk.END, f"{proxy} - does not work")
            proxy_listbox.itemconfig(tk.END, {'fg':'red'})
            dead_proxies_count += 1
        update_proxy_counts()

    def check_proxies_from_file():
        nonlocal working_proxies_count, dead_proxies_count
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
                            working_proxies_count += 1
                        else:
                            result_label.config(text=f"Proxy {proxy} does not work.", fg="red")
                            proxy_listbox.insert(tk.END, f"{proxy} - does not work")
                            proxy_listbox.itemconfig(tk.END, {'fg':'red'})
                            dead_proxies_count += 1
                        update_proxy_counts()  # Update counts after each proxy check
                        root.update()  # Update the UI to show the result of each proxy check
                if not valid_proxies:
                    result_label.config(text="No valid proxies found.", fg="red")
                update_proxy_counts()
            else:
                result_label.config(text="No proxies found in file.", fg="red")
        else:
            result_label.config(text="No file selected.", fg="red")

    def scrape_proxies_button_click():
        nonlocal working_proxies_count, dead_proxies_count
        proxies = scrape_proxies()
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
                        working_proxies_count += 1
                    else:
                        result_label.config(text=f"Proxy {proxy} does not work.", fg="red")
                        proxy_listbox.insert(tk.END, f"{proxy} - does not work")
                        proxy_listbox.itemconfig(tk.END, {'fg':'red'})
                        dead_proxies_count += 1
                    update_proxy_counts()  # Update counts after each proxy check
                    root.update()  # Update the UI to show the result of each proxy check
            if not valid_proxies:
                result_label.config(text="No valid proxies found.", fg="red")
            else:
                result_label.config(text=f"Scraped {len(valid_proxies)} valid proxies.", fg="blue")
            update_proxy_counts()
        else:
            result_label.config(text="Failed to scrape proxies.", fg="red")

    check_button = tk.Button(root, text="Check Proxy", command=check_button_click, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    check_button.pack(pady=5)

    check_file_button = tk.Button(root, text="Check Proxies from File", command=check_proxies_from_file, font=("Helvetica", 12), bg="#2196F3", fg="white", padx=10, pady=5)
    check_file_button.pack(pady=5)

    scrape_button = tk.Button(root, text="Scrape Proxies and Checker", command=scrape_proxies_button_click, font=("Helvetica", 12), bg="#FF9800", fg="white", padx=10, pady=5)
    scrape_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
