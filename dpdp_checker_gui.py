# DPDP Compliance Checker - Tkinter Version with Timestamped Excel & PDF

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import os

# Questionnaire
questions = [
    "Is explicit consent taken before collecting personal data?",
    "Is the purpose of data collection clearly explained to users?",
    "Can users withdraw their consent?",
    "Is personal data used only for the stated purpose?",
    "Is unnecessary personal data avoided?",
    "Can users request access to their personal data?",
    "Can users request correction of incorrect data?",
    "Can users request deletion of their data?",
    "Is there a defined data retention policy?",
    "Is personal data deleted after the retention period?",
    "Is access to personal data restricted to authorized users?",
    "Is personal data protected using security measures?",
    "Is there a process to handle data breaches?",
    "Is a contact person or grievance officer available?"
]

# Main Application Class
class DPDPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DPDP Compliance Checker")
        self.root.geometry("750x550")
        self.user_details = {}
        self.current_q = 0
        self.total_score = 0
        self.total_possible = len(questions)
        self.question_scores = {}
        self.create_welcome_page()

    # Welcome Page
    def create_welcome_page(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome to DPDP Compliance Checker", font=("Helvetica", 18, "bold")).pack(pady=20)

        tk.Label(self.root, text="Company / Institution Name:", font=("Helvetica", 12)).pack(pady=5)
        self.entry_institution = tk.Entry(self.root, width=50)
        self.entry_institution.pack(pady=5)

        tk.Label(self.root, text="User Name:", font=("Helvetica", 12)).pack(pady=5)
        self.entry_name = tk.Entry(self.root, width=50)
        self.entry_name.pack(pady=5)

        tk.Label(self.root, text="Email:", font=("Helvetica", 12)).pack(pady=5)
        self.entry_email = tk.Entry(self.root, width=50)
        self.entry_email.pack(pady=5)

        tk.Button(self.root, text="Start Questionnaire", font=("Helvetica", 12, "bold"), bg="green", fg="white",
                  command=self.start_questionnaire).pack(pady=20)

    # Clear all widgets
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Start Questionnaire
    def start_questionnaire(self):
        institution = self.entry_institution.get().strip()
        name = self.entry_name.get().strip()
        email = self.entry_email.get().strip()
        if not institution or not name or not email:
            messagebox.showerror("Error", "Please fill all fields")
            return
        self.user_details = {"Institution": institution, "Name": name, "Email": email}
        self.show_question()

    # Show Current Question
    def show_question(self):
        self.clear_window()
        if self.current_q < self.total_possible:
            tk.Label(self.root, text=f"Q{self.current_q+1}. {questions[self.current_q]}",
                     font=("Helvetica", 14), wraplength=700).pack(pady=20)

            tk.Button(self.root, text="Yes", width=15, bg="lightgreen",
                      command=lambda: self.record_answer(1)).pack(pady=5)
            tk.Button(self.root, text="Partial", width=15, bg="yellow",
                      command=lambda: self.record_answer(0.5)).pack(pady=5)
            tk.Button(self.root, text="No", width=15, bg="red",
                      command=lambda: self.record_answer(0)).pack(pady=5)
        else:
            self.show_results()

    # Record Answer
    def record_answer(self, score):
        question_text = questions[self.current_q]
        self.question_scores[question_text] = score
        self.total_score += score
        self.current_q += 1
        self.show_question()

    # Show Results
    def show_results(self):
        self.clear_window()
        percentage = (self.total_score / self.total_possible) * 100
        if percentage >= 80:
            risk_level = "Low Risk (Mostly Compliant)"
        elif percentage >= 50:
            risk_level = "Medium Risk (Partially Compliant)"
        else:
            risk_level = "High Risk (Non-Compliant)"

        # Display Results
        tk.Label(self.root, text="DPDP Compliance Results", font=("Helvetica", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Institution: {self.user_details['Institution']}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.root, text=f"User Name: {self.user_details['Name']}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Email: {self.user_details['Email']}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Total Score: {self.total_score} / {self.total_possible}", font=("Helvetica", 12)).pack(pady=10)
        tk.Label(self.root, text=f"Compliance Percentage: {round(percentage, 2)}%", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Risk Level: {risk_level}", font=("Helvetica", 12, "bold")).pack(pady=10)

        # Save results automatically with date/time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.save_to_excel(percentage, risk_level, timestamp)
        self.save_to_pdf(percentage, risk_level, timestamp)

        tk.Button(self.root, text="Exit", width=15, bg="gray", command=self.root.quit).pack(pady=20)
        tk.Label(self.root, text="Results saved to Excel & PDF in the program folder", font=("Helvetica", 10, "italic")).pack(pady=5)

    # Save results to Excel
    def save_to_excel(self, percentage, risk_level, timestamp):
        data = {
            "Institution": [self.user_details['Institution']],
            "User Name": [self.user_details['Name']],
            "Email": [self.user_details['Email']],
            "Total Score": [self.total_score],
            "Compliance Percentage": [round(percentage, 2)],
            "Risk Level": [risk_level],
            "Timestamp": [timestamp]
        }
        # Add question-wise scores
        for q, s in self.question_scores.items():
            data[q] = [s]

        df = pd.DataFrame(data)
        excel_file = f"dpdp_results_{timestamp}.xlsx"
        df.to_excel(excel_file, index=False)

    # Save results to PDF
    def save_to_pdf(self, percentage, risk_level, timestamp):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "DPDP Compliance Results", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Institution: {self.user_details['Institution']}", ln=True)
        pdf.cell(0, 10, f"User Name: {self.user_details['Name']}", ln=True)
        pdf.cell(0, 10, f"Email: {self.user_details['Email']}", ln=True)
        pdf.cell(0, 10, f"Total Score: {self.total_score} / {self.total_possible}", ln=True)
        pdf.cell(0, 10, f"Compliance Percentage: {round(percentage,2)}%", ln=True)
        pdf.cell(0, 10, f"Risk Level: {risk_level}", ln=True)
        pdf.cell(0, 10, f"Timestamp: {timestamp}", ln=True)
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Question-wise Scores:", ln=True)
        pdf.set_font("Arial", "", 12)
        for idx, (q, s) in enumerate(self.question_scores.items(), start=1):
            pdf.multi_cell(0, 10, f"Q{idx}. {q} --> Score: {s}")
        pdf_file = f"dpdp_results_{timestamp}.pdf"
        pdf.output(pdf_file)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DPDPApp(root)
    root.mainloop()
