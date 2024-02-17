import customtkinter as ctk
import json
import os

class ToDoApp(ctk.CTk):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("To Do App")
        self.geometry("400x400")
        self.tasks = []
        self.completed_tasks = []

        self.task_entry = ctk.CTkEntry(self, placeholder_text ="Enter task")
        self.task_entry.pack(fill="x", padx=10, pady=10)
        
        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task)
        self.add_button.pack(fill="x", padx=10, pady=10)
        self.bind("<Return>", lambda e: self.add_task())
        
        self.task_frame = ctk.CTkFrame(self)
        self.task_frame.pack(fill="both", expand=True)
        
        self.completed_task_frame = ctk.CTkFrame(self)
        self.completed_task_frame.pack(fill="both", expand=True)
        
        self.load_tasks()
        self.show_tasks()
        
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                data = json.load(file)
                self.tasks = data["tasks"]
                self.completed_tasks = data["completed_tasks"]
        else:
            with open("tasks.json", "w") as file:
                json.dump({"tasks": [], "completed_tasks": []}, file)
    
    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump({"tasks": self.tasks, "completed_tasks": self.completed_tasks}, file)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.save_tasks()
            self.show_tasks()
            self.task_entry.delete(0, "end")
            
    def show_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        for widget in self.completed_task_frame.winfo_children():
            widget.destroy()
        for task in self.tasks:
            task_frame = ctk.CTkFrame(self.task_frame)
            task_frame.pack(fill="x", padx=10, pady=5)
            task_label = ctk.CTkLabel(task_frame, text=task) 
            task_label.pack(side="left")
            done_button = ctk.CTkButton(task_frame, text="Done", command=lambda t=task: self.mark_as_done(t))
            done_button.pack(side="right")            
            task_label.bind("<Configure>", lambda e: self.update_window_size())

        for task in self.completed_tasks:
            task_frame = ctk.CTkFrame(self.completed_task_frame)
            task_frame.pack(fill="x", padx=10, pady=5)
            task_label = ctk.CTkLabel(task_frame, text=task)
            task_label.pack(side="left")
            done_button = ctk.CTkButton(task_frame, text="Delete", command=lambda t=task: self.delete_task(t))
            done_button.pack(side="right")

    def update_window_size(self):
        self.update_idletasks()
        max_height = self.winfo_screenheight() * 2 / 3
        max_width = self.winfo_screenwidth() / 2
        task_frame_height = self.task_frame.winfo_height()
        completed_task_frame_height = self.completed_task_frame.winfo_height()
        total_height = task_frame_height + completed_task_frame_height
        new_height = min(total_height, max_height)
        self.geometry(f"{min(self.winfo_width(), max_width)}x{new_height}")

    def mark_as_done(self, task):
        self.tasks.remove(task)
        self.completed_tasks.append(task)
        self.save_tasks()
        self.show_tasks()
        
    def delete_task(self, task):
        self.completed_tasks.remove(task)
        self.save_tasks()
        self.show_tasks()
        
if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()