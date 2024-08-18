import tkinter as tk
from tkinter import scrolledtext
from tkhtmlview import HTMLLabel
import requests
import json

# Your Bing Search API key
API_KEY = "input API key here"

def search():
    query = entry.get()
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"q": query, "count": 10, "textDecorations": True, "textFormat": "HTML"}
    
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()
        display_results(results)
    else:
        result_label.set_html("<p style='color:black;'>Error fetching search results</p>")

def display_results(results):
    html_content = ""
    
    if 'webPages' in results and 'value' in results['webPages']:
        for item in results['webPages']['value']:
            title = item['name']
            url = item['url']
            snippet = item.get('snippet', 'No description available')
            
            # Format the HTML content using inline CSS for the color black
            html_content += f"""
            <div class="p-4 border-b border-gray-200">
                <h2 class="text-xl font-bold" style="color:black;"><a href="{url}" class="text-black-500" target="_blank">{title}</a></h2>
                <p style="color:black;">{snippet}</p>
                <a href="{url}" class="text-black-500 underline" target="_blank">{url}</a>
            </div>
            """
    else:
        html_content = "<p style='color:black;'>No results found</p>"

    # Update the HTMLLabel with the formatted HTML content
    result_label.set_html(f"""
    <div class="prose">
        {html_content}
    </div>
    """)

# Create the main window
root = tk.Tk()
root.title("Quick Web Search")

# Create an entry widget for the search query with increased width
entry = tk.Entry(root, width=70)
entry.pack(pady=10)

# Bind the Enter key to the search function
entry.bind("<Return>", lambda event: search())

# Create a search button
search_button = tk.Button(root, text="Search", command=search)
search_button.pack(pady=10)

# Create a scrolledtext widget for displaying the search results
scroll_frame = tk.Frame(root)
scroll_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Create an HTMLLabel to display the HTML formatted results with initial blue text
result_label = HTMLLabel(scroll_frame, html="<p style='color:blue;'>Search results will be displayed here...</p>", width=80, height=20)
result_label.pack(pady=10, fill=tk.BOTH, expand=True)

# Add a vertical scrollbar
scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=result_label.yview)
scrollbar.pack(side="right", fill="y")

result_label.config(yscrollcommand=scrollbar.set)

# Run the application
root.mainloop()
