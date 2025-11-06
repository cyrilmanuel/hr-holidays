from datetime import datetime

import pytz

from odoo.tests.common import TransactionCase


class TestResourceCalendar(TransactionCase):
    def test_flexible_calendar_without_weekend_starting_sat(self):
        """
        Test that the duration of an attendance interval for
        flexible calendar is correctly computed.
        """
        calendar = self.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": True,
                "tz": "UTC",
            }
        )
        UTC = pytz.timezone("UTC")
        # start on saturday
        start_dt = datetime(2025, 11, 1, 0, 0, 0).astimezone(UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 8, 0, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds

        self.assertEqual(
            actual_duration / 3600,
            calendar.full_time_required_hours,
            "for 7d starting on saturday: you get a full week duration",
        )

    def test_flexible_calendar_without_weekend_starting_mon(self):
        """
        Test that the duration of an attendance interval for
        flexible calendar is correctly computed.
        """
        calendar = self.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": True,
                "tz": "UTC",
            }
        )
        UTC = pytz.timezone("UTC")
        # start on saturday
        start_dt = datetime(2025, 11, 3, 0, 0, 0).astimezone(UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 10, 0, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds

        self.assertEqual(
            actual_duration / 3600,
            calendar.full_time_required_hours,
            "for 7d starting on monday: you get a full week duration",
        )

    def test_flexible_calendar_with_weekend_interval_duration(self):
        """
        Test that the duration of an attendance interval for
        flexible calendar is correctly computed.
        """
        calendar = self.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": False,
                "tz": "UTC",
            }
        )
        UTC = pytz.timezone("UTC")
        start_dt = datetime(2025, 11, 1, 0, 0, 0).astimezone(UTC)
        end_dt = datetime(2025, 11, 8, 0, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds

        self.assertEqual(
            actual_duration / 3600,
            40,
            "std behavior: for 7 days, you get full week duration",
        )

    def test_flexible_calendar_with_weekdend_friday_to_friday(self):
        """
        Test that the duration of an attendance interval for
        flexible calendar is correctly computed.
        """
        calendar = self.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": False,
                "tz": "UTC",
            }
        )
        UTC = pytz.timezone("UTC")
        # Friday (inc.) to Friday (excl.)
        start_dt = datetime(2025, 11, 7, 0, 0, 0).astimezone(UTC)
        end_dt = datetime(2025, 11, 14, 0, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds

        self.assertEqual(
            actual_duration / 3600,
            40,
            "std behavior: for 7 days, you get full week duration",
        )

    def test_flexible_calendar_without_weekend_friday_sunday(self):
        """
        Test that the duration of an attendance interval for
        flexible calendar is correctly computed.
        """
        calendar = self.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": True,
                "tz": "UTC",
            }
        )
        UTC = pytz.timezone("UTC")
        start_dt = datetime(2025, 10, 31, 0, 0, 0).astimezone(UTC)
        end_dt = datetime(2025, 11, 3, 0, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds

        self.assertEqual(
            actual_duration / 3600,
            8,
            "For a full day, the interval must match full time required hours",
        )

    def test_flexible_calendar_without_weekend_2w_starting_wed(self):
        """
        Test that the duration of an attendance interval for
        flexible calendar is correctly computed.
        """
        calendar = self.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": True,
                "tz": "UTC",
            }
        )
        UTC = pytz.timezone("UTC")
        # start on saturday
        start_dt = datetime(2025, 11, 5, 0, 0, 0).astimezone(UTC)
        # end on friday midnight
        end_dt = datetime(2025, 11, 19, 0, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds

        self.assertEqual(
            actual_duration / 3600,
            calendar.full_time_required_hours * 2,
            "for 2w starting on wed: you get 2 full weeks duration",
        )
