import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

class MemoryMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Matrix")
        self.root.geometry("1000x800")
        self.root.configure(bg='#0a0a0a')
        
        style = ttk.Style()
        style.configure("Cyberpunk.TFrame", background='#0a0a0a')
        style.configure("Cyberpunk.TLabel", 
                       background='#0a0a0a', 
                       foreground='#00ff41',
                       font=('Courier', 10))
        style.configure("Cyberpunk.TButton",
                       background='#00ff41',
                       foreground='#0a0a0a',
                       font=('Courier', 10))
        
        # Main frame
        self.main_frame = ttk.Frame(root, style="Cyberpunk.TFrame")
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(self.main_frame, 
                         text="MEMORY MATRIX",
                         style="Cyberpunk.TLabel",
                         font=('Courier', 24, 'bold'))
        title.pack(pady=(0, 20))
        
        # Status Guide
        guide_frame = ttk.Frame(self.main_frame, style="Cyberpunk.TFrame")
        guide_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(guide_frame, 
                 text="HIT: Page found in memory (Fast)",
                 style="Cyberpunk.TLabel",
                 foreground='#00ff41').pack(side=tk.LEFT, padx=10)
        ttk.Label(guide_frame,
                 text="MISS: Page not in memory (Slow)",
                 style="Cyberpunk.TLabel",
                 foreground='#ff4141').pack(side=tk.RIGHT, padx=10)
        
        # Input Frame
        input_frame = ttk.Frame(self.main_frame, style="Cyberpunk.TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Pages Input
        ttk.Label(input_frame, 
                 text="INPUT SEQUENCE:",
                 style="Cyberpunk.TLabel").pack(anchor=tk.W)
        self.pages_entry = ttk.Entry(input_frame)
        self.pages_entry.pack(fill=tk.X, pady=(5, 10))
        self.pages_entry.insert(0, "1,2,3,4,1,2,5,1,2,3,4,5")
        
        # Frames Input
        ttk.Label(input_frame,
                 text="MEMORY FRAMES:",
                 style="Cyberpunk.TLabel").pack(anchor=tk.W)
        self.frames_entry = ttk.Entry(input_frame)
        self.frames_entry.pack(fill=tk.X, pady=(5, 10))
        self.frames_entry.insert(0, "3")
        
        # Algorithm Selection
        ttk.Label(input_frame,
                 text="ALGORITHM:",
                 style="Cyberpunk.TLabel").pack(anchor=tk.W)
        self.algorithm = tk.StringVar(value="fifo")
        ttk.Radiobutton(input_frame,
                       text="FIFO (First In, First Out)",
                       variable=self.algorithm,
                       value="fifo",
                       style="Cyberpunk.TLabel").pack(anchor=tk.W)
        ttk.Radiobutton(input_frame,
                       text="LRU (Least Recently Used)",
                       variable=self.algorithm,
                       value="lru",
                       style="Cyberpunk.TLabel").pack(anchor=tk.W)
        
        # Run Button
        ttk.Button(input_frame,
                  text="RUN",
                  command=self.run_simulation,
                  style="Cyberpunk.TButton").pack(fill=tk.X, pady=(20, 0))
        
        # Results Frame
        self.results_frame = ttk.Frame(self.main_frame, style="Cyberpunk.TFrame")
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Table
        self.table = ttk.Treeview(self.results_frame,
                                columns=("step", "page", "memory", "status"),
                                show="headings",
                                style="Cyberpunk.Treeview")
        self.table.heading("step", text="STEP")
        self.table.heading("page", text="PAGE")
        self.table.heading("memory", text="MEMORY STATE")
        self.table.heading("status", text="STATUS")
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Stats Label
        self.stats_label = ttk.Label(self.results_frame,
                                   text="",
                                   style="Cyberpunk.TLabel")
        self.stats_label.pack(pady=10)

    def fifo_replacement(self, frames, pages):
        memory = deque(maxlen=frames)
        page_faults = 0
        steps = []
        
        for i, page in enumerate(pages, 1):
            if page not in memory:
                page_faults += 1
                if len(memory) == frames:
                    memory.popleft()
                memory.append(page)
                status = "MISS"
            else:
                status = "HIT"
            
            steps.append({
                'step': i,
                'page': page,
                'memory': list(memory),
                'status': status
            })
        
        return steps, page_faults

    def lru_replacement(self, frames, pages):
        memory = []
        page_faults = 0
        steps = []
        
        for i, page in enumerate(pages, 1):
            if page not in memory:
                page_faults += 1
                if len(memory) == frames:
                    memory.pop(0)
                memory.append(page)
                status = "MISS"
            else:
                memory.remove(page)
                memory.append(page)
                status = "HIT"
            
            steps.append({
                'step': i,
                'page': page,
                'memory': list(memory),
                'status': status
            })
        
        return steps, page_faults

    def run_simulation(self):
        try:
            # Clear previous results
            for item in self.table.get_children():
                self.table.delete(item)
            
            # Get input values
            pages = [int(x.strip()) for x in self.pages_entry.get().split(',')]
            frames = int(self.frames_entry.get())
            algorithm = self.algorithm.get()
            
            # Run simulation
            if algorithm == "fifo":
                steps, faults = self.fifo_replacement(frames, pages)
            else:
                steps, faults, = self.lru_replacement(frames, pages)
            
            # Display results
            for step in steps:
                memory_str = ','.join(map(str, step['memory']))
                self.table.insert('', 'end', values=(
                    step['step'],
                    step['page'],
                    memory_str,
                    step['status']
                ))
            
            # Update stats
            total_pages = len(pages)
            hit_rate = ((total_pages - faults) / total_pages) * 100
            stats_text = f"Total Pages: {total_pages}\n"
            stats_text += f"Page Faults: {faults}\n"
            stats_text += f"Hit Rate: {hit_rate:.1f}%"
            self.stats_label.config(text=stats_text)
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = MemoryMatrixApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
