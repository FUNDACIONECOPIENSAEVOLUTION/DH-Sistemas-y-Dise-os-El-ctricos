#!/usr/bin/env python3
"""Corporate DH brochure generator. Works locally and in GitHub Actions."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from io import BytesIO
from reportlab.lib.utils import ImageReader
import textwrap

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'docs'/'portafolio-dh-david-hernandez.pdf'
DEST.parent.mkdir(parents=True,exist_ok=True)
FONT_REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
# fallback for runner
for path,name in [(FONT_REG,'DHRegular'),(FONT_BOLD,'DHBold')]:
 if Path(path).exists(): pdfmetrics.registerFont(TTFont(name,path))
BODY='DHRegular' if Path(FONT_REG).exists() else 'Helvetica'
BOLD='DHBold' if Path(FONT_BOLD).exists() else 'Helvetica-Bold'
W,H=A4
DARK=HexColor('#0B1017'); DARK2=HexColor('#16202B'); GOLD=HexColor('#FFC107'); GOLD2=HexColor('#F4AC00'); WHITE=HexColor('#FFFFFF'); PALE=HexColor('#F4F6F8'); GRAY=HexColor('#6B7785'); LIGHT=HexColor('#E6EAEE')
C=canvas.Canvas(str(DEST),pagesize=A4,pageCompression=1)
C.setTitle('Portafolio corporativo | DH David Hernández - Sistemas y Diseños Eléctricos')
C.setAuthor('DH - Sistemas y Diseños Eléctricos')
C.setSubject('Portafolio de servicios eléctricos, energía, redes y automatización - edición 2026')
PAGE=0

def rect(x,y,w,h,color,r=0):
 C.setFillColor(color)
 if r: C.roundRect(x,y,w,h,r,stroke=0,fill=1)
 else:C.rect(x,y,w,h,stroke=0,fill=1)
def txt(x,y,s,size=10,color=DARK,font=BODY):
 C.setFont(font,size);C.setFillColor(color);C.drawString(x,y,s)
def textwrap_lines(s,font,size,width):
 out=[]
 for para in s.split('\n'):
  if not para:out.append('');continue
  words=para.split(' ');line=''
  for word in words:
   proposed=(line+' '+word).strip()
   if pdfmetrics.stringWidth(proposed,font,size)>width and line:
    out.append(line);line=word
   else:line=proposed
  if line:out.append(line)
 return out

def para(x,y,s,width,size=10,color=GRAY,leading=16,font=BODY,max_lines=99):
 for ln in textwrap_lines(s,font,size,width)[:max_lines]:
  txt(x,y,ln,size,color,font);y-=leading
 return y

def title(label,heading,sub=None,dark=False):
 global PAGE
 PAGE+=1
 rect(0,0,W,H,DARK if dark else WHITE)
 rect(0,H-8,W,8,GOLD)
 txt(44,H-58,f'{PAGE:02d}  /  {label.upper()}',9,GOLD2 if dark else HexColor('#AB7A00'),BOLD)
 txt(44,H-114,heading,25,WHITE if dark else DARK,BOLD)
 if sub:para(44,H-144,sub,W-88,10,HexColor('#BBC4CE') if dark else GRAY,15)
 if dark:
  C.setStrokeColor(HexColor('#2D3740'))
 else:
  C.setStrokeColor(LIGHT)
 C.line(44,58,W-44,58)
 txt(44,40,'DH  ·  DAVID HERNÁNDEZ  |  SISTEMAS Y DISEÑOS ELÉCTRICOS',7,HexColor('#88939E') if dark else GRAY,BOLD)
 txt(W-88,40,f'{PAGE:02d}',8,GOLD2,BOLD)

def end():C.showPage()
def draw_im(path,x,y,w,h):
 p=ROOT/path
 if not p.exists():return False
 try:
  im=Image.open(p).convert('RGB');iw,ih=im.size
  s=max(w/iw,h/ih);nw=round(iw*s);nh=round(ih*s)
  left=(nw-w)/2;top=(nh-h)/2
  im=im.resize((nw,nh),Image.Resampling.LANCZOS).crop((int(left),int(top),int(left+w),int(top+h)))
  bio=BytesIO();im.save(bio,'JPEG',quality=88,optimize=True);bio.seek(0)
  C.drawImage(ImageReader(bio),x,y,width=w,height=h,mask='auto')
  return True
 except Exception:return False

def stripe(y=70):
 C.setStrokeColor(GOLD);C.setLineWidth(2)
 C.line(44,y,W-44,y)

def service_box(x,top,w,h,index,name,description):
 y=top-h
 rect(x,y,w,h,PALE,8)
 rect(x,y+h-7,w,7,GOLD)
 txt(x+19,y+h-35,f'{index:02d}',14,GOLD2,BOLD)
 y1=para(x+19,y+h-65,name,w-38,13,DARK,17,BOLD)
 para(x+19,y1-11,description,w-38,9.1,GRAY,14,max_lines=12)

def section_item(y,number,heading,body):
 txt(51,y,number,12,GOLD2,BOLD)
 txt(92,y,heading,12,DARK,BOLD)
 yy=para(92,y-22,body,W-142,9.8,GRAY,16)
 C.setStrokeColor(LIGHT);C.line(92,yy-14,W-52,yy-14)
 return yy-43

# 1 cover
PAGE+=1;rect(0,0,W,H,DARK);rect(0,H-8,W,8,GOLD)
# industrial vertical lines
for x in range(10,int(W),55):rect(x,H-420,1,340,HexColor('#26333B'))
if not draw_im('assets/emblema.webp',48,H-332,W-96,230):
 txt(58,H-240,'ϟ',112,GOLD,BOLD)
txt(48,H-422,'DH',72,GOLD,BOLD)
rect(49,H-439,128,5,GOLD)
txt(48,H-485,'DAVID HERNÁNDEZ',29,WHITE,BOLD)
txt(49,H-509,'SISTEMAS Y DISEÑOS ELÉCTRICOS',11,HexColor('#C5CCD3'),BOLD)
txt(48,H-588,'PORTAFOLIO DE SERVICIOS',13,GOLD,BOLD)
para(48,H-625,'Ingeniería eléctrica · Construcción · Mantenimiento · Tecnología · Eficiencia energética',W-96,12,WHITE,20)
rect(0,0,W,98,HexColor('#131C25'))
txt(48,59,'DISEÑAMOS CON CRITERIO. EJECUTAMOS CON COMPROMISO.',9,HexColor('#E5E9EC'),BOLD)
txt(48,36,'Edición corporativa 2026     |     Colombia',8,HexColor('#ABB3BA'))
end()

# 2 who we are
title('Nuestra empresa','Energía para avanzar','Sistemas y Diseños Eléctricos David Hernández')
para(44,H-210,'Somos una empresa dedicada al diseño, construcción, mantenimiento y suministro de productos eléctricos para necesidades residenciales, comerciales e industriales. Integramos la experiencia técnica y el trabajo multidisciplinario para plantear soluciones seguras, eficientes y pertinentes.',W-88,11.5,DARK,19)
txt(44,H-329,'PROPÓSITO',11,GOLD2,BOLD)
para(44,H-359,'Aportar soluciones eléctricas confiables que contribuyan a la seguridad de las instalaciones, la continuidad de los procesos y el uso responsable de la energía.',W-90,11,GRAY,18)
txt(44,H-450,'VISIÓN DE SERVICIO',11,GOLD2,BOLD)
para(44,H-481,'Consolidar relaciones de confianza mediante calidad técnica, innovación, responsabilidad y acompañamiento cercano, adaptándonos a las necesidades de cada proyecto.',W-90,11,GRAY,18)
for i,(head,desc) in enumerate([('COMPROMISO','Con el alcance acordado'),('RESPONSABILIDAD','Con las personas y el entorno'),('INNOVACIÓN','Tecnología útil y eficiente'),('PROFESIONALISMO','Rigor y atención técnica')]):
 x=44+(i%2)*258;y=H-620-(i//2)*87
 rect(x,y-35,239,72,PALE,6);txt(x+13,y+13,head,10,DARK,BOLD);txt(x+13,y-9,desc,8.3,GRAY)
 end() if False else None
end()

# 3 + 4 services
title('Servicios','Infraestructura eléctrica','Proyectos para inmuebles residenciales, comerciales, industriales e institucionales.')
items=[('Diseño e ingeniería eléctrica','Planeación, criterios y especificaciones técnicas para soluciones eléctricas adaptadas al proyecto.'),('Redes de media y baja tensión','Construcción y adecuación de infraestructura de distribución, según competencias y exigencias aplicables.'),('Puesta a tierra y apantallamiento','Sistemas de puesta a tierra y protección contra descargas atmosféricas, de acuerdo con condiciones del inmueble.'),('Bandejas y canalizaciones','Definición y montaje de rutas para conductores, soportes, bandejas portacables y organización técnica.'),('Suministro de equipos eléctricos','Asesoría y suministro de materiales y componentes adecuados a las necesidades y especificaciones del proyecto.'),('Iluminación técnica','Diseño, instalación, modernización y mantenimiento de sistemas lumínicos y soluciones eficientes.')]
for i,(h,d) in enumerate(items): service_box(44+(i%2)*258,H-207-(i//2)*173,239,156,i+1,h,d)
end()
title('Servicios','Operación y tecnología','Seguridad, conectividad y sistemas inteligentes.')
items=[('Mantenimiento y diagnóstico','Programas preventivos, predictivos y correctivos, revisión de instalaciones, pruebas y puesta en marcha.'),('Automatización y control','Tableros de control e integración hardware/software para procesos y necesidades particulares.'),('Cableado estructurado','Instalación, mantenimiento y organización de redes de datos y telecomunicaciones.'),('Seguridad electrónica','Videovigilancia CCTV, sistemas de alarmas y control de acceso para inmuebles y empresas.'),('Domótica e inmótica','Automatización de funciones de iluminación, seguridad, control y confort en diferentes espacios.'),('Energía solar fotovoltaica','Instalación y mantenimiento de soluciones solares para aplicaciones residenciales, comerciales e industriales.')]
for i,(h,d) in enumerate(items):service_box(44+(i%2)*258,H-207-(i//2)*173,239,156,i+7,h,d)
end()

# 5 spotlight renewable
title('Enfoque sostenible','Energía con visión futura','Eficiencia energética, iluminación y sistemas fotovoltaicos.')
if not draw_im('assets/identidad.webp',44,H-463,W-88,272):
 rect(44,H-463,W-88,272,DARK2);txt(65,H-327,'DH',87,GOLD,BOLD)
txt(44,H-499,'APLICACIONES',11,GOLD2,BOLD)
para(44,H-527,'La optimización de sistemas de iluminación y el aprovechamiento solar pueden ayudar a administrar mejor los recursos energéticos. Cada propuesta requiere análisis de necesidades, condiciones de instalación, dimensionamiento y viabilidad económica.',W-88,10.5,DARK,18)
for i,t in enumerate(['Iluminación funcional y eficiente','Proyectos solares según consumo y disponibilidad','Mantenimiento y seguimiento de sistemas instalados']):
 txt(54,H-645-i*31,'✦  '+t,10,DARK,BOLD)
end()

# 6 approach
title('Metodología','Del diagnóstico a la entrega','Una ruta de trabajo orientada a decisiones técnicas fundamentadas.')
y=H-222
for n,h,b in [('01','Diagnóstico y levantamiento','Escuchamos sus necesidades, identificamos el alcance y revisamos condiciones del espacio.'),('02','Propuesta técnica','Definimos alternativas, actividades, criterios de ejecución y recursos sujetos a cotización.'),('03','Planeación y ejecución','Coordinamos actividades y desarrollamos trabajos con atención a condiciones de seguridad.'),('04','Verificación y entrega','Revisamos los entregables acordados y documentamos el cierre según las condiciones contractuales.'),('05','Mantenimiento y continuidad','Ofrecemos planes de revisión y soporte técnico cuando el proyecto lo requiera.')]:
 y=section_item(y,n,h,b)
end()

# 7 quality
title('Gestión técnica','Seguridad como prioridad','Criterios de trabajo responsables y atención al cumplimiento técnico.')
for y,h,desc in [(H-225,'SEGURIDAD ELÉCTRICA','Identificación de peligros, prevención de incidentes y adopción de controles de acuerdo con el trabajo a ejecutar.'),(H-361,'CALIDAD DE INSTALACIONES','Selección de equipos y materiales, revisión de especificaciones y verificación técnica del alcance contratado.'),(H-498,'EFICIENCIA Y MEDIO AMBIENTE','Preferencia por alternativas que reduzcan desperdicios y favorezcan un uso responsable de recursos cuando resulte viable.')]:
 rect(44,y-76,W-88,110,PALE,6);rect(44,y-76,7,110,GOLD);txt(64,y+9,h,12,DARK,BOLD);para(64,y-14,desc,W-140,9.8,GRAY,16)
rect(44,99,W-88,135,DARK2,8)
txt(61,207,'NORMATIVA DE REFERENCIA',11,GOLD,BOLD)
para(61,182,'RETIE vigente, RETILAP vigente y NTC 2050, según la actividad y el campo de aplicación. Los procesos de evaluación de conformidad o inspección, cuando correspondan, se tramitan mediante los actores competentes y autorizados.',W-124,9.4,WHITE,15)
end()

# 8 capacity
title('Alianzas y capacidades','Soluciones que se integran','Coordinación con otras especialidades según las necesidades del proyecto.')
para(44,H-217,'La empresa considera la integración de profesionales y aliados con competencias complementarias para proyectos que requieren articulación entre sistemas técnicos y actividades de obra.',W-88,11,DARK,18)
for i,(h,desc) in enumerate([('ARQUITECTURA','Integración de instalaciones con distribución arquitectónica.'),('INGENIERÍA HIDRÁULICA','Coordinación de componentes de servicios e infraestructura.'),('INGENIERÍA DE SISTEMAS','Redes, control y soluciones de conectividad.'),('INGENIERÍA ELÉCTRICA','Diseño, supervisión y ejecución según alcance.'),('SEGURIDAD Y SALUD EN EL TRABAJO','Medidas de prevención y seguridad laboral.')]):
 y=H-301-i*91
 rect(44,y-56,W-88,77,PALE,5);txt(59,y-4,f'{i+1:02d}   {h}',10,DARK,BOLD);para(59,y-24,desc,W-124,9,GRAY,13)
end()

# 9 audiences
title('Ámbitos de aplicación','Donde hay energía, hay retos','Cada solución se define según el tipo de inmueble y sus condiciones particulares.')
sectors=[('RESIDENCIAL','Instalaciones, seguridad, iluminación, domótica, energía solar y mantenimiento.'),('COMERCIAL','Redes de alimentación, iluminación, control, seguridad electrónica y adecuaciones.'),('INDUSTRIAL','Tableros, automatización, mantenimiento, redes, infraestructura y continuidad operativa.'),('INSTITUCIONAL','Soluciones de red eléctrica, eficiencia, conectividad y necesidades de infraestructura.')]
for i,(h,descr) in enumerate(sectors):
 y=H-280-i*136
 txt(44,y,h,20,DARK,BOLD);rect(44,y-18,47,3,GOLD)
 para(44,y-44,descr,W-115,10.2,GRAY,17)
end()

# 10 closing
PAGE+=1;rect(0,0,W,H,DARK);rect(0,H-8,W,8,GOLD)
if not draw_im('assets/emblema.webp',47,H-309,W-94,214):txt(47,H-220,'DH  ϟ',64,GOLD,BOLD)
txt(46,H-396,'HABLEMOS DE SU',27,WHITE,BOLD)
txt(46,H-436,'PRÓXIMO PROYECTO.',27,GOLD,BOLD)
para(46,H-477,'Estamos disponibles para conocer su necesidad y revisar el alcance técnico y comercial de la solución que busca.',W-92,11,HexColor('#B2BDC6'),19)
txt(46,H-571,'WHATSAPP COMERCIAL',9,GOLD,BOLD)
txt(46,H-599,'+57 318 682 9585',19,WHITE,BOLD)
C.linkURL('https://wa.me/573186829585',(46,H-611,320,H-567),relative=0)
txt(46,H-648,'CORREO ELECTRÓNICO',9,GOLD,BOLD)
txt(46,H-673,'sistemaselectricosdh22@gmail.com',13,WHITE,BODY)
C.linkURL('mailto:sistemaselectricosdh22@gmail.com',(46,H-681,370,H-641),relative=0)
rect(0,0,W,92,HexColor('#151F29'))
txt(46,54,'DAVID HERNÁNDEZ  /  SISTEMAS Y DISEÑOS ELÉCTRICOS',10,WHITE,BOLD)
txt(46,34,'Portafolio informativo · Edición 2026 · Colombia',8,HexColor('#ADB6C0'))
end();C.save();print(DEST,DEST.stat().st_size,'bytes',PAGE,'pages')