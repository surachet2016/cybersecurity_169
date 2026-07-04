"""Generate Thai-language PDF summaries for unit 4 and unit 5 of 10-024-109.

Renders each unit as HTML and prints it to PDF via headless Chrome, so
Thai text shaping (tone marks, combining vowels) matches the actual
website. An earlier version used fpdf2, which doesn't perform complex
-script shaping and silently mispositioned marks like ไม้เอก/ไม้โท.

Run with: python3 scripts/generate_pdfs.py
Requires: Google Chrome installed at the default macOS path.
"""

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "assets" / "pdf"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

PRIMARY_DARK = "#08406f"
ACCENT = "#1488c9"
GROUP_COLOR = "#1c8a5e"
TEXT_MUTED = "#5b6b7a"
TEXT_BODY = "#282f38"

UNITS = [
    {
        "filename": "unit4-digital-security.pdf",
        "tag": "หน่วยที่ 4",
        "title": "การจัดการความปลอดภัยในโลกดิจิทัล",
        "meta": "สัปดาห์ที่ 5-6 | ผู้สอน: อาจารย์คณะวิทยาการจัดการ",
        "intro": (
            "เมื่อชีวิตประจำวันของเราผูกติดอยู่กับอุปกรณ์ดิจิทัลและบริการออนไลน์มากขึ้น "
            "ความเข้าใจเรื่องภัยคุกคามทางไซเบอร์และวิธีป้องกันตนเองจึงเป็นทักษะที่จำเป็นสำหรับ"
            "พลเมืองดิจิทัลทุกคน เอกสารนี้สรุปภัยคุกคามที่พบบ่อย และแนวทางปฏิบัติเพื่อรักษา"
            "ความปลอดภัยในโลกดิจิทัล"
        ),
        "topics": [
            (
                "4.1 ภัยคุกคามทางไซเบอร์ที่พบบ่อย",
                "ทำความรู้จักมัลแวร์ (Malware) ไวรัสคอมพิวเตอร์ การหลอกลวงแบบฟิชชิ่ง (Phishing) "
                "และแรนซัมแวร์ (Ransomware) ที่เข้ารหัสไฟล์เพื่อเรียกค่าไถ่ พร้อมตัวอย่างรูปแบบ"
                "การหลอกลวงที่พบในชีวิตจริง เช่น อีเมลปลอม ลิงก์ปลอม และข้อความ SMS หลอกลวง "
                "ตัวอย่างที่พบบ่อยในไทยคือ SMS แอบอ้างเป็นธนาคารหรือบริษัทขนส่งหลอกให้กดลิงก์"
                "กรอกข้อมูลบัตรเครดิต หรืออีเมลปลอมจากฝ่ายไอทีองค์กรหลอกให้ติดตั้งโปรแกรมที่แท้จริง"
                "เป็นมัลแวร์ ผลกระทบอาจรุนแรงถึงขั้นสูญเสียเงินในบัญชีหรือข้อมูลส่วนตัวรั่วไหล "
                "วิธีป้องกันเบื้องต้นคือตรวจสอบชื่อผู้ส่งและโดเมนเว็บไซต์ก่อนคลิกทุกครั้ง "
                "และไม่เปิดไฟล์แนบจากผู้ส่งที่ไม่รู้จัก",
            ),
            (
                "4.2 รหัสผ่านและการยืนยันตัวตนหลายขั้นตอน",
                "หลักการตั้งรหัสผ่านที่คาดเดายาก การใช้โปรแกรมจัดการรหัสผ่าน (Password Manager) "
                "และความสำคัญของการยืนยันตัวตนแบบหลายขั้นตอน (Multi-Factor Authentication: MFA) "
                "เพื่อเพิ่มชั้นความปลอดภัยให้บัญชีออนไลน์ รหัสผ่านที่ปลอดภัยควรมีความยาวอย่างน้อย "
                "12 ตัวอักษร ผสมตัวพิมพ์ใหญ่-เล็ก ตัวเลข และสัญลักษณ์ และไม่ใช้รหัสเดียวกันซ้ำ"
                "ในหลายบริการ เพื่อลดผลกระทบหากรหัสผ่านรั่วไหลจากเว็บใดเว็บหนึ่ง (credential "
                "stuffing) การเปิดใช้ MFA เช่น รับ OTP ทาง SMS หรือแอป Authenticator จะช่วยป้องกัน"
                "บัญชีได้แม้รหัสผ่านรั่วไหลไปแล้วก็ตาม",
            ),
            (
                "4.3 การปกป้องข้อมูลส่วนบุคคล",
                "แนวทางตั้งค่าความเป็นส่วนตัวบนโซเชียลมีเดีย การจำกัดสิทธิ์การเข้าถึงข้อมูลของแอปพลิเคชัน "
                "และข้อควรระวังในการเปิดเผยข้อมูลส่วนตัวบนพื้นที่สาธารณะออนไลน์ ควรตรวจสอบและปิดสิทธิ์"
                "เข้าถึงตำแหน่งที่ตั้งหรือสมุดรายชื่อของแอปที่ไม่จำเป็นต้องใช้ ตั้งค่าโพสต์ในโซเชียลมีเดีย"
                "ให้เห็นเฉพาะเพื่อน และระมัดระวังการแชร์ข้อมูลอ่อนไหว เช่น เลขบัตรประชาชน ที่อยู่ "
                "หรือภาพถ่ายบัตรนักศึกษา ซึ่งอาจถูกนำไปแอบอ้างทำธุรกรรมหรือสร้างบัญชีปลอมในชื่อเรา",
            ),
            (
                "4.4 แนวทางปฏิบัติเพื่อความปลอดภัยในชีวิตดิจิทัล",
                "ข้อปฏิบัติพื้นฐานที่ทุกคนทำได้ทันที เช่น การอัปเดตซอฟต์แวร์ให้ทันสมัย การสำรองข้อมูลสำคัญ "
                "การตรวจสอบลิงก์ก่อนคลิก และการตั้งค่าความปลอดภัยบน Wi-Fi และอุปกรณ์ส่วนตัว เช่น "
                "ตั้งค่าสำรองข้อมูลอัตโนมัติขึ้นระบบคลาวด์อย่างน้อยสัปดาห์ละครั้ง หลีกเลี่ยงการทำ"
                "ธุรกรรมทางการเงินผ่าน Wi-Fi สาธารณะที่ไม่มีรหัสผ่าน และเปิดใช้การอัปเดตซอฟต์แวร์"
                "อัตโนมัติเพื่อปิดช่องโหว่ความปลอดภัยที่ผู้ผลิตค้นพบและแก้ไขอยู่เสมอ",
            ),
        ],
        "assignments": [
            {
                "kind": "งานเดี่ยว",
                "title": "บันทึกสะท้อนความเสี่ยงดิจิทัลของฉัน",
                "brief": (
                    "สำรวจพฤติกรรมการใช้งานดิจิทัลของตนเอง (การตั้งรหัสผ่าน การตั้งค่าความเป็นส่วนตัว "
                    "ประสบการณ์ภัยไซเบอร์ที่เคยเจอหรือเคยได้ยินจากคนใกล้ตัว) แล้ววิเคราะห์ช่องโหว่ "
                    "พร้อมเสนอแนวทางปรับปรุง โดยอ้างอิงแนวคิดจากหน่วยที่ 4 อย่างน้อย 2 หัวข้อย่อย"
                ),
                "format": "เอกสาร 1-2 หน้า (400-600 คำ)",
                "deadline": "สัปดาห์ที่ 7",
                "requirements": [
                    "พฤติกรรม/สถานการณ์ที่สำรวจ",
                    "ช่องโหว่ความเสี่ยงที่พบ พร้อมอ้างอิงทฤษฎี",
                    "แนวทางปรับปรุงที่นำไปใช้จริงได้",
                    "ข้อคิดสะท้อน (reflection)",
                ],
                "rubric": [
                    ("ความครบถ้วนของเนื้อหา", 30),
                    ("การเชื่อมโยงทฤษฎี", 30),
                    ("ความลึกของการสะท้อนคิด", 20),
                    ("การสื่อสาร/รูปแบบการเขียน", 20),
                ],
            },
            {
                "kind": "งานกลุ่ม",
                "title": "แผนรณรงค์ความปลอดภัยดิจิทัล",
                "brief": (
                    "กลุ่ม 4-5 คน สำรวจความตระหนักด้านความปลอดภัยดิจิทัลของคนรอบตัวอย่างน้อย 10 คน "
                    "ด้วยแบบสอบถามสั้น ๆ วิเคราะห์ปัญหาที่พบบ่อยที่สุด แล้วออกแบบแผนรณรงค์ "
                    "(โปสเตอร์ คลิปสั้น หรือกิจกรรม) เพื่อแก้ปัญหานั้น"
                ),
                "format": "สไลด์ 8-12 หน้า + นำเสนอ 8-10 นาที/กลุ่ม",
                "deadline": "สัปดาห์ที่ 7",
                "requirements": [
                    "ผลสำรวจพร้อมสรุปตัวเลข",
                    "ปัญหาหลักที่เลือกแก้ พร้อมเหตุผล",
                    "แผนรณรงค์ที่เป็นรูปธรรม พร้อมตัวอย่างสื่อ",
                    "บทบาทของสมาชิกแต่ละคน",
                ],
                "rubric": [
                    ("คุณภาพข้อมูลสำรวจ", 25),
                    ("ความคิดสร้างสรรค์ของแผนรณรงค์", 25),
                    ("ความเป็นไปได้ในการนำไปใช้จริง", 25),
                    ("การนำเสนอและการมีส่วนร่วมของสมาชิก", 25),
                ],
            },
        ],
    },
    {
        "filename": "unit5-digital-literacy.pdf",
        "tag": "หน่วยที่ 5",
        "title": "การรู้เท่าทันดิจิทัล",
        "meta": "สัปดาห์ที่ 7-8 | ผู้สอน: อาจารย์คณะวิทยาการจัดการ",
        "intro": (
            "ในยุคที่ข้อมูลไหลเวียนอย่างรวดเร็วบนโลกออนไลน์ การรู้เท่าทันดิจิทัล (Digital Literacy) "
            "คือทักษะการคิดวิเคราะห์เพื่อแยกแยะข้อมูลจริง-เท็จ และใช้สื่อดิจิทัลอย่างมีวิจารณญาณ "
            "เอกสารนี้มุ่งเสริมทักษะการประเมินข้อมูลและการใช้สื่ออย่างมีความรับผิดชอบ"
        ),
        "topics": [
            (
                "5.1 การประเมินความน่าเชื่อถือของแหล่งข้อมูล",
                "หลักการตรวจสอบแหล่งที่มาของข่าวและข้อมูล การสังเกตสัญญาณของข่าวปลอม (Fake News) "
                "เช่น พาดหัวเร้าอารมณ์ ไม่ระบุแหล่งอ้างอิง หรือใช้รูปภาพไม่ตรงกับเนื้อหา "
                "ข่าวที่ใช้พาดหัวกระตุ้นอารมณ์รุนแรง ไม่มีชื่อผู้เขียนหรือองค์กรที่รับผิดชอบชัดเจน "
                "หรือแชร์มาจากเพจที่ไม่เคยรู้จัก ควรตรวจสอบกับสำนักข่าวที่น่าเชื่อถือหรือเว็บไซต์"
                "ตรวจสอบข่าวลือ เช่น ศูนย์ชัวร์ก่อนแชร์ ก่อนเชื่อหรือแชร์ต่อ",
            ),
            (
                "5.2 ฟองสบู่ข้อมูลและห้องเสียงสะท้อน",
                "ทำความเข้าใจปรากฏการณ์ฟองสบู่ข้อมูล (Filter Bubble) และห้องเสียงสะท้อน (Echo Chamber) "
                "ที่เกิดจากอัลกอริทึมแนะนำเนื้อหา ซึ่งอาจทำให้เราเห็นข้อมูลเพียงด้านเดียวโดยไม่รู้ตัว "
                "เมื่อเรากดไลก์เนื้อหาฝั่งใดฝั่งหนึ่งซ้ำ ๆ ระบบจะแนะนำเนื้อหาฝั่งเดียวกันมากขึ้นเรื่อย ๆ "
                "จนเรารู้สึกว่าคนส่วนใหญ่คิดเหมือนเรา ทั้งที่ในความจริงมีความเห็นหลากหลายกว่านั้นมาก "
                "วิธีลดผลกระทบคือเปิดใจติดตามแหล่งข่าวที่มีจุดยืนต่างกันบ้าง และสังเกตตัวเองเมื่อรู้สึกว่า"
                "เห็นแต่ข้อมูลด้านเดียวซ้ำ ๆ",
            ),
            (
                "5.3 การตรวจสอบข้อเท็จจริงก่อนแชร์",
                "เทคนิคและเครื่องมือตรวจสอบข้อเท็จจริง (Fact-Checking) อย่างง่าย เช่น การค้นหาแหล่งข่าวต้นทาง "
                "การตรวจสอบภาพด้วย Reverse Image Search และการเทียบเคียงจากหลายแหล่งข่าวที่น่าเชื่อถือ "
                "ตัวอย่างเช่น ใช้ Google Reverse Image Search ตรวจว่าภาพที่แชร์มาเป็นภาพเก่าหรือถูกตัดต่อ"
                "หรือไม่ ค้นหาคำสำคัญในข่าวเพื่อดูว่ามีสำนักข่าวอื่นรายงานตรงกันหรือไม่ และตรวจสอบ"
                "วันที่เผยแพร่เพื่อดูว่าข่าวนั้นเป็นข่าวเก่าที่ถูกนำมาแชร์ใหม่ในบริบทที่ผิดหรือไม่",
            ),
            (
                "5.4 จริยธรรมในการใช้และเผยแพร่ข้อมูลดิจิทัล",
                "ความรับผิดชอบต่อสังคมในการแบ่งปันข้อมูลออนไลน์ ผลกระทบของการแชร์ข้อมูลที่ไม่ผ่านการตรวจสอบ "
                "และแนวทางการเป็นผู้ใช้สื่อดิจิทัลอย่างมีจริยธรรม การแชร์ข่าวที่ยังไม่ตรวจสอบอาจสร้าง"
                "ความเข้าใจผิดในวงกว้างและกระทบต่อบุคคลที่ตกเป็นข่าว ผู้ใช้สื่อดิจิทัลที่มีจริยธรรม"
                "ควรหยุดคิดก่อนแชร์ ให้เครดิตแหล่งที่มาเมื่อนำข้อมูลของผู้อื่นมาเผยแพร่ และพร้อมแก้ไข"
                "หรือลบข้อมูลที่พบว่าผิดพลาดทันทีที่ทราบ",
            ),
        ],
        "assignments": [
            {
                "kind": "งานเดี่ยว",
                "title": "ถอดรหัสข่าวปลอม",
                "brief": (
                    "เลือกข่าวหรือโพสต์ที่น่าสงสัยว่าเป็นข่าวปลอมหรือข้อมูลบิดเบือน 1 ชิ้นจากโซเชียลมีเดีย "
                    "ใช้เทคนิคตรวจสอบข้อเท็จจริงจากหน่วยที่ 5 วิเคราะห์ความน่าเชื่อถือ สรุปว่าจริง เท็จ "
                    "หรือบางส่วนจริง พร้อมหลักฐานอ้างอิง"
                ),
                "format": "เอกสาร 1-2 หน้า (400-600 คำ) แนบลิงก์/ภาพข่าวต้นฉบับ",
                "deadline": "สัปดาห์ที่ 9 (ก่อนสอบกลางภาค)",
                "requirements": [
                    "ที่มาของข่าว/โพสต์",
                    "ขั้นตอนตรวจสอบที่ใช้ (อย่างน้อย 2 เทคนิคจากหน่วยที่ 5)",
                    "ข้อสรุปความน่าเชื่อถือพร้อมหลักฐาน",
                    "ข้อคิดสะท้อน (reflection)",
                ],
                "rubric": [
                    ("ความถูกต้องของกระบวนการตรวจสอบ", 35),
                    ("คุณภาพหลักฐานอ้างอิง", 25),
                    ("ความสมเหตุสมผลของข้อสรุป", 25),
                    ("การสื่อสาร/รูปแบบการเขียน", 15),
                ],
            },
            {
                "kind": "งานกลุ่ม",
                "title": "แผนรณรงค์การรู้เท่าทันดิจิทัล",
                "brief": (
                    "กลุ่ม 4-5 คน สำรวจพฤติกรรมการเสพและแชร์ข่าว/ข้อมูลออนไลน์ของคนรอบตัวอย่างน้อย 10 คน "
                    "วิเคราะห์ความเสี่ยงที่พบบ่อยที่สุด (เช่น แชร์โดยไม่ตรวจสอบ ติดอยู่ในฟองสบู่ข้อมูล) "
                    "แล้วออกแบบแผนรณรงค์เพื่อส่งเสริมการรู้เท่าทันดิจิทัล"
                ),
                "format": "สไลด์ 8-12 หน้า + นำเสนอ 8-10 นาที/กลุ่ม",
                "deadline": "สัปดาห์ที่ 9 (ก่อนสอบกลางภาค)",
                "requirements": [
                    "ผลสำรวจพร้อมสรุปตัวเลข",
                    "ปัญหาหลักที่เลือกแก้ พร้อมเหตุผล",
                    "แผนรณรงค์ที่เป็นรูปธรรม พร้อมตัวอย่างสื่อ",
                    "บทบาทของสมาชิกแต่ละคน",
                ],
                "rubric": [
                    ("คุณภาพข้อมูลสำรวจ", 25),
                    ("ความคิดสร้างสรรค์ของแผนรณรงค์", 25),
                    ("ความเป็นไปได้ในการนำไปใช้จริง", 25),
                    ("การนำเสนอและการมีส่วนร่วมของสมาชิก", 25),
                ],
            },
        ],
    },
]


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    raise RuntimeError("Google Chrome not found; install it or update CHROME_CANDIDATES")


def render_assignment_html(assignment: dict) -> str:
    badge_class = "badge-single" if assignment["kind"] == "งานเดี่ยว" else "badge-group"
    requirements = "".join(f"<li>{item}</li>" for item in assignment["requirements"])
    rubric_rows = "".join(
        f"<tr><td>{criteria}</td><td>{score}</td></tr>" for criteria, score in assignment["rubric"]
    )
    return f"""
    <div class="assignment">
      <span class="badge {badge_class}">{assignment['kind']}</span>
      <h3>{assignment['title']}</h3>
      <p class="brief">{assignment['brief']}</p>
      <div class="meta-row">
        <div><div class="meta-label">รูปแบบส่ง</div><div>{assignment['format']}</div></div>
        <div><div class="meta-label">กำหนดส่ง</div><div>{assignment['deadline']}</div></div>
      </div>
      <div class="sub-label">องค์ประกอบที่ต้องมี</div>
      <ul class="req-list">{requirements}</ul>
      <div class="sub-label">เกณฑ์การให้คะแนน (เต็ม 100)</div>
      <table class="rubric"><tbody>{rubric_rows}</tbody></table>
    </div>
    """


def render_unit_html(unit: dict) -> str:
    topics_html = "".join(
        f'<div class="topic"><h2>{heading}</h2><p>{body}</p></div>'
        for heading, body in unit["topics"]
    )
    assignments_html = "".join(render_assignment_html(a) for a in unit["assignments"])
    return f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  @page {{ size: A4; margin: 15mm 15mm 18mm; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: "Sarabun", "Tahoma", sans-serif;
    color: {TEXT_BODY};
    font-size: 11.5pt;
    line-height: 1.7;
  }}
  .banner {{
    background: {PRIMARY_DARK};
    color: #fff;
    margin: 0 0 8mm;
    padding: 6mm 8mm;
    border-radius: 3mm;
  }}
  .banner .code {{ font-size: 10.5pt; font-weight: 400; margin-bottom: 2mm; }}
  .banner h1 {{ font-size: 18pt; margin: 0 0 2mm; font-weight: 700; }}
  .banner .meta {{ font-size: 10pt; font-weight: 400; }}
  .intro {{ color: {TEXT_MUTED}; margin-bottom: 6mm; }}
  .topic {{ margin-bottom: 5mm; page-break-inside: avoid; }}
  .topic h2 {{ color: {ACCENT}; font-size: 12.5pt; margin: 0 0 2mm; }}
  .topic p {{ margin: 0; }}
  .assignments-title {{
    color: {PRIMARY_DARK}; font-size: 14pt; font-weight: 700;
    margin: 0 0 4mm; page-break-before: always;
  }}
  .assignment {{ margin-bottom: 8mm; page-break-inside: avoid; }}
  .badge {{
    display: inline-block; color: #fff; font-size: 9pt; font-weight: 700;
    padding: 1mm 3mm; border-radius: 8px; margin-bottom: 2mm;
  }}
  .badge-single {{ background: {ACCENT}; }}
  .badge-group {{ background: {GROUP_COLOR}; }}
  .assignment h3 {{ font-size: 12.5pt; margin: 0 0 2mm; }}
  .brief {{ color: {TEXT_MUTED}; margin: 0 0 3mm; }}
  .meta-row {{ display: flex; gap: 6mm; margin-bottom: 3mm; }}
  .meta-label {{ color: {ACCENT}; font-size: 9pt; font-weight: 600; }}
  .sub-label {{ font-weight: 700; font-size: 10pt; margin-bottom: 1mm; }}
  .req-list {{ margin: 0 0 3mm; padding-left: 5mm; color: {TEXT_MUTED}; }}
  .req-list li {{ margin-bottom: 1mm; }}
  table.rubric {{ width: 100%; border-collapse: collapse; font-size: 10pt; margin-bottom: 2mm; }}
  table.rubric td {{ padding: 1.5mm 2mm; border-bottom: 1px solid #dde6ee; color: {TEXT_MUTED}; }}
  table.rubric td:last-child {{ width: 12mm; text-align: right; font-weight: 700; color: {PRIMARY_DARK}; }}
  .footer {{
    margin-top: 10mm;
    padding-top: 3mm;
    border-top: 1px solid #dde6ee;
    text-align: center;
    font-size: 8.5pt;
    color: {TEXT_MUTED};
  }}
</style>
</head>
<body>
  <div class="banner">
    <div class="code">10-024-109 ความฉลาดทางดิจิทัล (Digital Intelligence)</div>
    <h1>{unit['tag']}: {unit['title']}</h1>
    <div class="meta">{unit['meta']}</div>
  </div>
  <p class="intro">{unit['intro']}</p>
  {topics_html}
  <div class="assignments-title">งานมอบหมายประจำ{unit['tag']}</div>
  {assignments_html}
  <div class="footer">คณะวิทยาการจัดการ มหาวิทยาลัยนราธิวาสราชนครินทร์ - ภาคการศึกษา 1 ปีการศึกษา 2569</div>
</body>
</html>"""


def render_pdf(chrome: str, html_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_path}",
            "--virtual-time-budget=5000",
            f"file://{html_path}",
        ],
        check=True,
        capture_output=True,
    )


def main() -> None:
    chrome = find_chrome()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for unit in UNITS:
            html_path = tmp_path / f"{unit['filename']}.html"
            html_path.write_text(render_unit_html(unit), encoding="utf-8")
            out_path = OUTPUT_DIR / unit["filename"]
            render_pdf(chrome, html_path, out_path)
            print(f"created {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
