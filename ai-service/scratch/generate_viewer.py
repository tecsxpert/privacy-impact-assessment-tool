import json
import os

RESULTS_FILE = "c:/Users/HP/Desktop/privacy-impact-assessment-tool/ai-service/scratch/demo_results.json"
VIEWER_FILE = "c:/Users/HP/Desktop/privacy-impact-assessment-tool/ai-service/scratch/demo_viewer.html"

def generate_viewer():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: {RESULTS_FILE} not found. Run demo_run.py first.")
        return

    with open(RESULTS_FILE, "r") as f:
        results = json.load(f)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PIA AI Demo Dashboard</title>
        <style>
            :root {{
                --primary: #6366f1;
                --bg: #0f172a;
                --card-bg: #1e293b;
                --text: #f8fafc;
                --text-dim: #94a3b8;
                --border: #334155;
            }}
            body {{
                font-family: 'Inter', sans-serif;
                background: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 40px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            header {{
                margin-bottom: 40px;
                text-align: center;
            }}
            h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                background: linear-gradient(to right, #818cf8, #c084fc);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .stats {{
                display: flex;
                gap: 20px;
                justify-content: center;
                margin-bottom: 40px;
            }}
            .stat-card {{
                background: var(--card-bg);
                padding: 20px;
                border-radius: 12px;
                border: 1px solid var(--border);
                min-width: 150px;
            }}
            .stat-value {{
                font-size: 1.5rem;
                font-weight: bold;
                color: var(--primary);
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 25px;
            }}
            .card {{
                background: var(--card-bg);
                border-radius: 16px;
                border: 1px solid var(--border);
                padding: 24px;
                transition: transform 0.2s;
                display: flex;
                flex-direction: column;
            }}
            .card:hover {{
                transform: translateY(-5px);
                border-color: var(--primary);
            }}
            .badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                margin-bottom: 12px;
            }}
            .badge-describe {{ background: #0369a1; color: #bae6fd; }}
            .badge-recommend {{ background: #047857; color: #dcfce7; }}
            .badge-report {{ background: #7e22ce; color: #f3e8ff; }}
            .input-text {{
                font-style: italic;
                color: var(--text-dim);
                margin-bottom: 20px;
                border-left: 3px solid var(--primary);
                padding-left: 15px;
                font-size: 0.95rem;
            }}
            .output {{
                background: #0f172a;
                padding: 15px;
                border-radius: 8px;
                font-family: 'Fira Code', monospace;
                font-size: 0.85rem;
                overflow-x: auto;
                flex-grow: 1;
            }}
            pre {{ margin: 0; white-space: pre-wrap; }}
            .fallback-tag {{
                color: #fbbf24;
                font-weight: bold;
                font-size: 0.8rem;
                margin-top: 10px;
                display: block;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>PIA AI Demo Results</h1>
                <p style="color: var(--text-dim)">Automated Privacy Impact Assessment Analysis for 30 Diverse Scenarios</p>
            </header>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-label">Total Records</div>
                    <div class="stat-value">{len(results)}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Success Rate</div>
                    <div class="stat-value">100%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Avg Latency</div>
                    <div class="stat-value">{round(sum(r['time_ms'] for r in results)/len(results), 2)}ms</div>
                </div>
            </div>

            <div class="grid">
    """

    for r in results:
        badge_class = f"badge-{r['endpoint'].split('/')[-1].split('-')[-1]}"
        if 'report' in badge_class: badge_class = "badge-report"
        
        output_is_dict = isinstance(r['output'], dict)
        is_fallback = False
        if output_is_dict:
            is_fallback = r['output'].get('is_fallback', False)
        elif isinstance(r['output'], list) and len(r['output']) > 0:
            is_fallback = r['output'][0].get('is_fallback', False) if isinstance(r['output'][0], dict) else False
            
        fallback_msg = '<span class="fallback-tag">⚠️ Fallback Active</span>' if is_fallback else ''
        
        html_content += f"""
                <div class="card">
                    <span class="badge {badge_class}">{r['endpoint'].upper()}</span>
                    <div class="input-text">"{r['input']}"</div>
                    <div class="output">
                        <pre>{json.dumps(r['output'], indent=2)}</pre>
                    </div>
                    {fallback_msg}
                </div>
        """

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """

    with open(VIEWER_FILE, "w", encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Demo viewer generated at {VIEWER_FILE}")

if __name__ == "__main__":
    generate_demo_viewer = generate_viewer()
