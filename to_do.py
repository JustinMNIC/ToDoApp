import customtkinter as ctk
import json
import datetime

class mainframe(ctk.CTk):
    json_file = "./tasks.json"

    def __init__(self):
        super().__init__()

        self.title("What you'll do (today - hopefully) ;)")
        self.geometry("800x400")

        self.grid_columnconfigure(tuple(range(7)), weight=1)
        self.grid_rowconfigure(tuple(range(15)), weight=1, uniform="yes")

        var_message = ctk.StringVar(self, value="Work hard, Party harder!", name="var_message")
        self.message = ctk.CTkLabel(self, text=var_message.get(), text_color="red", font=("Arial", 21, "bold"))
        self.message.grid(row=1, column=0, columnspan=7, sticky="news")

        self.add_new_task = ctk.CTkEntry(self, placeholder_text="type something..")
        self.add_new_task.grid(row=3, column=0, columnspan=2, sticky="news")

        self.button_add_new_task = ctk.CTkButton(self, text="ADD task", command=self.new_task)
        self.button_add_new_task.grid(row=3, column=2)
        self.bind("<Return>", lambda event: self.new_task())

        self.button_advanced = ctk.CTkButton(self, text="Advanced options", command=self.advanced_options)
        self.button_advanced.grid(row=3, column=3)

        self.button_show_completed_tasks = ctk.CTkButton(self, text="Completed tasks", command=self.show_completed_tasks)
        self.button_show_completed_tasks.grid(row=3, column=4)

        self.button_show_settings = ctk.CTkButton(self, text="Settings", command=self.show_settings)
        self.button_show_settings.grid(row=3, column=5)

        self.checkbox_frame = ctk.CTkFrame(self)
        self.checkbox_frame.grid(row=4, rowspan=11, column=0, columnspan=4, sticky="news")

        self.frame_accomplishments = ctk.CTkFrame(self)
        self.frame_accomplishments.grid(row=4, rowspan=11, column=4, columnspan=3, sticky="news")

        self.load_json_data()
        self.show_tasks()
        self.show_accomplishments()

    def show_settings(self):
        pass

    def advanced_options(self):
        pass

    def show_completed_tasks(self):
        for child in self.checkbox_frame.winfo_children():
            child.destroy()

        self.load_json_data()
        if self.button_show_completed_tasks.cget("text") == "Completed tasks":
            # Show completed tasks
            completed_tasks = [(key, val) for key, val in data.items() if val["completed"]]
            completed_tasks = completed_tasks[-11:]  # Show the last 11 completed tasks
            for key, val in completed_tasks:
                var_checkbox = ctk.IntVar(value=val["completed"])
                checkbox_task = ctk.CTkCheckBox(self.checkbox_frame, text=val["task"], variable=var_checkbox)
                checkbox_task.bind("<Button-1>", lambda event, key=key, var_checkbox=var_checkbox, show_completed=True: self.toggle_task(key, var_checkbox.get(), show_completed))
                checkbox_task.pack()
            # Change button text and command
            self.button_show_completed_tasks.configure(text="Your tasks", command=self.show_uncompleted_tasks)
        else:
            # Show uncompleted tasks
            self.show_uncompleted_tasks()

    def show_uncompleted_tasks(self):
        for child in self.checkbox_frame.winfo_children():
            child.destroy()
        self.load_json_data()
        uncompleted_tasks = [(key, val) for key, val in data.items() if not val["completed"]]
        uncompleted_tasks = uncompleted_tasks[:12]  # Show up to 12 uncompleted tasks
        for key, val in uncompleted_tasks:
            var_checkbox = ctk.IntVar(value=val["completed"])
            checkbox_task = ctk.CTkCheckBox(self.checkbox_frame, text=val["task"], variable=var_checkbox)
            checkbox_task.bind("<Button-1>", lambda event, key=key, var_checkbox=var_checkbox, show_completed=False: self.toggle_task(key, var_checkbox.get(), show_completed))
            checkbox_task.pack()
        # Change button text and command
        self.button_show_completed_tasks.configure(text="Completed tasks", command=self.show_completed_tasks)

    def new_task(self):
        text = self.add_new_task.get()
        if text != "":
            new_task = {
                f"task_id_{len(data.keys()) + 1}": {
                    "task": text,
                    "completed": False,
                    "Time: created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Time: finished": "n/a",
                    "Time_limit": "n/a",
                    "send notifications": 0
                }
            }
            data.update(new_task)
            with open(self.json_file, "w") as file:
                json.dump(data, file, indent=2)
        self.add_new_task.delete(0, 'end')
        self.show_tasks()
        self.show_accomplishments()

    def load_json_data(self):
        global data
        try:
            with open(self.json_file, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}
            with open(self.json_file, "w") as file:
                json.dump(data, file, indent=2)

    def show_tasks(self, *args):
        for child in self.checkbox_frame.winfo_children():
            child.destroy()
        self.load_json_data()
        for key, val in data.items():
            if not val["completed"]:
                var_checkbox = ctk.IntVar(value=val["completed"])
                checkbox_task = ctk.CTkCheckBox(self.checkbox_frame, text=val["task"], variable=var_checkbox)
                checkbox_task.bind("<Button-1>", lambda event, key=key, var_checkbox=var_checkbox, show_completed=False: self.toggle_task(key, var_checkbox.get(), show_completed))
                checkbox_task.pack()

    def toggle_task(self, index, state, show_completed):
        data[index]["completed"] = state
        if state:
            data[index]["Time: finished"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=2)
        self.load_json_data()
        if show_completed:
            self.show_completed_tasks()
        else:
            self.show_tasks()
        self.show_accomplishments()

    def show_accomplishments(self):
        # Remove existing labels in frame_accomplishments
        for child in self.frame_accomplishments.winfo_children():
            child.destroy()

        today = datetime.datetime.now().date()
        yesterday = today - datetime.timedelta(days=1)
        week_start = today - datetime.timedelta(days=today.weekday())
        month_start = today.replace(day=1)

        unfinished_tasks = sum(1 for task in data.values() if not task["completed"])
        today_completed_tasks = sum(1 for task in data.values() if task["completed"] and datetime.datetime.strptime(task["Time: finished"], "%Y-%m-%d %H:%M:%S").date() == today)
        yesterday_completed_tasks = sum(1 for task in data.values() if task["completed"] and datetime.datetime.strptime(task["Time: finished"], "%Y-%m-%d %H:%M:%S").date() == yesterday)
        week_completed_tasks = sum(1 for task in data.values() if task["completed"] and datetime.datetime.strptime(task["Time: finished"], "%Y-%m-%d %H:%M:%S").date() >= week_start)
        month_completed_tasks = sum(1 for task in data.values() if task["completed"] and datetime.datetime.strptime(task["Time: finished"], "%Y-%m-%d %H:%M:%S").date() >= month_start)

        report_text = f"Unfinished tasks: {unfinished_tasks}\n" \
                      f"Tasks finished today: {today_completed_tasks}\n" \
                      f"Tasks finished yesterday: {yesterday_completed_tasks}\n" \
                      f"Tasks finished this week: {week_completed_tasks}\n" \
                      f"Tasks finished in the past 30 days: {month_completed_tasks}"

        report_label = ctk.CTkLabel(self.frame_accomplishments, text=report_text)
        report_label.pack()

if __name__ == "__main__":
    program = mainframe()
    program.mainloop()
