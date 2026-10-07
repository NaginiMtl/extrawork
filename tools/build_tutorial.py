import os; os.makedirs('dist', exist_ok=True)
import re,base64
S='dist'
H=open('tutoriel.html').read()
css=re.sub(r'@import url\([^)]*\);','',''.join(open(f'css/{n}.css').read() for n in ('tokens','components','home','tutorial')))
js=open('js/main.js').read()+'\n'+open('js/tutorial.js').read()
b64=lambda p,m:f'data:{m};base64,'+base64.b64encode(open(p,'rb').read()).decode()
body=re.search(r'<body>(.*)</body>',H,re.S).group(1)
body=re.sub(r'<script src="js/[a-z]+\.js"></script>','',body)
V2='https://claude.ai/artifact/2r7wuzz47oKt5FXeB4J7jR'
body=body.replace('href="index.html#','href="'+V2+'#').replace('href="index.html"','href="'+V2+'"')
for n in ('logo-light','logo-dark'): body=body.replace(f'assets/{n}.png',b64(f'assets/{n}.png','image/png'))
import glob
for f in glob.glob('assets/tuto/*.webp'): body=body.replace(f,b64(f,'image/webp'))
fonts='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Inter:wght@400..600&family=Caveat:wght@600&display=swap">'
out=f'<title>Gestion des droits d\'accès | Centre d\'aide Kiwili</title>\n{fonts}\n<style>{css}\nbody{{margin:0;background:var(--bg);color:var(--text)}}\n.logo img{{height:36px;width:auto}}</style>\n{body}<script>{js}</script>'
open(S+'/kiwili-tutoriel.html','w').write(out)

print(len(out)//1024,'KB', out.count('assets/'))
