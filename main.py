
import smtplib
import dns.resolver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def is_valid_email(email):
    try:
        parts = email.split('@')
        domain = parts[1]
        answers = dns.resolver.query(domain, 'MX')
        return len(answers) > 0
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False

def send_email(sender, recipient, subject, message):
    server = None
    try:
        # SMTPサーバーに接続
        server = smtplib.SMTP(sender['smtp_server'], sender['smtp_port'])
        server.starttls()

        # ログイン
        if sender['username'] and sender['password']:
            server.login(sender['username'], sender['password'])

        # メール作成
        msg = MIMEMultipart()
        msg['From'] = sender['username']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # メール送信
        server.sendmail(sender['username'], recipient, msg.as_string())
        print("メールが送信されました。")
    except smtplib.SMTPException as e:
        print("メールの送信中にエラーが発生しました:")
        print(str(e))
    finally:
        if server is not None:
            server.quit()

def main():
    # 送信元SMTPサーバーの情報
    sender = {
        'smtp_server': input("SMTPサーバー: "),
        'smtp_port': input("SMTPポート番号: "),
        'username': input("送信元メールアドレス: "),
        'password': input("パスワード: ")
    }

    # 実行回数の指定
    try:
        num_executions = int(input("実行回数を入力してください (最大20回): "))
        if num_executions <= 0 or num_executions > 20:
            raise ValueError()
    except ValueError:
        print("実行回数は1から20の範囲で指定してください。")
        return

    for _ in range(num_executions):
        # 送信先メールアドレスの入力とチェック
        recipient = input("送信先メールアドレス: ")
        if not is_valid_email(recipient):
            print("無効なメールアドレスです。再度入力してください。")
            continue

        # 件名と本文の入力
        subject = input("件名: ")
        message = input("本文: ")

        # メール送信
        send_email(sender, recipient, subject, message)

if __name__ == "__main__":
    main()
