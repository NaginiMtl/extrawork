import os; os.makedirs('dist', exist_ok=True)
import re,base64
S='dist'
css=re.sub(r'@import url\([^)]*\);','',''.join(open(f'css/{n}.css').read() for n in ('tokens','components','home')))
js=open('js/main.js').read()
b64=lambda p,m:f'data:{m};base64,'+base64.b64encode(open(p,'rb').read()).decode()
def embed(s):
    for n in ('logo-light','logo-dark'): s=s.replace(f'assets/{n}.png',b64(f'assets/{n}.png','image/png'))
    s=s.replace('assets/photos/demo-expert.webp',b64('assets/photos/demo-expert.webp','image/webp')).replace('assets/photos/demo-expert.jpg',b64('assets/photos/demo-expert.jpg','image/jpeg'))
    for n in ('metier-architectes','metier-ingenieurs','metier-obnl','metier-construction','metier-designers'): s=s.replace(f'assets/photos/{n}.webp',b64(f'assets/photos/{n}.webp','image/webp'))
    return s.replace('assets/audio/presentation-kiwili.mp3',b64('assets/audio/presentation-kiwili.mp3','audio/mpeg'))
fonts='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Inter:wght@400..600&family=Caveat:wght@600&display=swap">'
h=open('index.html').read()
body=re.search(r'<body>(.*)</body>',h,re.S).group(1).replace('<script src="js/main.js"></script>','')
open(S+'/kiwili-v2.html','w').write(f'<title>Kiwili</title>\n{fonts}\n<style>{css}\nbody{{margin:0;background:var(--bg);color:var(--text);overflow-x:hidden}}\n.logo img{{height:36px;width:auto}}</style>\n{embed(body)}<script>{js}</script>')
d=open('design-system.html').read()
d=re.sub(r'<link rel="icon"[^>]*>','',d);d=re.sub(r'<link rel="preconnect"[^>]*>','',d)
d=re.sub(r'<link rel="stylesheet" href="https://fonts[^>]*>',fonts,d,1);d=re.sub(r'<link rel="stylesheet" href="css/[a-z]+\.css">\n?','',d)
d=d.replace('</head>',f'<style>{css}\n.logo img{{height:36px;width:auto}}body{{margin:0}}</style></head>').replace('<script src="js/main.js"></script>',f'<script>{js}</script>')
open(S+'/design-system-v2.html','w').write(embed(d))
