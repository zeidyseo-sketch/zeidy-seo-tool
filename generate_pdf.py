from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, NextPageTemplate
from reportlab.lib.styles import ParagraphStyle
import datetime
import io

W, H = A4
PRIMARY   = colors.HexColor('#0D1B2A')
SECONDARY = colors.HexColor('#1B4F72')
ACCENT    = colors.HexColor('#00C897')
NEUTRAL   = colors.HexColor('#8D99AE')
BG        = colors.HexColor('#F0F4F8')
WHITE     = colors.white
RED       = colors.HexColor('#e74c3c')
ORANGE    = colors.HexColor('#f39c12')
GREEN     = colors.HexColor('#1a8a6e')

def draw_cover(c, data):
    c.setFillColor(PRIMARY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, H-10*mm, W, 10*mm, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.roundRect(20*mm, H-42*mm, 22*mm, 22*mm, 4, fill=1, stroke=0)
    c.setFillColor(PRIMARY)
    c.setFont('Helvetica-Bold', 18)
    c.drawCentredString(31*mm, H-33*mm, 'Z')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 24)
    c.drawString(48*mm, H-33*mm, 'Zeidy SEO')
    c.setFillColor(ACCENT)
    c.setFont('Helvetica', 11)
    c.drawString(48*mm, H-40*mm, 'Data Authority')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 36)
    c.drawCentredString(W/2, H/2+30*mm, 'SEO AUDIT')
    c.drawCentredString(W/2, H/2+18*mm, 'REPORT')
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(30*mm, H/2+10*mm, W-30*mm, H/2+10*mm)
    c.setFillColor(ACCENT)
    c.setFont('Helvetica-Bold', 20)
    c.drawCentredString(W/2, H/2-2*mm, data['domain'])
    c.setFillColor(NEUTRAL)
    c.setFont('Helvetica', 11)
    c.drawCentredString(W/2, H/2-14*mm, datetime.datetime.now().strftime('%B %Y'))
    score = data.get('score', 0)
    sc = GREEN if score>=70 else (ORANGE if score>=45 else RED)
    c.setFillColor(sc)
    c.circle(W/2, H/2-45*mm, 22*mm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(W/2, H/2-49*mm, f'{score}%')
    c.setFont('Helvetica', 8)
    c.drawCentredString(W/2, H/2-57*mm, 'SEO HEALTH SCORE')
    c.setFillColor(NEUTRAL)
    c.setFont('Helvetica', 9)
    c.drawCentredString(W/2, 12*mm, 'zeidyseo@gmail.com  |  +216 98 239 317  |  wa.me/message/LJYDD45XHP2BL1')

def draw_header_footer(c, doc, data):
    c.saveState()
    c.setFillColor(PRIMARY)
    c.rect(0, H-14*mm, W, 14*mm, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(15*mm, H-9*mm, 'Zeidy SEO')
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 9)
    c.drawRightString(W-15*mm, H-9*mm, f"SEO Audit — {data['domain']}")
    c.setFillColor(BG)
    c.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    c.setFillColor(NEUTRAL)
    c.setFont('Helvetica', 8)
    c.drawString(15*mm, 4*mm, 'zeidyseo@gmail.com  |  +216 98 239 317')
    c.drawRightString(W-15*mm, 4*mm, f'Page {doc.page}')
    c.restoreState()

def make_table(headers, rows, col_widths):
    t = Table([headers]+rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),PRIMARY),
        ('TEXTCOLOR',(0,0),(-1,0),WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#dde3ea')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,BG]),
        ('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),
    ]))
    return t

def generate_pdf(data):
    buffer = io.BytesIO()
    h1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=14, textColor=PRIMARY, spaceBefore=8*mm, spaceAfter=3*mm)
    body = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, textColor=PRIMARY, spaceAfter=2*mm)

    story = []

    def section(title, prefix=''):
        story.append(Spacer(1, 4*mm))
        story.append(HRFlowable(width='100%', thickness=1, color=BG, spaceAfter=3*mm))
        story.append(Paragraph(f'{prefix}  {title}', h1))

    # Executive Summary
    story.append(Paragraph('Executive Summary', h1))
    t = Table([
        ['SEO Health Score', f'{data["score"]}/100 — {"Good" if data["score"]>=70 else ("Needs Improvement" if data["score"]>=45 else "Poor")}'],
        ['Domain', data['domain']],
        ['Page Position', f'Page {data.get("page",2)} of Google'],
        ['Report Date', datetime.datetime.now().strftime('%B %d, %Y')],
        ['Audited By', 'Taha Zeidy | Zeidy SEO'],
    ], colWidths=[70*mm, 110*mm])
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),
        ('FONTNAME',(1,0),(1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('TEXTCOLOR',(0,0),(0,-1),NEUTRAL),
        ('TEXTCOLOR',(1,0),(1,-1),PRIMARY),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#dde3ea')),
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[BG,WHITE]),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),8),
    ]))
    story.append(t)

    # Issues
    section('Key Issues Found', '!')
    for issue in data.get('issues', []):
        col = '#e74c3c' if issue['l']=='red' else ('#f39c12' if issue['l']=='orange' else '#1a8a6e')
        prefix = '[CRITICAL]' if issue['l']=='red' else ('[WARNING]' if issue['l']=='orange' else '[INFO]')
        story.append(Paragraph(
            f'<font color="{col}"><b>{prefix}</b></font>  {issue["t"]}',
            ParagraphStyle('Issue', fontName='Helvetica', fontSize=10, textColor=PRIMARY, spaceAfter=3*mm, leftIndent=4*mm)
        ))

    # Performance
    section('Performance', 'P')
    mob, desk = data.get('mob',0), data.get('desk',0)
    story.append(make_table(
        ['Metric','Score','Status'],
        [
            ['Mobile Speed', f'{mob}/100', 'Good' if mob>=75 else ('Fair' if mob>=50 else 'Poor')],
            ['Desktop Speed', f'{desk}/100', 'Good' if desk>=80 else ('Fair' if desk>=55 else 'Poor')],
            ['HTTPS/SSL', 'Enabled' if data.get('ssl') else 'Disabled', 'Good' if data.get('ssl') else 'Critical'],
            ['Core Web Vitals', data.get('cwv','N/A'), data.get('cwv','N/A')],
        ],
        [80*mm, 50*mm, 50*mm]
    ))

    # On-Page
    section('On-Page SEO', 'O')
    def st(v): return 'Present' if v else 'Missing'
    story.append(make_table(
        ['Element','Status','Priority'],
        [
            ['Meta Title', st(data.get('hasTitle')), 'High'],
            ['Meta Description', st(data.get('hasDesc')), 'High'],
            ['H1 Tag', st(data.get('hasH1')), 'High'],
            ['Sitemap.xml', 'Found' if data.get('hasSitemap') else 'Not Found', 'Medium'],
            ['Robots.txt', 'Found' if data.get('hasRobots') else 'Not Found', 'Medium'],
        ],
        [80*mm, 60*mm, 40*mm]
    ))

    # Backlinks
    section('Backlink Profile', 'B')
    bl, rd, dr = data.get('bl',0), data.get('rd',0), data.get('dr',0)
    story.append(make_table(
        ['Metric','Value','Assessment'],
        [
            ['Total Backlinks', f'{bl:,}', 'Strong' if bl>500 else ('Moderate' if bl>100 else 'Weak')],
            ['Referring Domains', f'{rd:,}', 'Strong' if rd>200 else ('Moderate' if rd>50 else 'Weak')],
            ['Domain Rank', f'{dr}/100', 'Good' if dr>=40 else ('Fair' if dr>=20 else 'Low')],
            ['Google Maps', 'Listed' if data.get('maps') else 'Not Listed', 'Good' if data.get('maps') else 'Missing'],
        ],
        [80*mm, 50*mm, 50*mm]
    ))

    # Recommendations
    section('Top Recommendations', 'R')
    recs = []
    if not data.get('hasDesc'): recs.append('Add Meta Description to all pages to improve click-through rate')
    if not data.get('hasH1'): recs.append('Add H1 Tag — critical on-page SEO element')
    if mob < 70: recs.append(f'Improve mobile speed ({mob}/100) — compress images and enable caching')
    if not data.get('hasSitemap'): recs.append('Create and submit sitemap.xml to Google Search Console')
    if not data.get('maps'): recs.append('Create a Google Business Profile for local search visibility')
    if rd < 50: recs.append('Build quality backlinks — referring domains count is low')
    recs.append(f'Site is on page {data.get("page",2)} — focused SEO can reach page 1 in 3-4 months')
    for i, r in enumerate(recs[:6], 1):
        story.append(Paragraph(f'{i}.  {r}',
            ParagraphStyle('Rec', fontName='Helvetica', fontSize=10, textColor=PRIMARY, spaceAfter=3*mm, leftIndent=5*mm)))

    # CTA
    story.append(Spacer(1, 6*mm))
    cta = Table(
        [['Ready to improve your Google rankings?'],['Contact Taha Zeidy for a free consultation']],
        colWidths=[180*mm]
    )
    cta.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),PRIMARY),
        ('TEXTCOLOR',(0,0),(0,0),WHITE),
        ('TEXTCOLOR',(0,1),(0,1),ACCENT),
        ('FONTNAME',(0,0),(0,0),'Helvetica-Bold'),
        ('FONTNAME',(0,1),(0,1),'Helvetica'),
        ('FONTSIZE',(0,0),(0,0),13),
        ('FONTSIZE',(0,1),(0,1),10),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
    ]))
    story.append(cta)
    story.append(Spacer(1,3*mm))
    contact = Table(
        [['zeidyseo@gmail.com','+216 98 239 317','wa.me/message/LJYDD45XHP2BL1']],
        colWidths=[60*mm,60*mm,60*mm]
    )
    contact.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Helvetica'),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('TEXTCOLOR',(0,0),(-1,-1),NEUTRAL),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),4),
    ]))
    story.append(contact)

    # WhatsApp message
    wa_msg = f"""السلام عليكم،

أنا Taha من Zeidy SEO.

راجعت موقعكم *{data['domain']}* ووجدت:

• الموقع يظهر في الصفحة {data.get('page',2)} من Google
• سرعة الموبايل: {data.get('mob',0)}/100
• {f"Meta Description مفقود" if not data.get('hasDesc') else f"H1 Tag مفقود" if not data.get('hasH1') else f"يحتاج تحسين تقني"}

أرفقت تقرير مفصل مجاني يوضح كل المشاكل والحلول.

هل تحبون نتكلم؟ 📊

Taha Zeidy | Zeidy SEO
+216 98 239 317"""

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=18*mm,
        bottomMargin=16*mm,
    )
    cover_template = PageTemplate(
        id='cover',
        frames=[Frame(0,0,W,H,id='cover')],
        onPage=lambda c,d: draw_cover(c,data)
    )
    content_template = PageTemplate(
        id='content',
        frames=[Frame(15*mm,14*mm,W-30*mm,H-32*mm)],
        onPage=lambda c,d: draw_header_footer(c,d,data)
    )
    doc.addPageTemplates([cover_template, content_template])
    doc.build([NextPageTemplate('content'), PageBreak()] + story)
    buffer.seek(0)
    return buffer.getvalue(), wa_msg

if __name__ == '__main__':
    pdf_bytes, wa = generate_pdf({
        'domain':'moments1.com','page':2,'score':45,
        'mob':35,'desk':50,'ssl':True,'cwv':'Needs Improvement',
        'hasTitle':True,'hasDesc':False,'hasH1':True,
        'hasSitemap':True,'hasRobots':True,
        'bl':413,'rd':327,'dr':22,'maps':True,
        'issues':[
            {'l':'red','t':'Mobile speed is very low (35/100)'},
            {'l':'red','t':'Meta Description is missing'},
            {'l':'orange','t':'Desktop speed needs improvement (50/100)'},
            {'l':'red','t':'Site appears on page 2 — losing 90% of visitors'},
            {'l':'green','t':'Site has 413 backlinks — good foundation'},
        ]
    })
    with open('/mnt/user-data/outputs/zeidy-report-final.pdf','wb') as f:
        f.write(pdf_bytes)
    print("Done!")
    print("WhatsApp message:")
    print(wa)
