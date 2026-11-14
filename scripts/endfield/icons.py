"""Small line icons on a 24×24 grid, drawn with round 1.8px strokes."""

ICONS = {
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5 13.6 13.6 8.5 15.5 10.4 10.4Z"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>'
            '<path d="M12 14.5v2.5"/>',
    "cloud": '<path d="M7 18.5h10.5a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.6 9.2 4.7 4.7 0 0 0 7 18.5Z"/>',
    "pulse": '<path d="M3 12h4l2.5-6 5 12 2.5-6h4"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.3 7.5 9.5 4.3-1.2 7.5-4.9 7.5-9.5V6Z"/><path d="m9 12 2 2 4-4"/>',
    "tools": '<rect x="4" y="4" width="6.5" height="6.5" rx="1.6"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.6"/>'
             '<rect x="4" y="13.5" width="6.5" height="6.5" rx="1.6"/><path d="M16.75 13.5v6.5M13.5 16.75H20"/>',
    "gauge": '<path d="M4.5 16.5a8 8 0 1 1 15 0"/><path d="m12 13.5 3.5-4"/><circle cx="12" cy="14" r="1.4"/>',
    "bandage": '<rect x="2.8" y="8.2" width="18.4" height="7.6" rx="3.8" transform="rotate(-45 12 12)"/>'
               '<path d="M10.6 10.6h.01M13.4 13.4h.01M13.4 10.6h.01M10.6 13.4h.01"/>',
    "speech": '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H11l-4.5 4v-4A2.5 2.5 0 0 1 4 13.5Z"/>'
              '<path d="M8.5 8.5h7M8.5 11.5h4.5"/>',
    "download": '<path d="M12 4v11"/><path d="m7.5 10.5 4.5 4.5 4.5-4.5"/><path d="M5 19.5h14"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/>',
    "book": '<path d="M5 5.5A1.5 1.5 0 0 1 6.5 4H19v14H6.5A1.5 1.5 0 0 0 5 19.5Z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19"/>',
    "star": '<path d="m12 3.8 2.5 5.1 5.6.8-4 3.9.9 5.6-5-2.6-5 2.6.9-5.6-4-3.9 5.6-.8Z"/>',
    "fork": '<circle cx="7" cy="5.5" r="2"/><circle cx="17" cy="5.5" r="2"/><circle cx="12" cy="19" r="2"/>'
            '<path d="M7 7.5v1.5a3 3 0 0 0 3 3h4a3 3 0 0 0 3-3V7.5M12 12v5"/>',
    "arrow": '<path d="M7 17 17 7M9 7h8v8"/>',
}


def icon(name: str, x: float, y: float, size: float, color: str, width: float = 1.8) -> str:
    s = size / 24
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')
