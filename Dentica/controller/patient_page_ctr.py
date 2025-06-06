from PyQt6 import QtCore, QtGui, QtWidgets
from ui.Patients_Page import PatientPage
from backend.patient_page_comp import get_all_patient_records
from controller.patient_ctr import Patient_Dialog_Ctr
from PyQt6.QtWidgets import QDialog, QMessageBox
from backend.patients_comp import get_patient_data
from PyQt6.QtCore import pyqtSignal
import os

class Patient_Page_Ctr(PatientPage):
    reload_patient_signal = pyqtSignal()
    
    def __init__(self, stacked_widget, patient_id):
        super().__init__(stacked_widget)
        self.Pages = stacked_widget
        
        self.Editpat_btn.setProperty("Patient ID", patient_id)
        self.Editpat_btn.clicked.connect(self.edit_patient)
        
        # Load patient information when the page is initialized
        self.load_patient_infos(patient_id)

    def load_patient_infos(self, patient_id):
        data = get_all_patient_records(patient_id)
        patient_info = data.get("info", None)
        if patient_info:
            patient_id, full_name, gender, birth_date, contact_number, email, address = patient_info
            
            # Split the full name into parts
            name_parts = full_name.split()
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            middle_name = name_parts[1] if len(name_parts) > 2 else ""
            last_name = name_parts[-1] if len(name_parts) > 0 else ""
            
            # Convert birth_date to string
            birth_date_str = str(birth_date) if birth_date else ""
            
            # Set the values 
            self.pat_id.setText(str(patient_id))
            self.pat_name.setText(full_name or "Unknown")
            self.fnval.setText(first_name)
            self.mnval.setText(middle_name)
            self.lndval.setText(last_name)
            self.genval.setText(gender or "")
            self.bdval.setText(birth_date_str)
            self.condval.setText(contact_number or "")
            self.emailval.setText(email or "")
            self.adval.setText(address or "")
            
            # Load and display the patient's picture if it exists
            self.load_patient_picture(patient_id)
        else:
            # Clear or set empty in case no data found
            self.pat_id.setText("N/A")
            self.pat_name.setText("Unknown")
            self.fnval.setText("")
            self.mnval.setText("")
            self.lndval.setText("")
            self.genval.setText("")
            self.bdval.setText("")
            self.condval.setText("")
            self.emailval.setText("")
            self.adval.setText("")
            
    def load_patient_picture(self, patient_id):
        """Load the patient's picture from the directory if it exists."""
        picture_path = os.path.join("Dentica/patient_pic", f"{patient_id}.jpg")
        if os.path.exists(picture_path):
            pixmap = QtGui.QPixmap(picture_path).scaled(
                150, 150,
                QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            mask = QtGui.QBitmap(150, 150)
            mask.fill(QtCore.Qt.GlobalColor.color0)
            p = QtGui.QPainter(mask)
            p.setBrush(QtCore.Qt.GlobalColor.color1)
            p.setPen(QtCore.Qt.PenStyle.NoPen)
            p.drawEllipse(0, 0, 150, 150)
            p.end()

            pixmap.setMask(mask)
            self.pic_frame.setPixmap(pixmap) 
        else:
            self.pic_frame.clear()  # Clear the picture if not found

    def edit_patient(self):
        button = self.sender()
        patient_id = button.property("Patient ID")
        patient_data = get_patient_data(patient_id)
        if not patient_data:
            QMessageBox.warning(self, "Error", "Could not load patient data")
            return
        
        patient_popup = Patient_Dialog_Ctr(patient_data=patient_data)
        if patient_popup.exec():
            # After the dialog closes and if accepted, reload the updated data
            self.load_patient_infos(patient_id)
            self.reload_patient_signal.emit()
