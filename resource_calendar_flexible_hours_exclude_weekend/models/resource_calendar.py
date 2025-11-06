# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections import defaultdict
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

        # 0=Monday, 6=Sunday
        weekday = start_dt.weekday()
        skipping_start_dt = start_dt
        if weekday in (5, 6):  # Saturday or Sunday
            # Move to next Monday
            days_to_monday = 7 - weekday
            skipping_start_dt += timedelta(days=days_to_monday)
        if not resources:
            resources = self.env["resource.resource"]
            resources_list = [resources]
        else:
            resources_list = list(resources) + [self.env["resource.resource"]]

        resources_with_flex_no_weekend = []
        other_resources = []
        for resource in resources_list:
            if (
                resource
                and resource.calendar_id.flexible_hours
                and resource.calendar_id.exclude_weekends
            ) or (self.flexible_hours and self.exclude_weekends):
                resources_with_flex_no_weekend.append(resource)
            else:
                other_resources.append(resources)

        res_others = super()._attendance_intervals_batch(
            start_dt, end_dt, other_resources, domain, tz, lunch
        )
        # for resources which should skip weekend we have to iterate by week
        skipping_res = defaultdict(list)
        while skipping_start_dt < end_dt:
            res_skip = super()._attendance_intervals_batch(
                skipping_start_dt,
                end_dt,
                resources_with_flex_no_weekend,
                domain,
                tz,
                lunch,
            )
            for resource, work_intervals in res_skip.items():
                new_intervals = skipping_res[resource]
                for start, end, attendance in work_intervals:
                    if start.weekday() not in (5, 6):
                        new_intervals.append((start, end, attendance))
            # go to next monday
            skipping_start_dt += timedelta(days=7 - skipping_start_dt.weekday())
        # merge both result set
        for resource, intervals in skipping_res.items():
            res_others[resource] = WorkIntervals(intervals)
        return res_others
