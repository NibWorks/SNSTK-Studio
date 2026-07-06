
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk

from paths import APP_ICON, NIB_HAPPY

loaded_image_path = None
preview_photo = None


def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def has_transparency(image):
    return image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    )


def prepare_preview_image(image):
    if has_transparency(image):
        image = image.convert("RGBA")
        background = Image.new("RGBA", image.size, "WHITE")
        background.alpha_composite(image)
        image = background.convert("RGB")
    else:
        image = image.convert("RGB")

    image.thumbnail((540, 260), Image.Resampling.LANCZOS)
    return image


def load_image(preview_canvas, info_label):
    global loaded_image_path, preview_photo

    file_path = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
        ],
    )

    if not file_path:
        return

    loaded_image_path = Path(file_path)
    image = Image.open(file_path)
    original_width, original_height = image.size

    preview_image = prepare_preview_image(image)
    preview_photo = ImageTk.PhotoImage(preview_image)

    preview_canvas.delete("all")
    preview_canvas.create_image(
        280,
        140,
        image=preview_photo,
        anchor="center"
    )

    file_size = format_file_size(loaded_image_path.stat().st_size)
    transparency = "Yes" if has_transparency(image) else "No"

    info_label.config(
        text=(
            f"Image Information\n"
            f"Filename: {loaded_image_path.name}\n"
            f"Dimensions: {original_width} × {original_height} px\n"
            f"Transparency: {transparency}\n"
            f"File Size: {file_size}"
        )
    )
def create_snstk(window, output_path):
    if not hasattr(window, "selected_image_path"):
        messagebox.showwarning("No Image Selected", "Please choose an image first.")
        return

    selected_size = window.selected_size.get()
    output_folder = output_path.get()

    print("Creating SNSTK...")
    print("Image:", window.selected_image_path)
    print("Size:", selected_size)
    print("Output folder:", output_folder)

    messagebox.showinfo(
        "Create .SNSTK",
        f"Ready to create sticker!\n\nSize: {selected_size} px\nOutput folder: {output_folder}"
    )
    create_button = tk.Button(
        window,
        text="Create .SNSTK",
        width=20,
        height=2,
        command=lambda: create_snstk(window, output_path)
    )
def show_create_stickers_page(window):
    for widget in window.winfo_children():
        if str(widget) != ".menu_bar":
            widget.destroy()

    title = tk.Label(window, text="Create Stickers", font=("Segoe UI", 24, "bold"))
    title.pack(pady=20)

    instructions = tk.Label(
        window,
        text="Choose a PNG or JPG image to preview.",
        font=("Segoe UI", 12)
    )
    instructions.pack(pady=5)

    preview_canvas = tk.Canvas(
        window,
        width=560,
        height=280,
        bg="white",
        highlightthickness=1,
        highlightbackground="black"
    )
    preview_canvas.pack(pady=15)
    preview_canvas.create_text(
        280,
        140,
        text="Image Preview Area",
        font=("Segoe UI", 12)
    )

    info_label = tk.Label(
        window,
        text="Image Information\nNo image selected.",
        font=("Segoe UI", 10),
        justify="left"
    )
    info_label.pack(pady=5)

    browse_button = tk.Button(
        window,
        text="Browse for Image...",
        width=22,
        command=lambda: load_image(preview_canvas, info_label)
    )
    browse_button.pack(pady=10)
    # Output Folder
    output_label = tk.Label(
        window,
        text="Output Folder",
        font=("Segoe UI", 10, "bold")
    )
    output_label.pack(pady=(10, 2))

    output_path = tk.StringVar(value="output")

    # Frame to hold the output path and Browse button
    output_frame = tk.Frame(window)
    output_frame.pack(pady=(0, 10))

    output_entry = tk.Entry(
        output_frame,
        textvariable=output_path,
        width=45
    )
    output_entry.pack(side="left", padx=(0, 5))

    browse_output_button = tk.Button(
        output_frame,
        text="Browse...",
        width=10
    )
    browse_output_button.pack(side="left")
    size_label = tk.Label(window, text="Output Size", font=("Segoe UI", 12, "bold"))
    size_label.pack(pady=(15, 5))

    window.selected_size = tk.StringVar(value="260")

    size_frame = tk.Frame(window)
    size_frame.pack()

    for size in ["180", "260", "300", "400", "500"]:
        tk.Radiobutton(
            size_frame,
            text=f"{size} px",
            variable=window.selected_size,
            value=size,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=8)

    create_button = tk.Button(
    window,
    text="Create .SNSTK",
    width=20,
    height=2,
    command=lambda: create_snstk(window, output_path)
)
    create_button.pack(pady=18)

    back_button = tk.Button(window, text="Back", command=lambda: show_home_page(window))
    back_button.pack()

    version = tk.Label(window, text="Version 0.6.0", font=("Segoe UI", 10))
    version.pack(side="bottom", pady=8)


def show_home_page(window):
    global preview_photo

    for widget in window.winfo_children():
        if str(widget) != ".menu_bar":
            widget.destroy()

    title = tk.Label(window, text="SNSTK Studio", font=("Segoe UI", 26, "bold"))
    title.pack(pady=(24, 8))

    if NIB_HAPPY.exists():
        nib_image = Image.open(NIB_HAPPY).convert("RGBA")
        nib_image.thumbnail((170, 170), Image.Resampling.LANCZOS)
        preview_photo = ImageTk.PhotoImage(nib_image)

        nib_label = tk.Label(window, image=preview_photo)
        nib_label.pack(pady=(2, 10))

    subtitle = tk.Label(
        window,
        text="Create native Supernote sticker collections",
        font=("Segoe UI", 12)
    )
    subtitle.pack(pady=(8, 0))

    create_button = tk.Button(
        window,
        text="Create Stickers",
        width=22,
        height=2,
        command=lambda: show_create_stickers_page(window)
    )
    create_button.pack(pady=(30, 40))

    version = tk.Label(window, text="Version 0.6.0", font=("Segoe UI", 10))
    version.pack(side="bottom", pady=5)

    footer = tk.Label(
        window,
        text="Built by NibWorks for the Supernote community.",
        font=("Segoe UI", 10)
    )
    footer.pack(side="bottom", pady=(0, 35))




def main():
    window = tk.Tk()
  

    window.title("SNSTK Studio")

    if APP_ICON.exists():
        window.iconbitmap(APP_ICON)

    window.geometry("900x720")
    window.resizable(False, False)
    create_menu_bar(window)
    show_home_page(window)

    window.mainloop()
def show_about_window(window):
    about = tk.Toplevel(window)
    about.title("About SNSTK Studio")
    about.geometry("420x420")
    about.resizable(False, False)

    if APP_ICON.exists():
        about.iconbitmap(APP_ICON)

    title = tk.Label(
        about,
        text="SNSTK Studio",
        font=("Segoe UI", 20, "bold")
    )
    title.pack(pady=(25, 10))

    if NIB_HAPPY.exists():
        nib_image = Image.open(NIB_HAPPY).convert("RGBA")
        nib_image.thumbnail((110, 110), Image.Resampling.LANCZOS)
        about.nib_photo = ImageTk.PhotoImage(nib_image)

        nib_label = tk.Label(about, image=about.nib_photo)
        nib_label.pack(pady=5)

    description = tk.Label(
        about,
        text="Create native Supernote sticker collections.",
        font=("Segoe UI", 10),
        wraplength=340,
        justify="center"
    )
    description.pack(pady=(10, 8))

    version = tk.Label(
        about,
        text="Version 0.6.0",
        font=("Segoe UI", 10)
    )
    version.pack(pady=4)

    creator = tk.Label(
        about,
        text="Built by NibWorks for the Supernote community.",
        font=("Segoe UI", 9),
        wraplength=340,
        justify="center"
    )
    creator.pack(pady=(8, 18))

    close_button = tk.Button(
        about,
        text="Close",
        width=14,
        command=about.destroy
    )
    close_button.pack()

def create_menu_bar(window):
    menu_frame = tk.Frame(window, bg="#f2f2f2", height=32, name="menu_bar")
    menu_frame.pack(fill="x")

    file_button = tk.Menubutton(
        menu_frame,
        text="File",
        bg="#f2f2f2",
        relief="flat",
        font=("Segoe UI", 10)
    )
    file_button.pack(side="left", padx=(10, 5), pady=4)

    file_menu = tk.Menu(file_button, tearoff=0)
    file_menu.add_command(label="Exit", command=window.destroy)
    file_button.config(menu=file_menu)

    help_button = tk.Menubutton(
        menu_frame,
        text="Help",
        bg="#f2f2f2",
        relief="flat",
        font=("Segoe UI", 10)
    )
    help_button.pack(side="left", padx=5, pady=4)

    help_menu = tk.Menu(help_button, tearoff=0)
    help_menu.add_command(
    label="About SNSTK Studio",
    command=lambda: show_about_window(window)
)
    help_button.config(menu=help_menu)
    


if __name__ == "__main__":
    main()