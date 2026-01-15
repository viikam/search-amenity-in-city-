import markdown


def tohtml(name:str):
    """crée un fchier ou le modifie pour ecrire ce qu'il y a dasn un ficheir en md dans un fichier html"""
    with open(f"{name}.md", "r", encoding="utf-8") as f:
        md_text = f.read()
    text = '<!DOCTYPE html>\n\n<html lang="fr">\n\n<meta charset="UTF-8">\n\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\n<title>Resultat osm</title>\n\n<link href="osm.css" rel="stylesheet">\n\n</head>\n\n<body>\n\n' + markdown.markdown(md_text) + "\n\n</body>\n\n</html>"
    html = markdown.markdown(text)
    with open(f"{name}.html", "w+", encoding="utf-8") as f:
        f.write(html)



