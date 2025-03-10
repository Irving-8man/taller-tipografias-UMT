import os
from fontTools.ttLib import TTFont
from datetime import datetime

INPUT_DIR = "../fonts_ttf"
OUTPUT_DIR = "fonts_web"
LOG_FILE = "conversion_log.txt"

def convert_font(ttf_path, output_dir):
    font_name = os.path.basename(ttf_path).replace(".ttf", "")
    log_msg = ""
    success = True
    try:
        font = TTFont(ttf_path)
        is_variable = "fvar" in font
        # Convertir a WOFF
        woff_path = os.path.join(output_dir, f"{font_name}.woff")
        font.flavor = "woff"
        font.save(woff_path)
        # Convertir a WOFF2 (requiere brotli)
        woff2_path = os.path.join(output_dir, f"{font_name}.woff2")
        font.flavor = "woff2"
        font.save(woff2_path)
        log_msg = f"Creado: {font_name} (Variable: {is_variable}) -> .woff/.woff2"
    except Exception as e:
        success = False
        log_msg = f"ERROR: {font_name} -> {str(e)}"
    finally:
        font.close()
    return log_msg, success

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(LOG_FILE, "w") as log:
        log.write(f"Conversión iniciada: {datetime.now()}\n\n")
        # Procesar todos los archivos .ttf
        for filename in os.listdir(INPUT_DIR):
            if filename.endswith(".ttf"):
                ttf_path = os.path.join(INPUT_DIR, filename)
                log_msg, success = convert_font(ttf_path, OUTPUT_DIR)
                log.write(log_msg + "\n")
    print(f"Proceso completo. Revisa {LOG_FILE} para detalles.")

if __name__ == "__main__":
    main()