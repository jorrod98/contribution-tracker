from html import escape
from typing import Any
from urllib.parse import urlsplit


_STYLE = """
* { box-sizing: border-box; }
body {
  margin: 0;
  background: #f4f6fb;
  color: #172033;
  font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
main { width: min(1050px, calc(100% - 40px)); margin: 56px auto; }
.eyebrow { color: #5666c2; font-size: 12px; font-weight: 700; letter-spacing: .12em; }
h1 { margin: 8px 0; font-size: clamp(30px, 5vw, 42px); letter-spacing: -.03em; }
.subtitle { margin: 0; color: #606b7d; }
.panel {
  margin-top: 30px;
  overflow: hidden;
  border: 1px solid #e1e6ef;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 8px 28px #1c2a4410;
}
.panel-heading { padding: 18px 22px; border-bottom: 1px solid #e9edf3; font-weight: 650; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; text-align: left; }
th, td { padding: 15px 18px; border-bottom: 1px solid #edf0f5; vertical-align: top; }
th { color: #687386; font-size: 12px; font-weight: 650; text-transform: uppercase; letter-spacing: .06em; }
tbody tr:last-child td { border-bottom: 0; }
.id { color: #788397; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; }
.repo { color: #667187; font-size: 13px; }
.title { color: #22366e; font-weight: 650; text-decoration: none; }
.title:hover { text-decoration: underline; }
.status { display: inline-block; padding: 4px 9px; border-radius: 99px; background: #eef1f7; color: #515c70; font-size: 12px; white-space: nowrap; }
.status-planned { background: #eef1f7; color: #515c70; }
.status-in-progress { background: #fff3d8; color: #815b00; }
.status-pr-open { background: #e8f0ff; color: #2854a3; }
.status-merged { background: #e5f6ec; color: #267343; }
.status-closed { background: #fcebea; color: #9c3d38; }
.notes { max-width: 260px; color: #606b7d; white-space: pre-wrap; overflow-wrap: anywhere; }
.empty { padding: 42px 18px; color: #687386; text-align: center; }
footer { margin-top: 18px; color: #788397; font-size: 12px; text-align: right; }
@media (max-width: 640px) {
  main { width: min(100% - 24px, 1050px); margin: 30px auto; }
  th, td { padding: 12px; }
}
"""


def _issue_link(url: str, title: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        return (
            f'<a class="title" href="{escape(url, quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">{title}</a>'
        )
    return title


def render_html(entries: list[dict[str, Any]]) -> str:
    if not entries:
        rows = '<tr><td class="empty" colspan="4">No contributions tracked yet.</td></tr>'
    else:
        rows = "\n".join(
            "<tr>"
            f'<td class="id">{escape(str(entry.get("id", "")))}</td>'
            f'<td><div class="repo">{escape(str(entry.get("repo", "")))}</div>'
            f'<div>{_issue_link(str(entry.get("url", "")), escape(str(entry.get("title", ""))))}</div></td>'
            f'<td><span class="status status-{escape(str(entry.get("status", "unknown")))}">'
            f'{escape(str(entry.get("status", "unknown")))}</span></td>'
            f'<td class="notes">{escape(str(entry.get("notes", ""))) or "—"}</td>'
            "</tr>"
            for entry in entries
        )

    count = len(entries)
    summary = f"{count} contribution{'s' if count != 1 else ''} tracked"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contribution Tracker</title>
  <style>{_STYLE}</style>
</head>
<body>
  <main>
    <header>
      <div class="eyebrow">OPEN-SOURCE WORK</div>
      <h1>Contribution Tracker</h1>
      <p class="subtitle">A simple overview of the issues and pull requests on your radar.</p>
    </header>
    <section class="panel" aria-label="Tracked contributions">
      <div class="panel-heading">{summary}</div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Repository and issue</th><th>Status</th><th>Notes</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </section>
    <footer>Refresh this page after changing your tracker entries.</footer>
  </main>
</body>
</html>
"""
