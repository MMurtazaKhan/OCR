# def ocr(self):
#         source_folder = filedialog.askdirectory(title="Select a folder with files to OCR")
#         if source_folder:
#             ocr_folder = os.path.join(source_folder, "OCRed")
#             os.makedirs(ocr_folder, exist_ok=True)

#             # Get a list of all eligible files
#             eligible_files = [os.path.join(root_dir, file) for root_dir, _, files in os.walk(source_folder) for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf'))]

#             # Display the list of files in the text box
#             self.display_text("List of files to OCR:")
#             for file_path in eligible_files:
#                 self.display_text(file_path)

#             # Configure the progress bar
#             self.progress_bar.configure(mode='determinate')
#             self.progress_bar['maximum'] = len(eligible_files)
#             self.progress_bar['value'] = 0
#             self.root.update_idletasks()

#             # Process each eligible file
#             for index, file_path in enumerate(eligible_files, start=1):
#                 try:
#                     extracted_text = self.perform_ocr_with_opencv(file_path)
#                     ocr_result_path = os.path.join(ocr_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_OCR.txt")
#                     with open(ocr_result_path, "w") as ocr_file:
#                         ocr_file.write(extracted_text)
#                     self.display_text(f"OCR completed for {file_path}")

#                 except Exception as e:
#                     error_file_path = os.path.join(ocr_folder, f"error_{os.path.basename(file_path)}.txt")
#                     with open(error_file_path, "w") as error_file:
#                         error_file.write(str(e))
#                     self.display_text(f"OCR Error for {file_path}: {e}")

#                 # Update the progress bar
#                 self.progress_bar['value'] = index
#                 self.root.update_idletasks()

#             # Reset the progress bar
#             self.progress_bar['value'] = 0
#             self.progress_bar.configure(mode='indeterminate')

import pytesseract
import cv2
def perform_ocr_with_opencv(image_path):
    try:
        # Specify the path to the Tesseract executable here
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        
        image = cv2.imread(image_path)
        extracted_text = pytesseract.image_to_string(image)
        print(extracted_text)
    except Exception as e:
        raise e
    
perform_ocr_with_opencv('C:\\Users\\Haier\\Desktop\\pics\\testocr.png')