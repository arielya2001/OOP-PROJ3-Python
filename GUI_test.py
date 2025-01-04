import tkinter as tk

root = tk.Tk()
root.title("Porject-OOP")

def on_click():
    #print("you clicked the button!")
    lbl.config(text = "Button clicked")


lbl = tk.Label(root, text = "Label1")
lbl.grid(row = 0, column = 0)

btn = tk.Button(root, text = "Button", command = on_click)
btn.grid(row = 0, column = 1)

root.mainloop()

def log_arguments_and_return(func):
    def wrapper(args, **kwargs):
        print(f"Function '{func.name}' was called with arguments: {args}, {kwargs}")
        result = func(args, **kwargs)
        print(f"Function '{func.name}' returned: {result}")
        return result

    return wrapper