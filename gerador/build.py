"""Gera a pasta de publicação (branch main) a partir da fonte.

Uso: python3 gerador/build.py <pasta-saida>
  - home e 404 com CSS e JS embutidos
  - páginas de segmento e privacidade (gerar_paginas.py)
  - blog, feed e sitemap (gerar_blog.py)
  - arquivos estáticos (img, robots, llms, .htaccess, verificação do Google)
"""
import os
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(RAIZ, "site")
ARTIGOS = os.path.join(RAIZ, "artigos")
GER = os.path.join(RAIZ, "gerador")
SAIDA = os.path.abspath(sys.argv[1])

if os.path.isdir(SAIDA):
    shutil.rmtree(SAIDA)
os.makedirs(SAIDA)

css = open(os.path.join(SITE, "assets/css/style.css"), encoding="utf-8").read()
js = open(os.path.join(SITE, "assets/js/main.js"), encoding="utf-8").read()


def embutir(nome):
    h = open(os.path.join(SITE, nome), encoding="utf-8").read()
    h = h.replace('<link rel="stylesheet" href="/assets/css/style.css">', "<style>\n" + css + "\n</style>")
    h = h.replace('<script src="/assets/js/main.js" defer></script>', "<script>\n" + js + "\n</script>")
    open(os.path.join(SAIDA, nome), "w", encoding="utf-8").write(h)


embutir("index.html")
embutir("404.html")

for nome in [".htaccess", "robots.txt", "llms.txt", "googled11b61e259725e11.html"]:
    shutil.copy2(os.path.join(SITE, nome), os.path.join(SAIDA, nome))
shutil.copytree(os.path.join(SITE, "img"), os.path.join(SAIDA, "img"), ignore=shutil.ignore_patterns(".gitkeep"))

subprocess.run([sys.executable, "-I", os.path.join(GER, "gerar_paginas.py"), SITE, SAIDA], check=True)
subprocess.run([sys.executable, "-I", os.path.join(GER, "gerar_blog.py"), SITE, ARTIGOS, SAIDA], check=True)
print("Publicação gerada em", SAIDA)
