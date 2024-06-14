class MailSender:
    def send_mail(self, schedule):
        if schedule.customer.email:
            print(f"Sending email to {schedule.customer.email} for schedule at {schedule.date_time}")


class SmsSender:
    def send(self, schedule):
        print(f"Sending SMS to {schedule.customer.phone_number} for schedule at {schedule.date_time}")