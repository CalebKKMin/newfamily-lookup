import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def generate_prayer():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    now = datetime.now(KST)
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    today_str = now.strftime(f"%Y년 %m월 %d일 {weekdays[now.weekday()]}")

    # 주제별 강조점을 매일 조금씩 다르게 변화
    day_of_year = now.timetuple().tm_yday
    emphases = [
        "연구의 소명과 인내에 초점을",
        "감사와 겸손에 초점을",
        "새 힘과 회복에 초점을",
        "지혜와 분별력에 초점을",
        "사랑과 섬김에 초점을",
        "믿음의 담대함에 초점을",
        "평안과 신뢰에 초점을",
    ]
    emphasis = emphases[day_of_year % 7]

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1800,
        messages=[
            {
                "role": "user",
                "content": f"""오늘({today_str})의 기도문을 작성해주세요.
매일 새롭고 다른 표현과 내용으로, 오늘은 특히 '{emphasis}' 두어 기도해주세요.

반드시 아래 7가지 주제를 모두 자연스럽게 포함하되, 단순 나열이 아닌 하나의 흐름 있는 기도가 되도록 작성해 주세요.

1. 연구원으로서의 삶
   - 연구자로서의 사명감, 탁월함, 성실함
   - 연구 결과가 사회와 하나님 나라에 기여하도록

2. 연구센터의 발전
   - 기관의 장기적 비전과 건강한 성장
   - 성실하고 유능한 연구원들이 충원되도록

3. 가족을 위한 기도
   - 아내의 건강 회복과 평안
   - 두 아들의 신앙 성장
   - 첫째 아들: 직장 인턴생활에서 지혜와 적응, 인정받음
   - 둘째 아들: 대입 준비 중 집중력, 체력, 마음의 평안

4. 교회 청년부와 청년들
   - 청년들의 신앙, 사명, 공동체 회복
   - 청년을 향한 하나님의 계획

5. 교회와 목사님들
   - 담임목사님과 모든 목사님의 건강과 사역
   - 교회 공동체가 빛과 소금이 되도록

6. 대한민국
   - 나라의 안전과 정치적 안정
   - 경제 발전과 사회 정의
   - 한국 교회의 부흥

7. 세계 평화와 복음화
   - 현재 진행 중인 전쟁과 분쟁이 종식되도록
   - 복음이 땅끝까지 전파되도록

[형식 지침]
- 하나님께 직접 드리는 1인칭 기도 형식
- 따뜻하고 간절하며 신뢰에 찬 어조
- 성경적 언어와 표현 사용
- 총 길이: 700~950자
- 예수님의 이름으로 마무리
- 날짜나 주제 번호, 소제목 등을 기도문 본문에 넣지 말 것"""
            }
        ]
    )

    return message.content[0].text


def send_email(prayer_text, recipient_email, sender_email, app_password):
    now = datetime.now(KST)
    weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    today_str = now.strftime(f"%Y년 %m월 %d일 {weekdays[now.weekday()]}")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"✝ 오늘의 기도문 — {today_str}"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    plain_body = f"오늘의 기도문 — {today_str}\n\n{prayer_text}\n\n─\n매일 오전 8시 40분 자동 발송"
    text_part = MIMEText(plain_body, "plain", "utf-8")

    html_prayer = prayer_text.replace("\n", "<br>")
    html_body = f"""<!DOCTYPE html>
<html lang="ko">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f5f3ff;font-family:'Malgun Gothic','맑은 고딕',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f3ff;padding:32px 0;">
    <tr><td align="center">
      <table width="580" cellpadding="0" cellspacing="0" style="max-width:580px;width:100%;">

        <!-- 헤더 -->
        <tr>
          <td style="background:linear-gradient(135deg,#4f46e5,#7c3aed);padding:28px 32px;border-radius:14px 14px 0 0;text-align:center;">
            <div style="font-size:1.05rem;color:rgba(255,255,255,0.85);letter-spacing:1px;margin-bottom:6px;">✝ 오늘의 기도문</div>
            <div style="font-size:1.5rem;font-weight:700;color:white;">{today_str}</div>
          </td>
        </tr>

        <!-- 본문 -->
        <tr>
          <td style="background:white;padding:32px 36px;border-radius:0 0 14px 14px;
                     box-shadow:0 4px 20px rgba(79,70,229,0.12);">
            <div style="border-left:4px solid #7c3aed;padding-left:20px;
                        color:#374151;line-height:2.0;font-size:0.97rem;">
              {html_prayer}
            </div>
            <hr style="margin:28px 0;border:none;border-top:1px solid #ede9fe;">
            <p style="margin:0;color:#a78bfa;font-size:0.78rem;text-align:center;">
              매일 오전 8시 40분 자동 발송 &nbsp;|&nbsp; Claude AI 생성
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""
    html_part = MIMEText(html_body, "html", "utf-8")

    msg.attach(text_part)
    msg.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
    print(f"[완료] 기도문 이메일 발송 → {recipient_email}")


if __name__ == "__main__":
    print("기도문 생성 중...")
    prayer = generate_prayer()
    print("── 생성된 기도문 ──")
    print(prayer)
    print("──────────────────")

    recipient = os.environ["RECIPIENT_EMAIL"]
    sender    = os.environ["GMAIL_USER"]
    password  = os.environ["GMAIL_APP_PASSWORD"]

    send_email(prayer, recipient, sender, password)
