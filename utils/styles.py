PRIMARY_COLOR = "#004aad"
SECONDARY_COLOR = "#a3c9f1"
FONT_FAMILY = "Helvetica"
TITLE_FONT = (FONT_FAMILY, 30, "bold")
SUBTITLE_FONT = (FONT_FAMILY, 24, "bold")

def centerWindow(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = (screenWidth // 2) - (width // 2)
    y = (screenHeight // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")