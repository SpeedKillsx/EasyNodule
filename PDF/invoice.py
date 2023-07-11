import jinja2
import pdfkit
from datetime import datetime




def MakePDF(pname , idc ,idp ,pwilaya , pphone,pemail,modc,clic,rep,cname,cid ):
  patient_name = pname
  id_cons=idc
  patient_id = idp
  patient_wilaya = pwilaya
  patient_phone = pphone
  patient_email =pemail
  model_classification = modc
  clinicien_classification =clic
  c_report = rep
  clinicien_name = cname
  clinicien_id = cid


  today_date = datetime.today().strftime("%d %b, %Y")
  month = datetime.today().strftime("%B")

  context = {'patient_name': patient_name, 'today_date': today_date, 'month': month,
            'model_classification': model_classification, 
            'clinicien_classification': clinicien_classification, 
            'c_report': c_report, 
            "id_cons":id_cons,
              "patient_id":patient_id ,
              "patient_wilaya":patient_wilaya ,
              "patient_phone":patient_phone ,
              "patient_email":patient_email,
              "clinicien_name":clinicien_name,
              "clinicien_id":clinicien_id,
          
            }

  template_loader = jinja2.FileSystemLoader('PDF\\')
  template_env = jinja2.Environment(loader=template_loader)

  html_template = 'invoice.html'
  template = template_env.get_template(html_template)
  output_text = template.render(context)

  config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
  current_date = datetime.now().strftime("%Y%m%d")
  output_pdf = f'PDF\\{id_cons}_{patient_name}_{current_date}.pdf'
  pdfkit.from_string(output_text, output_pdf, configuration=config, css='PDF\\invoice.css')


#MakePDF("Az mad","PC14447","P4474","ALger","055477447","aziz@gmail.com","benin","benin","iudhfoui osdifh poi osqdifj oisdqj fpoiqsd f  oqspdif soqdifjqos df sdqoifqs pdof sddsqfs sdqfqsdf dsqfqsdf qsdf","AMINE","C44784")