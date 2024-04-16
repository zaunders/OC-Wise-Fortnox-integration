from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import lightgrey, black, blue
from reportlab.pdfgen import canvas
import os


def make_voucher_pdf(transferId, created, value, AccountSlug, Description, LegacyId, Tags, invoiceFiles, Items, transferFee):
    invoice_file_list = invoiceFiles.split(";")
    expence_items_list = Items.split(";")

    relative_path=os.getenv("relative_path")

    # Create PDF
    pdf_path = f'{relative_path}pdfs/wise_transaction_{transferId}.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Set PDF title
    c.setTitle(f"Information about Wise-transaction #{transferId}")

    currentHeight = 60
    c.setFont("Helvetica", 14)
    c.drawString(30, height-currentHeight, f"Information about Wise-transaction #{transferId}")
    currentHeight += 20
    
    #set the link to the expense on OC
    c.setFillColor(blue)
    c.setFont("Helvetica", 10)
    expense_link = f"https://opencollective.com/borderland/projects/{AccountSlug}/expenses/{LegacyId}"
    c.drawString(30, height-currentHeight, expense_link)
    c.linkURL(expense_link, (30, height-currentHeight, 500, height-currentHeight+10), relative=1)
    c.setFillColor(black)
    currentHeight += 30

    c.setFont("Helvetica", 10)
    c.drawString(30, height-currentHeight, "Transaction made at:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150, height-currentHeight, created)
    currentHeight += 15

    c.setFont("Helvetica", 10)
    c.drawString(30, height-currentHeight, f"Description:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150, height-currentHeight, Description)    
    currentHeight += 15

    c.setFont("Helvetica", 10)
    c.drawString(30, height-currentHeight, f"Sum total:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150, height-currentHeight, f"{value} sek")
    currentHeight += 15

    c.setFont("Helvetica", 10)
    c.drawString(30, height-currentHeight, f"Transfer fee:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150, height-currentHeight, f"{transferFee} sek")
    currentHeight += 15

    
    c.setFont("Helvetica", 10)
    c.drawString(30, height-currentHeight, f"Project:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150, height-currentHeight, AccountSlug) 
    currentHeight += 15

    c.setFont("Helvetica", 10)
    c.drawString(30, height-currentHeight, f"Tags:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(150, height-currentHeight, Tags) 
    currentHeight += 30



    c.drawString(30, height-currentHeight, "Attached files:")
    currentHeight += 15
    c.setFont("Helvetica", 6)
    c.setFillColor(blue)


    if invoice_file_list[0] != '':
        for invoice_file in invoice_file_list:
            if invoice_file == '':
                break
            c.drawString(30, height-currentHeight, f"{invoice_file}")
            c.linkURL(invoice_file.strip(), (30, height-currentHeight, 500, height-currentHeight+8), relative=1)

            currentHeight += 15
    if expence_items_list[0] != '':
        for expence_item in expence_items_list:
            if expence_item == '':
                break
            c.drawString(30, height-currentHeight, f"{expence_item.strip()}")
            c.linkURL(expence_item.strip(), (30, height-currentHeight, 500, height-currentHeight+8), relative=1)
            currentHeight += 15
            
    c.save()
    return pdf_path

               
