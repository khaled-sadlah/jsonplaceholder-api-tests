# script to parse pytest xml output and generate html report

import xml.etree.ElementTree as ET
import os
from datetime import datetime


def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    suites = []

    for suite in root.iter("testsuite"):
        suite_name = suite.attrib.get("name", "Unknown")
        suite_tests = int(suite.attrib.get("tests", 0))
        suite_failures = int(suite.attrib.get("failures", 0))
        suite_errors = int(suite.attrib.get("errors", 0))
        suite_skipped = int(suite.attrib.get("skipped", 0))
        suite_time = float(suite.attrib.get("time", 0))

        cases = []
        for case in suite.findall("testcase"):
            name = case.attrib.get("name", "")
            classname = case.attrib.get("classname", "")
            time = float(case.attrib.get("time", 0))

            failure = case.find("failure")
            error = case.find("error")
            skipped = case.find("skipped")

            if failure is not None:
                status = "FAILED"
                message = failure.attrib.get("message", "")
                detail = failure.text or ""
            elif error is not None:
                status = "ERROR"
                message = error.attrib.get("message", "")
                detail = error.text or ""
            elif skipped is not None:
                status = "SKIPPED"
                message = skipped.attrib.get("message", "")
                detail = ""
            else:
                status = "PASSED"
                message = ""
                detail = ""

            cases.append({
                "name": name,
                "classname": classname,
                "time": time,
                "status": status,
                "message": message,
                "detail": detail,
            })

        suites.append({
            "name": suite_name,
            "tests": suite_tests,
            "failures": suite_failures,
            "errors": suite_errors,
            "skipped": suite_skipped,
            "time": suite_time,
            "cases": cases,
        })

    return suites


def group_by_class(cases):
    groups = {}
    for case in cases:
        cls = case["classname"].split(".")[-1]
        if cls not in groups:
            groups[cls] = []
        groups[cls].append(case)
    return groups


def status_badge(status):
    colors = {
        "PASSED":  ("#d4edda", "#155724", "PASSED"),
        "FAILED":  ("#f8d7da", "#721c24", "FAILED"),
        "ERROR":   ("#fff3cd", "#856404", "ERROR"),
        "SKIPPED": ("#e2e3e5", "#383d41", "SKIPPED"),
    }
    bg, fg, label = colors.get(status, ("#eee", "#333", status))
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 10px;'
        f'border-radius:4px;font-size:12px;font-weight:600;">{label}</span>'
    )


def build_summary_cards(suites):
    total = sum(s["tests"] for s in suites)
    failed = sum(s["failures"] + s["errors"] for s in suites)
    skipped = sum(s["skipped"] for s in suites)
    passed = total - failed - skipped
    total_time = sum(s["time"] for s in suites)

    pass_rate = round((passed / total * 100), 1) if total > 0 else 0

    cards = [
        ("Total Tests", str(total), "#4a90d9"),
        ("Passed", str(passed), "#27ae60"),
        ("Failed", str(failed), "#e74c3c"),
        ("Skipped", str(skipped), "#f39c12"),
        ("Pass Rate", f"{pass_rate}%", "#8e44ad"),
        ("Duration", f"{total_time:.2f}s", "#2c3e50"),
    ]

    html = '<div style="display:flex;flex-wrap:wrap;gap:16px;margin-bottom:32px;">'
    for label, value, color in cards:
        html += f"""
        <div style="background:#fff;border-radius:8px;padding:20px 28px;
                    box-shadow:0 1px 4px rgba(0,0,0,0.1);min-width:120px;
                    border-top:4px solid {color};">
          <div style="font-size:28px;font-weight:700;color:{color};">{value}</div>
          <div style="font-size:13px;color:#666;margin-top:4px;">{label}</div>
        </div>"""
    html += "</div>"
    return html


def build_suite_section(suite):
    name = suite["name"]
    cases = suite["cases"]

    if not cases:
        return ""

    groups = group_by_class(cases)

    html = f"""
    <div style="margin-bottom:40px;">
      <h2 style="font-size:18px;color:#2c3e50;margin-bottom:16px;
                 padding-bottom:8px;border-bottom:2px solid #eee;">
        {name}
      </h2>"""

    for classname, class_cases in groups.items():
        passed = sum(1 for c in class_cases if c["status"] == "PASSED")
        total = len(class_cases)
        color = "#27ae60" if passed == total else "#e74c3c"

        html += f"""
      <div style="margin-bottom:24px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
          <span style="font-size:15px;font-weight:600;color:#34495e;">{classname}</span>
          <span style="font-size:12px;color:{color};font-weight:500;">
            {passed}/{total} passed
          </span>
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <thead>
            <tr style="background:#f8f9fa;">
              <th style="text-align:left;padding:8px 12px;color:#555;font-weight:600;border-bottom:1px solid #dee2e6;">Test Name</th>
              <th style="text-align:center;padding:8px 12px;color:#555;font-weight:600;border-bottom:1px solid #dee2e6;width:90px;">Status</th>
              <th style="text-align:right;padding:8px 12px;color:#555;font-weight:600;border-bottom:1px solid #dee2e6;width:80px;">Time</th>
            </tr>
          </thead>
          <tbody>"""

        for i, case in enumerate(class_cases):
            bg = "#fff" if i % 2 == 0 else "#fafafa"
            html += f"""
            <tr style="background:{bg};">
              <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;color:#333;">
                {case['name']}"""

            if case["message"]:
                short = case["message"][:120] + "..." if len(case["message"]) > 120 else case["message"]
                html += f"""
                <div style="font-size:11px;color:#999;margin-top:3px;">{short}</div>"""

            html += f"""
              </td>
              <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;text-align:center;">
                {status_badge(case['status'])}
              </td>
              <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;text-align:right;color:#888;">
                {case['time']:.3f}s
              </td>
            </tr>"""

        html += """
          </tbody>
        </table>
      </div>"""

    html += "</div>"
    return html


def build_html(suites, xml_path):
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(s["tests"] for s in suites)
    failed = sum(s["failures"] + s["errors"] for s in suites)
    overall = "ALL PASSED" if failed == 0 else f"{failed} FAILED"
    overall_color = "#27ae60" if failed == 0 else "#e74c3c"

    summary_cards = build_summary_cards(suites)

    suite_sections = ""
    for suite in suites:
        suite_sections += build_suite_section(suite)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Test Report - JSONPlaceholder API</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f4f6f8;
      color: #333;
      padding: 32px;
    }}
    .container {{ max-width: 1100px; margin: 0 auto; }}
    .header {{
      background: #2c3e50;
      color: white;
      padding: 28px 32px;
      border-radius: 10px;
      margin-bottom: 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .header h1 {{ font-size: 22px; font-weight: 700; }}
    .header .meta {{ font-size: 13px; opacity: 0.7; margin-top: 4px; }}
    .overall {{
      font-size: 14px;
      font-weight: 700;
      color: {overall_color};
      background: white;
      padding: 6px 16px;
      border-radius: 20px;
    }}
    .section {{
      background: #fff;
      border-radius: 10px;
      padding: 28px 32px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.08);
      margin-bottom: 24px;
    }}
    .section-title {{
      font-size: 16px;
      font-weight: 700;
      color: #2c3e50;
      margin-bottom: 20px;
    }}
    .footer {{
      text-align: center;
      font-size: 12px;
      color: #aaa;
      margin-top: 32px;
    }}
  </style>
</head>
<body>
  <div class="container">

    <div class="header">
      <div>
        <h1>JSONPlaceholder API — Test Report</h1>
        <div class="meta">Generated: {generated_at} &nbsp;|&nbsp; Source: {os.path.basename(xml_path)}</div>
      </div>
      <div class="overall">{overall}</div>
    </div>

    <div class="section">
      <div class="section-title">Summary</div>
      {summary_cards}
    </div>

    <div class="section">
      <div class="section-title">Test Results</div>
      {suite_sections}
    </div>

    <div class="footer">
      JSONPlaceholder API Test Suite &nbsp;|&nbsp; {generated_at}
    </div>

  </div>
</body>
</html>"""

    return html


def main():
    xml_path = os.path.join("reports", "report.xml")
    html_path = os.path.join("reports", "report.html")

    if not os.path.exists(xml_path):
        print(f"report.xml not found at: {xml_path}")
        print("Run pytest first to generate the XML report.")
        return

    print(f"Parsing {xml_path} ...")
    suites = parse_xml(xml_path)

    print("Building HTML report ...")
    html = build_html(suites, xml_path)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    total = sum(s["tests"] for s in suites)
    failed = sum(s["failures"] + s["errors"] for s in suites)
    passed = total - failed - sum(s["skipped"] for s in suites)

    print(f"Done. Report saved to: {html_path}")
    print(f"Results: {passed}/{total} passed, {failed} failed")


if __name__ == "__main__":
    main()
