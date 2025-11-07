from datetime import datetime

import pytz

from odoo.tests.common import TransactionCase


class TestResourceCalendar(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.calendar_flex_with_weekend = cls.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar (std implementation)",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": False,
                "tz": "UTC",
            }
        )
        cls.calendar_flex_without_weekend = cls.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar (exclude weekends)",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": True,
                "tz": "UTC",
            }
        )
        cls.UTC = pytz.timezone("UTC")

    def _check(self, calendar, start_dt, end_dt, expected_duration, message):
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds
        self.assertEqual(
            actual_duration / 3600,
            expected_duration,
            "for 7d starting on saturday: you get a full week duration",
        )

    def test_flexible_calendar_without_weekend_starting_sat(self):
        calendar = self.calendar_flex_without_weekend
        # start on saturday
        start_dt = datetime(2025, 11, 1, 0, 0, 0).astimezone(self.UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 8, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            calendar.full_time_required_hours,
            "for 7d starting on saturday: you get a full week duration",
        )

    def test_flexible_calendar_without_weekend_starting_mon(self):
        calendar = self.calendar_flex_without_weekend
        # start on saturday
        start_dt = datetime(2025, 11, 3, 0, 0, 0).astimezone(self.UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 10, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            calendar.full_time_required_hours,
            "for 7d starting on monday: you get a full week duration",
        )

    def test_flexible_calendar_with_weekend_interval_duration(self):
        calendar = self.calendar_flex_with_weekend
        start_dt = datetime(2025, 11, 1, 0, 0, 0).astimezone(self.UTC)
        end_dt = datetime(2025, 11, 8, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            40,
            "std behavior: for 7 days, you get full week duration",
        )

    def test_flexible_calendar_with_weekdend_friday_to_friday(self):
        calendar = self.calendar_flex_with_weekend
        # Friday (inc.) to Friday (excl.)
        start_dt = datetime(2025, 11, 7, 0, 0, 0).astimezone(self.UTC)
        end_dt = datetime(2025, 11, 14, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            40,
            "std behavior: for 7 days, you get full week duration",
        )

    def test_flexible_calendar_without_weekend_friday_sunday(self):
        calendar = self.calendar_flex_without_weekend
        start_dt = datetime(2025, 10, 31, 0, 0, 0).astimezone(self.UTC)
        end_dt = datetime(2025, 11, 3, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            8,
            "For a full day, the interval must match full time required hours",
        )

    def test_flexible_calendar_without_weekend_2w_starting_wed(self):
        calendar = self.calendar_flex_without_weekend
        # start on saturday
        start_dt = datetime(2025, 11, 5, 0, 0, 0).astimezone(self.UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 19, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            calendar.full_time_required_hours * 2,
            "for 2w starting on wed: you get 2 full weeks duration",
        )

    def test_flexible_calendar_without_weekend_10d_starting_mon(self):
        calendar = self.calendar_flex_without_weekend
        # start on saturday
        start_dt = datetime(2025, 11, 3, 0, 0, 0).astimezone(self.UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 13, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            8 * 8,
            "for 10d starting on Mon: you get 8d",
        )

    def test_flexible_calendar_without_weekend_10d_starting_fri(self):
        calendar = self.calendar_flex_without_weekend
        # start on saturday
        start_dt = datetime(2025, 11, 7, 0, 0, 0).astimezone(self.UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 17, 0, 0, 0).astimezone(self.UTC)
        self._check(
            calendar,
            start_dt,
            end_dt,
            6 * 8,
            "for 10d starting on Fri: you get 6d",
        )
