# Find the cell that created the DataMind website
matches = [
    (i, source)
    for i, source in enumerate(In)
    if 'HTML = r"""' in source
    and 'def build_sql(question):' in source
    and 'def ask_gemma(' in source
]

if not matches:
    print("Couldn't find the website cell. Don't worry; we can save it another way.")
else:
    website_source = matches[-1][1]

    with open("/content/app.py", "w", encoding="utf-8") as f:
        f.write(website_source)

    print("Saved website code to /content/app.py")