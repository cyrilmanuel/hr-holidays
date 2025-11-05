# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields, models

from odoo.addons.hr_work_entry_contract.models.hr_work_intervals import WorkIntervals


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    exclude_weekends = fields.Boolean()

    # Override to return weekends as special days if exclude_weekends is set
    def _attendance_intervals_batch(
        self, start_dt, end_dt, resources=None, domain=None, tz=None, lunch=False
    ):
        """
        Override to adjust start_dt if it falls on a weekend.
        - Convert start_dt to the relevant timezone
        - If Saturday or Sunday → move to next Monday
        - Then call super() with the adjusted start_dt
        """
        # Ensure timezone awareness
        assert start_dt.tzinfo and end_dt.tzinfo, "Datetimes must be timezone-aware"
        if self.exclude_weekends and self.flexible_hours:
            # Convert start_dt to target timezone for checking day of week
            local_start = start_dt

            # 0=Monday, 6=Sunday
            weekday = local_start.weekday()
            if weekday in (5, 6):  # Saturday or Sunday
                # Move to next Monday
                days_to_monday = 7 - weekday
                local_start = local_start + timedelta(days=days_to_monday)
                start_dt = local_start

        res = super()._attendance_intervals_batch(
            start_dt, end_dt, resources, domain, tz, lunch
        )

        # Filter out weekends from each WorkIntervals
        filtered_results = {}
        # if exclude_weekends AND flexible_hours is True,
        # filter work intervals to remove weekends
        if self.exclude_weekends and self.flexible_hours:
            for resource_id, work_intervals in res.items():
                new_intervals = []
                # Each interval = (start_datetime, end_datetime, attendance_record)
                for start, end, attendance in work_intervals:
                    # Check if start or end is during weekend
                    # weekday(): Monday = 0 ... Sunday = 6
                    if start.weekday() in (5, 6) or end.weekday() in (
                        5,
                        6,
                    ):
                        continue  # skip weekends
                    new_intervals.append((start, end, attendance))

                # Create new WorkIntervals from filtered data
                filtered_results[resource_id] = WorkIntervals(new_intervals)

            # Return the filtered WorkIntervals per resource
            return filtered_results

        return res
