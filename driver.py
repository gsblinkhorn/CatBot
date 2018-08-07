import smtplib
import config
import message

def main():
    # Send the email
    print("Connecting to server...")
    server = smtplib.SMTP('smtp.gmail.com' ,587)
    server.ehlo()
    server.starttls()

    print("Connection successful\nLogging in...")
    print(config.USER)
    print(config.PASS)
    server.login(config.USER, config.PASS)

    print("Login successful\nGenerating email...")
    server.sendmail(config.FROM, config.TO, message.generate_email())

    print("Email sent! Goodbye")
    server.quit()

if __name__ == "__main__":
    main()
