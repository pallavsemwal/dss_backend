
from distutils.command.config import config
from django.template import loader
import pdfkit
def generate():
#First page
    template = loader.get_template('meetings/noticeTemplate.html')
    myHtml=template.render()
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config=pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdfkit.from_string(myHtml,'meetings/temp/notice.pdf', configuration=config)
    # pdf.write_html(myHtml)
    # pdf.output('meetings/temp/notice.pdf', 'F')