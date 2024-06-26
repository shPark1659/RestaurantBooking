import unittest
from datetime import datetime
from unittest import skip

from booking_scheduler import TestableBookingScheduler
from communication import SmsSender, MailSender
from schedule import Customer, Schedule

NOT_ON_TIME_TIMESTAMP = datetime.strptime("2021/03/26 09:05", "%Y/%m/%d %H:%M")
ON_TIME_TIMESTAMP = datetime.strptime("2021/03/26 09:00", "%Y/%m/%d %H:%M")
DIFFERENT_TIME_TIMESTAMP = datetime.strptime("2021/03/26 10:00", "%Y/%m/%d %H:%M")
CUSTOMER = Customer("Fake name", "010-1234-5678")
CUSTOMER_WITH_MAIL = Customer("Fake name", "010-1234-5678", "fake@samsung.com")
CAPACITY_PER_HOUR = 3
UNDER_CAPACITY = 1
OVER_CAPACITY = 4


class BookingSchedulerTest(unittest.TestCase):
    def setUp(self):
        class FakeSmsSender(SmsSender):
            def __init__(self):
                self.__cnt_called = 0

            def send(self, schedule):
                self.__cnt_called += 1

            @property
            def cnt_called(self):
                return self.__cnt_called

        class FakeMailSender(MailSender):
            def __init__(self):
                self.__cnt_called = 0

            def send_mail(self, schedule):
                self.__cnt_called += 1

            @property
            def cnt_called(self):
                return self.__cnt_called

        self.fake_sms_sender = FakeSmsSender()
        self.fake_mail_sender = FakeMailSender()
        self.booking_scheduler = TestableBookingScheduler(CAPACITY_PER_HOUR, "2021/03/29 09:00")
        self.sunday_booking_scheduler = TestableBookingScheduler(CAPACITY_PER_HOUR, "2021/03/28 09:00")

    def test_예약은_정시에만_가능하다_정시가_아닌경우_예약불가(self):
        # arrange
        schedule = Schedule(NOT_ON_TIME_TIMESTAMP, UNDER_CAPACITY, CUSTOMER)

        # act and assert
        with self.assertRaises(ValueError):
            self.booking_scheduler.add_schedule(schedule)

    def test_예약은_정시에만_가능하다_정시인_경우_예약가능(self):
        # arrange
        schedule = Schedule(ON_TIME_TIMESTAMP, UNDER_CAPACITY, CUSTOMER_WITH_MAIL)

        # act
        self.booking_scheduler.add_schedule(schedule)

        # assert
        self.assertTrue(self.booking_scheduler.has_schedule(schedule))

    def test_시간대별_인원제한이_있다_같은_시간대에_Capacity_초과할_경우_예외발생(self):
        # arrange
        schedule1 = Schedule(ON_TIME_TIMESTAMP, CAPACITY_PER_HOUR, CUSTOMER)
        schedule2 = Schedule(ON_TIME_TIMESTAMP, UNDER_CAPACITY, CUSTOMER)

        self.booking_scheduler.add_schedule(schedule1)

        # act and assert
        with self.assertRaises(ValueError):
            self.booking_scheduler.add_schedule(schedule2)

    def test_시간대별_인원제한이_있다_같은_시간대가_다르면_Capacity_차있어도_스케쥴_추가_성공(self):
        # arrange
        schedule1 = Schedule(ON_TIME_TIMESTAMP, CAPACITY_PER_HOUR, CUSTOMER)
        schedule2 = Schedule(DIFFERENT_TIME_TIMESTAMP, CAPACITY_PER_HOUR, CUSTOMER)

        # act
        self.booking_scheduler.add_schedule(schedule1)
        self.booking_scheduler.add_schedule(schedule2)

        # assert
        self.assertTrue(self.booking_scheduler.has_schedule(schedule1))
        self.assertTrue(self.booking_scheduler.has_schedule(schedule2))

    def test_예약완료시_SMS는_무조건_발송(self):
        # arrange
        schedule = Schedule(ON_TIME_TIMESTAMP, UNDER_CAPACITY, CUSTOMER)

        # act
        self.booking_scheduler.set_sms_sender(self.fake_sms_sender)
        self.booking_scheduler.add_schedule(schedule)

        # assert
        self.assertEqual(1, self.fake_sms_sender.cnt_called)

    def test_이메일이_없는_경우에는_이메일_미발송(self):
        # arrange
        schedule = Schedule(ON_TIME_TIMESTAMP, UNDER_CAPACITY, CUSTOMER)

        # act
        self.booking_scheduler.set_mail_sender(self.fake_mail_sender)
        self.booking_scheduler.add_schedule(schedule)

        # assert
        self.assertEqual(0, self.fake_mail_sender.cnt_called)

    def test_이메일이_있는_경우에는_이메일_발송(self):
        # arrange
        schedule = Schedule(ON_TIME_TIMESTAMP, UNDER_CAPACITY, CUSTOMER_WITH_MAIL)

        # act
        self.booking_scheduler.set_mail_sender(self.fake_mail_sender)
        self.booking_scheduler.add_schedule(schedule)

        # assert
        self.assertEqual(1, self.fake_mail_sender.cnt_called)

    def test_현재날짜가_일요일인_경우_예약불가_예외처리(self):
        # arrange
        schedule = Schedule(ON_TIME_TIMESTAMP, CAPACITY_PER_HOUR, CUSTOMER)

        # act and assert
        with self.assertRaises(ValueError):
            self.sunday_booking_scheduler.add_schedule(schedule)

    def test_현재날짜가_일요일이_아닌경우_예약가능(self):
        # arrange
        schedule = Schedule(ON_TIME_TIMESTAMP, UNDER_CAPACITY, CUSTOMER_WITH_MAIL)

        # act
        self.booking_scheduler.add_schedule(schedule)

        # assert
        self.assertTrue(self.booking_scheduler.has_schedule(schedule))


if __name__ == '__main__':
    unittest.main()
