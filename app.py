import pandas as pd
import folium
from math import sqrt
from flask import Flask, render_template, request, jsonify

# ---- CONFIG: keep the 4 CSV files in the same folder as app.py ---------------
FILE_MAIN, FILE_COORDS = "analys_result.csv", "city_coordinates.csv"
FILE_BERUF_TOPICS, FILE_FIRMA_TOPICS = "top_beruf_topics.csv", "top_firma_topics.csv"
COL = dict(beruf=None,   # None = find the Beruf column automatically
           true_sent="sentiment", model_sent="finetuned sentiment",
           city="ausbildung place", begin="ausbildung begin", status="study condition", company="company",
           s1="first year salary", s2="second year salary", s3="third year salary")
NEED_ALL_3_SALARIES = True   # True: mean only if all 3 years exist. False: mean of the years given
# ------------------------------------------------------------------------------

norm = lambda x: str(x).strip().lower()
app = Flask(__name__)

df = pd.read_csv(FILE_MAIN)
df.columns = df.columns.str.strip().str.lower().str.replace("_", " ")
beruf_topics = pd.read_csv(FILE_BERUF_TOPICS, index_col=0)
firma_topics = pd.read_csv(FILE_FIRMA_TOPICS, index_col=0)
coords = pd.read_csv(FILE_COORDS)
coords["city"] = coords["city"].astype(str).str.strip().str.title()

# Beruf column = the column whose values match the column names of top_topics_by_beruf.csv
topic_keys = {norm(c) for c in beruf_topics.columns}
overlap = lambda c: len(set(df[c].dropna().map(norm)) & topic_keys)
BERUF = COL["beruf"] or max(df.columns, key=overlap)
if not COL["beruf"] and overlap(BERUF) == 0:
    raise SystemExit(f"Could not find the Beruf column. Set COL['beruf'] in app.py. Columns: {list(df.columns)}")
print("Beruf column:", BERUF)

df = df.dropna(subset=[BERUF]).copy()
df[BERUF] = df[BERUF].astype(str).str.strip()
df["city"] = df[COL["city"]].astype(str).str.strip().str.title()
df["year"] = pd.to_numeric(df[COL["begin"]].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")


def to_num(c):
    s = df[c]
    if pd.api.types.is_numeric_dtype(s):
        return s
    return pd.to_numeric(s.astype(str).str.replace(".", "", regex=False).str.extract(r"(\d+)")[0], errors="coerce")


df["salary_mean"] = pd.concat([to_num(COL[k]) for k in ("s1", "s2", "s3")], axis=1).mean(
    axis=1, skipna=not NEED_ALL_3_SALARIES)

SRC = {"model": COL["model_sent"], "true": COL["true_sent"]}
is_pos = lambda s: s.astype(str).str.lower().str.strip().str.startswith("pos") | (s.astype(str).str.strip() == "1")
OVERALL = {k: is_pos(df[c].dropna()).mean() * 100 for k, c in SRC.items()}   # share positive in ALL opinions


# Stack order in the study chart, bottom to top: still studying, completed, quit, other
GROUPS = {"studying": ("Noch in der Ausbildung", "#ffd166"), "completed": ("Übernommen", "#3ddc97"),
          "quit": ("Nicht Übernommen", "#ff6b6b"), "other": ("Other", "#8fa3c9")}


def status_group(v):
    t = str(v).lower()
    if any(k in t for k in ("nicht", "refus", "drop", "quit", "abgebrochen", "cancel", "not")):
        return "quit"
    if any(k in t for k in ("noch", "still", "study", "current", "laufend", "ongoing", "aktuell")):
        return "studying"
    if any(k in t for k in ("bernommen", "complet", "finish", "abgeschlossen", "bestanden", "done")):
        return "completed"
    return "other"


def selected():
    chosen = request.args.getlist("berufe") or sorted(df[BERUF].unique())   # nothing checked -> all
    return df[df[BERUF].isin(chosen)], chosen


def top_lists(table, berufe, n):
    lookup = {norm(c): c for c in table.columns}
    out = []
    for b in berufe:
        col = lookup.get(norm(b))
        out.append({"beruf": b, "topics": [t for t in table[col].tolist()[:n] if pd.notna(t)] if col else []})
    return out


@app.route("/")
def index():
    return render_template("index.html", berufe=list(df[BERUF].value_counts().sort_index().items()))


@app.route("/api/data")
def api_data():
    d, chosen = selected()
    years = d["year"].dropna()
    stats = dict(opinions=len(d), berufe=int(d[BERUF].nunique()),
                 years=f"{int(years.min())} - {int(years.max())}" if len(years) else "-")

    src = request.args.get("source", "model")
    col = SRC.get(src, SRC["model"])
    g = (d.dropna(subset=[col]).groupby(BERUF)[col]
          .agg(n="size", pos=lambda s: is_pos(s).mean() * 100).reset_index())
    sentiment = dict(beruf=g[BERUF].tolist(), pos=g["pos"].round(1).tolist(),
                     neg=(100 - g["pos"]).round(1).tolist(), n=g["n"].tolist(), overall=round(OVERALL[src], 1))

    sc = d.dropna(subset=["salary_mean"]).sort_values(BERUF)
    salary = dict(x=list(range(1, len(sc) + 1)), y=sc["salary_mean"].round(0).tolist(), beruf=sc[BERUF].tolist())

    st = d.dropna(subset=[COL["company"], COL["status"]]).copy()
    st["group"] = st[COL["status"]].map(status_group)
    cnt = st.groupby([COL["company"], "group"]).size().unstack(fill_value=0)
    cnt = cnt.loc[cnt.sum(axis=1).sort_values(ascending=False).index]       # biggest companies first
    study = dict(companies=cnt.index.tolist(),
                 series=[dict(name=GROUPS[g][0], color=GROUPS[g][1], y=cnt[g].tolist()) for g in GROUPS if g in cnt.columns])

    return jsonify(stats=stats, sentiment=sentiment, salary=salary, study=study,
                   topics=dict(beruf=top_lists(beruf_topics, chosen, 2), firma=top_lists(firma_topics, chosen, 3)))


@app.route("/map")
def city_map():
    d, _ = selected()
    cc = d["city"].value_counts().reset_index()
    cc.columns = ["city", "count"]
    cc = cc.merge(coords, on="city", how="left").dropna(subset=["latitude", "longitude"])
    colorize = request.args.get("colorize") == "1"

    m = folium.Map(location=[51.1657, 10.4515], width="100%", height=520, zoom_start=6,
                   min_zoom=5, max_zoom=12, max_bounds=True,
                   min_lat=46.5, max_lat=55.8, min_lon=5.0, max_lon=16.0, scrollWheelZoom=False)
    m.fit_bounds([[47.27, 5.87], [55.06, 15.04]])
    for _, r in cc.iterrows():
        c = r["count"]
        color = ("#d64545" if c < 5 else "#e6b800" if c <= 10 else "#2e9e4f") if colorize else "#2a6fdb"
        folium.CircleMarker(location=[r["latitude"], r["longitude"]], radius=4 + sqrt(c) * 3,
                            tooltip=f"{r['city']}: {c} opinions", color=color, fill=True,
                            fill_color=color, fill_opacity=0.6).add_to(m)

    items = ([("#d64545", "Less than 5 opinions"), ("#e6b800", "5 to 10 opinions"), ("#2e9e4f", "More than 10 opinions")]
             if colorize else [("#2a6fdb", "Circle size = number of opinions")])
    rows = "".join(f'<div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;'
                   f'background:{c};margin-right:6px"></span>{t}</div>' for c, t in items)
    m.get_root().html.add_child(folium.Element(
        '<div style="position:fixed;bottom:24px;left:24px;z-index:9999;background:#fff;padding:8px 12px;'
        f'border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,.3);font:13px sans-serif"><b>Opinions per city</b>{rows}</div>'))
    return m.get_root().render()


if __name__ == "__main__":
    app.run(debug=True)