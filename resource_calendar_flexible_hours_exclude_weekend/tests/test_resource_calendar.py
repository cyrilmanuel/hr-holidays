from datetime import datetime

import pytz

from odoo.tests.common import TransactionCase


class TestResourceCalendar(TransactionCase):
    def test_flexible_calendar_attendance_interval_duration_without_weekend(self):
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
            calendar.full_time_required_hours,
            "For a full day, the interval must match full time required hours",
        )

    def test_flexible_calendar_attendance_interval_duration(self):
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
            48,
            "For a full day, the interval must match full time required hours",
        )

    def test_flexible_calendar_attendance_interval_duration_friday(self):
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
            }
        )
        UTC = pytz.timezone("UTC")
        start_dt = datetime(2025, 11, 7, 0, 0, 0).astimezone(UTC)
        end_dt = datetime(2025, 11, 14, 0, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)

        actual_duration = 0
        for _res_id, work_intervals in result_per_resource_id.items():
            for start, end, _ in work_intervals:
                actual_duration += (end - start).seconds

        self.assertEqual(
            actual_duration / 3600,
            48,
            "For a full day, the interval must match full time required hours",
        )
