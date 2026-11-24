import os
from datetime import datetime
from reportlab.pdfgen import canvas
class Recompensas:

    def __init__(self):

        self.pasta_certificados = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "certificados"
        )

        os.makedirs(
            self.pasta_certificados,
            exist_ok=True
        )
    
    def gerar_certificado(self, usuario, pontos):

        nome_arquivo = (
            f"certificado_{usuario}.pdf"
        )

        caminho = os.path.join(
            self.pasta_certificados,
            nome_arquivo
        )

        pdf = canvas.Canvas(caminho)

        pdf.setFont(
            "Helvetica-Bold",
            24
        )

        pdf.drawCentredString(
            300,
            750,
            "CERTIFICADO"
        )

        pdf.setFont(
            "Helvetica",
            16
        )

        pdf.drawCentredString(
            300,
            680,
            "Certificamos que"
        )

        pdf.setFont(
            "Helvetica-Bold",
            20
        )

        pdf.drawCentredString(
            300,
            640,
            usuario
        )

        pdf.setFont(
            "Helvetica",
            16
        )

        pdf.drawCentredString(
            300,
            600,
            "concluiu todos os módulos"
        )

        pdf.drawCentredString(
            300,
            570,
            "do sistema LibrasCode."
        )

        pdf.drawCentredString(
            300,
            530,
            f"Pontuação acumulada: {pontos}"
        )

        pdf.drawCentredString(
            300,
            490,
            f"Data: {datetime.now().strftime('%d/%m/%Y')}"
        )

        pdf.save()

        return caminho