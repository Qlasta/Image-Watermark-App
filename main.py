import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont

BACKGROUND_C = "#B3E8E5"
TITLE_C = "#3BACB6"
TEXT_C = "#2F8F9D"
TITLE_F = ("Terminal", 24, "normal")
TEXT_F = ("Helvetica", 14, "normal")
TEXT_F_s = ("Helvetica", 10, "normal")


# functions


def file_open():
    """Opens directory dialog to select an image. Shows path of selected image."""
    global selected_image
    selected_image = filedialog.askopenfilename()
    # show file path
    label_f_uploaded["text"] = "Selected file:"
    label_file_path["text"] = selected_image
    label_f_uploaded.grid(row=7, column=0)
    label_file_path.grid(row=7, column=2)


def execute():
    """Puts customized text on an image. Shows the result for a user and creates shows inputs to save an image."""
    global result_image
    global entry_save

    # get text settings
    watermark = entry_w_text.get()
    if watermark == "":
        messagebox.showinfo("Missing info", "Please enter a text.")
        return
    alpha = radio_state.get()
    if alpha == 0:
        messagebox.showinfo("Missing info", "Please select text type: Half-Transparent or Opaque.")
        return
    col = radio_state_c.get()
    if col == 0:
        messagebox.showinfo("Missing info", "Please select text color: Black or Red.")
        return

    # check image
    try:
        type(selected_image)
    except:
        messagebox.showinfo("Missing info", "Please select an image.")
        return

    # put text on image
    with Image.open(selected_image).convert("RGBA") as image_to_mark:
        transp_layer = Image.new("RGBA", image_to_mark.size, (255, 255, 255, 0))
        w_font = ImageFont.truetype("Raleway-Bold.ttf", int(image_to_mark.size[1]*0.05))
        draw_image = ImageDraw.Draw(transp_layer)
        draw_image.text((image_to_mark.size[0] - (image_to_mark.size[0])*0.5-len(watermark)*12,
                         image_to_mark.size[1] - (int(image_to_mark.size[1]*0.05)+5)), watermark,
                        font=w_font, fill=(col, 0, 0, alpha))
        result_image = Image.alpha_composite(image_to_mark, transp_layer)
        result_image.show()

    # inputs to save image
    label_save = tk.Label(text="Save image as:", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C)
    label_save.grid(row=9, column=0)
    entry_save = tk.Entry(width=30)
    entry_save.grid(row=9, column=2)
    button_save = tk.Button(text="Save image", font=TEXT_F, fg=TEXT_C, width=30, command=save, activeforeground=TEXT_C)
    button_save.grid(row=10, column=0, columnspan=3)


def save():
    """Opens directory dialog and saves image to it by entered name. Shows success message."""
    new_file_name = entry_save.get()
    if new_file_name == "":
        messagebox.showinfo("Missing info", "Please enter a new file name.")
        return
    save_directory = filedialog.askdirectory()
    entry_w_text.delete(0, tk.END)
    entry_save.delete(0,tk.END)
    label_file_path["text"] = ""
    result_image.save(f"{save_directory}/{new_file_name}.png", "png")
    label_file_saved = tk.Label(text=f"Your image is saved to {save_directory}", font=TEXT_F_s, fg=TEXT_C, bg=BACKGROUND_C)
    label_file_saved.grid(row=11, column=0, columnspan=3)


# title and background
window = tk.Tk()
window.title("Watermark application")
window.minsize(width=500, height=300)
window.config(padx=50, pady=50, bg=BACKGROUND_C)
title_label = tk.Label(text="Watermark your image", fg=TITLE_C, pady=20, bg=BACKGROUND_C)
title_label["font"]=TITLE_F
title_label.grid(row=0, column=0, columnspan=3)
canvas = tk.Canvas(width=80, height=120)
img = tk.PhotoImage(file="watermark.png")
cover_img = img.subsample(4, 4)
canvas.config(bg=BACKGROUND_C, highlightthickness=0)
canvas.create_image(40,64, image=cover_img)
canvas.grid(row=1, column=1)

# enter image text
label_w_text = tk.Label(text="Enter text you want to put:", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C)
label_w_text.grid(row=2, column=0)
label_w_text.focus()
entry_w_text = tk.Entry(width=30)
entry_w_text.grid(row=2, column=2)

# radio buttons to customize text
radio_state = tk.IntVar()
radio_state_c = tk.IntVar()
radio_transparent = tk.Radiobutton(text="Half-Transparent", value=128, variable=radio_state,  font=TEXT_F_s, fg=TEXT_C,
                                   activebackground=BACKGROUND_C, justify="left", bg=BACKGROUND_C)
radio_transparent.grid(row=3, column=1)
radio_opaque = tk.Radiobutton(text="Opaque", value=255, variable=radio_state,  font=TEXT_F_s, fg=TEXT_C,
                              activebackground=BACKGROUND_C, justify="left", bg=BACKGROUND_C)
radio_opaque.grid(row=3, column=2)
radio_black = tk.Radiobutton(text="Black", value=1, variable=radio_state_c, font=TEXT_F_s, fg=TEXT_C,
                             activebackground=BACKGROUND_C, anchor="nw", justify="left", bg=BACKGROUND_C)
radio_black.grid(row=4, column=1)
radio_red = tk.Radiobutton(text="Red", value=255, variable=radio_state_c,  font=TEXT_F_s, fg=TEXT_C,
                           activebackground=BACKGROUND_C, justify="left", bg=BACKGROUND_C)
radio_red.grid(row=4, column=2)

# select image
label_w_upload = tk.Label(text="Select your image:", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C, anchor="nw", justify="left")
label_w_upload.grid(row=6, column=0)

button_w_upload = tk.Button(text="Open image", font=TEXT_F, fg=TEXT_C, width=15, command=file_open, activeforeground=TEXT_C, height=1)
button_w_upload.grid(row=6, column=2)

# path of selected image
label_f_uploaded = tk.Label(text="", font=TEXT_F, fg=TEXT_C, bg=BACKGROUND_C)
label_file_path = tk.Label(text="", bg=BACKGROUND_C)

# view result
execute_button = tk.Button(text="View result", font=TEXT_F, fg=TEXT_C, width=30, command=execute,
                           activeforeground=TEXT_C)
execute_button.grid(row=8, column=0, columnspan=3)


window.mainloop()

