from datetime import datetime

from schedule import Schedule
from communication import SmsSender
from communication import MailSender


class BookingScheduler:
    def __init__(self, capacity_per_hour):
        self.capacity_per_hour = capacity_per_hour
        self.schedules = []
        self.sms_sender = SmsSender()
        self.mail_sender = MailSender()

    def add_schedule(self, schedule: Schedule):
        if schedule.date_time.minute != 0:
            raise ValueError("Booking should be on the hour.")

        number_of_people = schedule.number_of_people
        for booked_schedule in self.schedules:
            if booked_schedule.date_time == schedule.date_time:
                number_of_people += booked_schedule.number_of_people
        if number_of_people > self.capacity_per_hour:
            raise ValueError("Number of people is over restaurant capacity per hour")

        # 일요일에는 시스템을 오픈하지 않는다.
        #now = datetime.now()
        #if now.weekday() == 6:  # datetime 모듈에서 일요일은 6
            #raise ValueError("Booking system is not available on Sunday")

        self.schedules.append(schedule)
        self.sms_sender.send(schedule)
        if schedule.customer.email:
            self.mail_sender.send_mail(schedule)

    def has_schedule(self, schedule):
        return schedule in self.schedules

    def set_sms_sender(self, sms_sender):
        self.sms_sender = sms_sender

    def set_mail_sender(self, mail_sender):
        self.mail_sender = mail_sender