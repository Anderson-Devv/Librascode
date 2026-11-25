from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from tkinter import filedialog

class Recompensas:

    def gerar_certificado(self, usuario, pontos):

        caminho = filedialog.asksaveasfilename(
            title="Salvar Certificado",
            initialfile=f"certificado_{usuario}.pdf",
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )

        if not caminho:
            return None

        pdf = canvas.Canvas(caminho)

        largura = 595
        altura = 842

        pdf.setStrokeColor(colors.black)
        pdf.setLineWidth(8)
        pdf.rect(20, 20, largura-40, altura-40)

        pdf.setStrokeColor(colors.darkblue)
        pdf.setLineWidth(4)
        pdf.rect(35, 35, largura-70, altura-70)

        pdf.setStrokeColor(colors.gold)
        pdf.setLineWidth(2)
        pdf.rect(50, 50, largura-100, altura-100)

        pdf.setFillColor(colors.darkblue)
        pdf.setFont("Helvetica-Bold", 28)
        pdf.drawCentredString(
            largura/2,
            730,
            "CERTIFICADO"
        )

        pdf.setStrokeColor(colors.gold)
        pdf.setLineWidth(3)
        pdf.line(
            150,
            710,
            445,
            710
        )

        pdf.setFillColor(colors.black)

        pdf.setFont("Helvetica", 16)

        pdf.drawCentredString(
            largura/2,
            640,
            "Certificamos que"
        )

        pdf.setFont(
            "Helvetica-Bold",
            24
        )

        pdf.setFillColor(colors.darkblue)

        pdf.drawCentredString(
            largura/2,
            590,
            usuario
        )

        pdf.setFillColor(colors.black)

        pdf.setFont(
            "Helvetica",
            15
        )

        pdf.drawCentredString(
            largura/2,
            530,
            "concluiu todos os módulos"
        )

        pdf.drawCentredString(
            largura/2,
            500,
            "do sistema LibrasCode."
        )

        pdf.setFillColor(colors.gold)

        pdf.setFont(
            "Helvetica-Bold",
            18
        )

        pdf.drawCentredString(
            largura/2,
            430,
            f"Pontuação Final: {pontos} pontos"
        )

        pdf.setFillColor(colors.black)

        pdf.setFont(
            "Helvetica",
            14
        )

        pdf.drawCentredString(
            largura/2,
            350,
            f"Emitido em {datetime.now().strftime('%d/%m/%Y')}"
        )

        pdf.line(
            220,
            230,
            380,
            230
        )

        pdf.drawCentredString(
            largura/2,
            210,
            "Equipe LibrasCode"
        )
        
        pdf.setFont(
            "Helvetica-Oblique",
            11
        )

        pdf.drawCentredString(
            largura/2,
            150,
            "Quando tiver medo de fazer uma decisão, pense assim: Se eu não fizer, quem fará por mim?"
        )

        pdf.save()

        return caminho