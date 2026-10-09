#!/usr/bin/env python3
# Regenerates the ChatCLI banner on the home pages (EN and pt) from
# the logo the CLI prints at startup (cli/welcome.go, printLogo), as an SVG
# whose colors come from style.css. Run from the docs root:
#   CHATCLI_REPO=/path/to/chatcli python3 scripts/gen-intro-banner.py
import os
import re
repo=os.environ.get('CHATCLI_REPO', os.path.expanduser('~/GolandProjects/chatcli'))
src=open(os.path.join(repo,'cli','welcome.go'),encoding='utf-8').read()
logo=src[src.index('logo := `')+len('logo := `'):]; logo=logo[:logo.index('`')]
lines=[l.rstrip() for l in logo.split('\n') if l.strip()]
ind=min(len(l)-len(l.lstrip(' ')) for l in lines); lines=[l[ind:] for l in lines]
W,H=6,10            # cell size: a monospace cell is about 0.6 as wide as tall
X1,X2=2,4           # double-line offsets across a cell
Y1,Y2=3.5,6.5
cols=max(len(l) for l in lines); rows=len(lines)
def f(v): return ('%g'%v)
def mix(t):
    # coral -> orange (at 55%) -> amber, the stops defined in style.css
    if t<=0.55: a,b,u='--cb-a','--cb-b',t/0.55
    else: a,b,u='--cb-b','--cb-c',(t-0.55)/0.45
    return 'color-mix(in oklch, var(%s) %d%%, var(%s))'%(a,round((1-u)*100),b)
fills=[]; edges=[]
for r,line in enumerate(lines):
    for c,ch in enumerate(line):
        if ch!='█': continue
        # One cell per column, colored by its column like the CLI's
        # left-to-right gradient. Mintlify strips <linearGradient> from inline
        # SVG, so each cell mixes the theme's stops (style.css) itself.
        # A hair of overlap so adjacent cells never show an anti-aliasing seam.
        fills.append('<rect x="%s" y="%s" width="%s" height="%s" style={{fill: "%s"}} />'%(f(c*W-0.05),f(r*H-0.05),f(W+0.1),f(H+0.1),mix(c/(cols-1))))
    for c,ch in enumerate(line):
        x,y=c*W,r*H
        P=lambda pts:'<path d="M%s" />'%' L'.join('%s %s'%(f(x+a),f(y+b)) for a,b in pts)
        if ch=='═': edges+= [P([(0,Y1),(W,Y1)]), P([(0,Y2),(W,Y2)])]
        elif ch=='║': edges+= [P([(X1,0),(X1,H)]), P([(X2,0),(X2,H)])]
        elif ch=='╔': edges+= [P([(X1,H),(X1,Y1),(W,Y1)]), P([(X2,H),(X2,Y2),(W,Y2)])]
        elif ch=='╗': edges+= [P([(0,Y1),(X2,Y1),(X2,H)]), P([(0,Y2),(X1,Y2),(X1,H)])]
        elif ch=='╚': edges+= [P([(X1,0),(X1,Y2),(W,Y2)]), P([(X2,0),(X2,Y1),(W,Y1)])]
        elif ch=='╝': edges+= [P([(0,Y2),(X2,Y2),(X2,0)]), P([(0,Y1),(X1,Y1),(X1,0)])]
pad=1.5
vb='%s %s %s %s'%(f(-pad),f(-pad),f(cols*W+2*pad),f(rows*H+2*pad))
svg='''<div data-chatcli-banner="" className="chatcli-banner">
  <svg role="img" aria-label="ChatCLI" viewBox="%s" className="chatcli-banner-art">
    <g className="cb-edges">
%s
    </g>
    <g className="cb-fills">
%s
    </g>
  </svg>
</div>
<div className="cb-prompt" aria-hidden="true"><span className="cb-prompt-sign">$</span> chatcli<span className="cb-cursor" /></div>'''%(vb,'\n'.join('      '+e for e in edges),'\n'.join('      '+e for e in fills))
for p in ('index.mdx','pt/index.mdx'):
    s=open(p,encoding='utf-8').read()
    i=s.index('<div role="img" aria-label="ChatCLI"') if '<div role="img" aria-label="ChatCLI"' in s else s.index('<div data-chatcli-banner=""')
    j=s.index('\n</div>\n',i)+len('\n</div>')
    # the prompt line under the art is part of the generated block
    if s.startswith('\n<div className="cb-prompt"',j):
        j=s.index('</div>',j+1)+len('</div>')
    s=s[:i]+svg+s[j:]
    open(p,'w',encoding='utf-8').write(s)
print('banner: %d rects, %d strokes, viewBox %s' % (len(fills), len(edges), vb))
