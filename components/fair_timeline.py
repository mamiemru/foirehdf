
from datetime import datetime

from nicegui import ui

from backend.models.fair_model import Fair


def format_date(dt: datetime) -> str:
    """
    Parse a datetime into humain european ridable string.

    Args:
        dt (datetime): date

    Returns:
        str: str

    """
    return dt.strftime("%d %B %Y")


def fair_timeline(fair: Fair, draw_bars: bool = True) -> None:
    """
    Display fair timeline with dates details from date.today.

    Args:
        fair (Fair): a fair
        draw_bars (bool, optional): display bars. Defaults to True.

    """
    today = datetime.today()
    total_days = (fair.end_date - fair.start_date).days
    days_passed = (today - fair.start_date).days
    progress = min(max(days_passed / total_days, 0), 1)
    ui.label(f"{_('DATES') }").classes("text-2xl font-bold")
    ui.label(f"{_('FAIR_FROM_DATE')}: {format_date(fair.start_date)}")
    ui.label(f"{_('FAIR_UNTIL_DATE')}: {format_date(fair.end_date)}")
    ui.label(f"{_('FAIR_FOR_DATE')}: {total_days} days")

    if fair.fair_incoming:
        ui.label(f"{_('FAIR_DAYS_BEFORE_THE_FAIR')}: {fair.days_before_start_date} { _('DAYS') }")
    if fair.fair_available_today:
        if fair.days_before_end_date:
            ui.label(f"{_('FAIR_DAYS_LEFT_UNTIL_END')}: {fair.days_before_end_date} { _('DAYS') }")
        else:
            ui.label(f"{_('FAIR_LAST_DAY')}")
