import os
import shutil
from PIL import Image, ImageTk
from rembg import remove
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog

# Paths
file = Path(__file__).parent
assets = file / "assets"

def relative_to_assets(path: str) -> Path:
    return assets / path

# Variáveis Globais | Global Variables
image_path = None
imageBG_path = None

# Display das Funções | Display Functions
def display_image(image_path, x, y):
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize((350, 350), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(pil_image)
    canvas.create_image(x, y, anchor="nw", image=tk_image)
    canvas.tk_image_ref = tk_image

# Chamada das Funções | Callback Functions
def upload_image():
    global image_path
    image_path = filedialog.askopenfilename()
    display_image(image_path, 79, 120)

def remove_background():
    global image_path, imageBG_path
    if image_path:
        input_image = Image.open(image_path)
        output_image = remove(input_image)
        imageBG_path = "newimage.png"
        output_image.save(imageBG_path)
        display_image(imageBG_path, 471, 120)

def download_background_removed_image():
    global imageBG_path
    if imageBG_path:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            shutil.copyfile(imageBG_path, save_path)
            os.remove(imageBG_path)  # Exclui o arquivo temporário | Remove temporary file after saving

def clear_canvas():
    items = canvas.find_all()
    for item in items:
        if canvas.type(item) == "image":
            if item not in (upload_button, remove_button, download_button, cancel_button):
                canvas.delete(item)

def cancel_image():
    global image_path, imageBG_path
    if imageBG_path and os.path.exists(imageBG_path):
        os.remove(imageBG_path)
    image_path = None
    imageBG_path = None
    clear_canvas()

# Setup GUI
window = Tk()
window.title("BGRemover")
photo = PhotoImage(file=relative_to_assets("icon.png"))
window.wm_iconphoto(False, photo)
window.geometry("900x607")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=607,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Elementos da GUI | GUI Elements
canvas.create_rectangle(0, 73, 900, 607, fill="#161617", outline="")
canvas.create_rectangle(0, 0, 900, 73, fill="#1E1E1F", outline="")
canvas.create_text(325, 28, anchor="nw", text="Python Background Remover", fill="#FFFFFF", font=("AnonymousPro Bold", 16))

# Botões | Buttons
cancel_button = PhotoImage(file=relative_to_assets("cancelar.png"))
cancel = Button(image=cancel_button, borderwidth=0, highlightthickness=0, command=cancel_image, relief="flat")
cancel.place(x=770, y=14, width=90, height=45)

upload_button = PhotoImage(file=relative_to_assets("upload.png"))
upload = Button(image=upload_button, borderwidth=0, highlightthickness=0, command=upload_image, relief="flat")
upload.place(x=79, y=532, width=65, height=55)

remove_button = PhotoImage(file=relative_to_assets("remover.png"))
remover = Button(image=remove_button, borderwidth=0, highlightthickness=0, command=remove_background, relief="flat")
remover.place(x=370, y=532, width=160, height=55)

download_button = PhotoImage(file=relative_to_assets("download.png"))
download = Button(image=download_button, borderwidth=0, highlightthickness=0, command=download_background_removed_image, relief="flat")
download.place(x=756, y=532, width=65, height=55)

# Canvas Image Placeholders
canvas.create_rectangle(79, 120, 429, 470, fill="#1E1E1F", outline="")
canvas.create_rectangle(471, 120, 821, 470, fill="#1E1E1F", outline="")

window.resizable(False, False)
window.mainloop()