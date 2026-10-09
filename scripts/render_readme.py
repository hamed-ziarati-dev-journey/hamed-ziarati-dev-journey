#!/usr/bin/env python3
'''Update README.md and SVG title/about/tech cards using profile.json (stdlib only).'''
from pathlib import Path
from urllib.parse import quote
import json, html, textwrap
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
c=json.loads((ROOT/'profile.json').read_text(encoding='utf-8'))
e=lambda x: html.escape(str(x),quote=True)
u=c['github_username'].strip().lstrip('@')
name=c['display_name'].strip()
about=c['about_me'].strip()
tag=c['tagline'].strip()
gh='https://github.com/'+quote(u,safe='')

# SVGs have no scripts/external dependencies; GitHub displays them through <img>.
svg_head='''<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#071522"/><stop offset="1" stop-color="#0c2230"/></linearGradient></defs>'''

def svg_txt(s,x,y,size=24,color='#ebe5d8',family='Georgia, serif',weight='400',anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{e(s)}</text>'

def wrap(s,width):
    # Preserve long text across languages; avoid potentially clipped cards.
    return textwrap.wrap(s,width=width,break_long_words=False,break_on_hyphens=False) or ['']

# Searchable text also appears as HTML in README; nameplate is the decorative gold version.
s=svg_head%(1550,194,1550,194)
s+='''<rect width="1550" height="194" rx="20" fill="url(#bg)"/>
<path d="M50 37 H412 M1138 37 H1500" stroke="#ac814e" opacity=".6"/>
<path d="M50 160 H412 M1138 160 H1500" stroke="#ac814e" opacity=".6"/>
<path d="M772 15 l9 9 -9 9 -9 -9Z" fill="#b89257"/>'''
s+=svg_txt("Hi, I'm",385,110,61,'#f8f4ec','Georgia, serif','700','middle')
s+=svg_txt(name,1000,110,72,'#e7b96f','Georgia, serif','700','middle')
s+=svg_txt(tag,775,164,24,'#bdc6ca','DejaVu Sans, sans-serif','400','middle')+'</svg>'
(A/'nameplate.svg').write_text(s,encoding='utf-8')

# About section card: exact user-provided professional description, not invented achievements.
w,h=850,535
s=svg_head%(w,h,w,h)
s+='''<rect x="3" y="3" width="844" height="529" rx="20" fill="url(#bg)" stroke="#987044" stroke-width="3"/>
<path d="M35 36 H146 M35 36 V115 M815 36 H710 M815 36 V115 M35 499 H145 M35 499 V426 M815 499 H711 M815 499 V426" stroke="#bf9459" stroke-width="2" opacity=".7" />
<circle cx="78" cy="77" r="21" fill="#daa965" opacity=".15"/><path d="M68 80 a10 10 0 1 1 20 0" stroke="#edbd78" fill="none" stroke-width="3"/>'''
s+=svg_txt('About Me',120,90,45,'#e9b976','Georgia, serif','700')
s+='<path d="M55 130 H795" stroke="#856342" opacity=".7"/>'
s+=svg_txt('COMPUTER ENGINEER',56,181,22,'#bb9360','DejaVu Sans, sans-serif','700')
for i,line in enumerate(wrap(about,42)[:4]):
    s+=svg_txt(line,56,240+i*46,31,'#f3eee6','Georgia, serif')
s+='''<path d="M55 437 H796" stroke="#856342" opacity=".6"/>
<circle cx="67" cy="474" r="6" fill="#c99854"/>'''
s+=svg_txt('Software Engineering',87,482,24,'#b6c8ce','DejaVu Sans, sans-serif')
s+='''<path d="M736 433 l46 -142 12 34 -53 134" fill="#c99d61" opacity=".55"/><path d="M740 450 L790 316" stroke="#dcb77d" stroke-width="2"/>'''
s+='</svg>'
(A/'about.svg').write_text(s,encoding='utf-8')

# Tech tile is deliberately marked as an editable example until actual skills are provided.
tech=c.get('technologies',[])[:8];w,h=850,535
s=svg_head%(w,h,w,h)
s+='''<rect x="3" y="3" width="844" height="529" rx="20" fill="url(#bg)" stroke="#987044" stroke-width="3"/>
<path d="M35 36 H146 M35 36 V115 M815 36 H710 M815 36 V115 M35 499 H145 M35 499 V426 M815 499 H711 M815 499 V426" stroke="#bf9459" stroke-width="2" opacity=".7" />'''
s+=svg_txt('</>',60,91,42,'#e8b877','DejaVu Sans, sans-serif','700')
s+=svg_txt('Tech Stack',157,88,45,'#e9b976','Georgia, serif','700')
s+=svg_txt('EXAMPLE · CUSTOMIZE',812,81,17,'#b9a17c','DejaVu Sans, sans-serif','400','end')
s+='<path d="M55 122 H796" stroke="#856342" opacity=".7"/>'
colors=['#eabd40','#e9bf4a','#439ae9','#71b8eb','#e56d40','#3b89dc','#59c6c5','#70ad68']
for i,t in enumerate(tech):
    col=i%4;row=i//4;x=50+col*197;y=156+row*168
    s+=f'<rect x="{x}" y="{y}" width="177" height="141" rx="12" fill="#0b1b2b" stroke="#304359"/>'
    # The simple initials are not an unauthorized use of brand art.
    acr={'Python':'Py','JavaScript':'JS','TypeScript':'TS','C++':'C++','HTML':'H5','CSS':'C3','React':'⚛','Node.js':'N'}.get(t,t[:3])
    s+=f'<rect x="{x+62}" y="{y+18}" width="54" height="54" rx="9" fill="{colors[i]}"/>'
    s+=svg_txt(acr,x+89,y+53,22,'#071522','DejaVu Sans, sans-serif','700','middle')
    s+=svg_txt(t,x+88,y+115,20,'#f2ebdd','DejaVu Sans, sans-serif','400','middle')
s+='</svg>'
(A/'tech-stack.svg').write_text(s,encoding='utf-8')

# No placeholder project gets an invented repository or fabricated engagement numbers.
links=[('GitHub',gh,'github'),('Repositories',gh+'?tab=repositories','github')]
for key,title,logo in [('linkedin_url','LinkedIn','linkedin'),('x_url','X','x'),('instagram_url','Instagram','instagram'),('website_url','Website','googlechrome')]:
    if c.get(key,'').strip(): links.append((title,c[key].strip(),logo))
if c.get('email','').strip(): links.append(('Email','mailto:'+c['email'].strip(),'gmail'))
social='\n'.join(f'    <a href="{e(url)}"><img src="https://img.shields.io/badge/{quote(label)}-111b27?style=for-the-badge&amp;logo={logo}&amp;logoColor=e2b36d&amp;labelColor=111b27" alt="{e(label)}"/></a>' for label,url,logo in links)
projects=[]
for i,p in enumerate(c.get('projects',[])[:3],1):
    title=p.get('title',f'Project {i}')
    description=p.get('description','Coming soon.')
    repo=p.get('repo','').strip()
    target=repo if repo.startswith('https://') else (gh+'/'+quote(repo.strip('/')) if repo else gh+'?tab=repositories')
    projects.append(f'''    <td align="center" valign="top" width="33%">
      <a href="{e(target)}"><img src="assets/project-{i}.png" width="100%" alt="{e(title)} cover" /></a>
      <b>{e(title)}</b><br/>
      <sub>{e(description)}</sub><br/>
      <a href="{e(target)}">Explore →</a>
    </td>''')
projs='\n'.join(projects)
text=f'''<!-- Midnight Wizard Academia by Hamed Ziarati -->
<!-- Edit profile.json then run: python3 scripts/render_readme.py -->

<div align="center">
  <img src="assets/banner.png" alt="Dark academia programmer desk, moonlit wizarding castle and gold lights" width="100%" />
  <br/>
  <img src="assets/avatar.png" alt="Illustrated avatar of {e(name)}" width="150" />
  <h1>Hi, I'm {e(name)} ✦</h1>
  <p><b>{e(about)}</b></p>
  <p><i>Good Code. Brighter Tomorrows.</i></p>
  <p>
{social}
  </p>
  <p>
    <img src="https://img.shields.io/badge/Computer%20Engineering-172638?style=flat-square&amp;logo=github&amp;logoColor=e2b36d" alt="Computer Engineering"/>
    <img src="https://img.shields.io/badge/Software%20Engineering-172638?style=flat-square&amp;logo=codecademy&amp;logoColor=e2b36d" alt="Software Engineering"/>
  </p>
</div>

<!-- Rendered illustration panels are editable through profile.json. -->
<table align="center">
  <tr>
    <td width="50%"><img src="assets/about.svg" alt="About Me: {e(about)}" width="100%"/></td>
    <td width="50%"><img src="assets/tech-stack.svg" alt="Example technology layout; edit profile.json with your actual technologies" width="100%"/></td>
  </tr>
</table>

<p align="center"><img src="assets/stats-heading.png" alt="GitHub Records" width="100%" /></p>

<div align="center">
  <a href="{gh}"><img src="https://github-readme-stats.vercel.app/api?username={quote(u)}&amp;show_icons=true&amp;hide_border=true&amp;bg_color=091623&amp;title_color=deb675&amp;text_color=ebedf2&amp;icon_color=d6a964&amp;ring_color=d6a964" alt="GitHub statistics for {e(name)}" height="170" /></a>
  <a href="{gh}?tab=repositories"><img src="https://github-readme-stats.vercel.app/api/top-langs/?username={quote(u)}&amp;layout=compact&amp;langs_count=6&amp;hide_border=true&amp;bg_color=091623&amp;title_color=deb675&amp;text_color=ebedf2" alt="Top languages" height="170" /></a>
  <br/>
  <img src="https://streak-stats.demolab.com?user={quote(u)}&amp;hide_border=true&amp;background=091623&amp;ring=D6A964&amp;fire=E4A65E&amp;currStreakLabel=D6A964&amp;sideLabels=DCE2E8&amp;dates=9BA7B2&amp;sideNums=F0D7A7&amp;currStreakNum=F0D7A7" alt="GitHub contribution streak" width="65%" />
</div>

<p align="center"><img src="assets/projects-heading.png" alt="Featured Projects" width="100%" /></p>
<table align="center">
  <tr>
{projs}
  </tr>
</table>
<p align="center">
  <a href="{gh}?tab=repositories">View all repositories →</a>
  <br/>
  <img src="assets/divider.png" alt="Gold divider" width="100%" />
  <img src="assets/footer.png" alt="A better developer builds a better tomorrow" width="100%" />
  <br/>
  <sub>Thanks for visiting. Keep learning. Keep building. ✦</sub>
</p>
'''
(ROOT/'README.md').write_text(text,encoding='utf-8')
print('Updated README.md and 3 SVG assets for @'+u)
