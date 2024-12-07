import PyInstaller.__main__

PyInstaller.__main__.run([
    'chess.py',
    '--windowed',           # No console window
    '--noconsole',          # No console window for GUI apps
    '--icon=icon.icns',    # Replace with your .icns icon path
    '--add-data=images:images',  # Include the images folder (adjust path if necessary)
])
