var path=require('path'),fs=require('fs');
var K=require('./core.cjs');
var OUT=path.join(__dirname,'.out');fs.mkdirSync(OUT,{recursive:true});
var PAL=[
 {id:'yamabuki',name:'山吹',en:'Yamabuki',h:88,cf:.8,tint:.5},
 {id:'tachibana',name:'橘',en:'Tachibana',h:58,cf:.8,tint:.5},
 {id:'kobai',name:'紅梅',en:'Kobai',h:352,cf:.8,tint:.5},
 {id:'fuji',name:'藤',en:'Fuji',h:298,cf:.8,tint:.5},
 {id:'ai',name:'藍',en:'Ai',h:256,cf:.8,tint:.5},
 {id:'sora',name:'空',en:'Sora',h:225,cf:.7,tint:.5},
 {id:'seiji',name:'青磁',en:'Seiji',h:185,cf:.55,tint:.5},
 {id:'moegi',name:'萌黄',en:'Moegi',h:115,cf:.7,tint:.5},
 {id:'sumi',name:'墨',en:'Sumi',h:80,cf:0,tint:.15,accL:.30,accLd:.88,inkL0:.28}
];
var ORDER=['--bg','--surface','--surface-2','--surface-3','--ink','--muted','--line','--switch-off','--accent','--accent-soft','--accent-ink','--on-accent','--focus','--notice-head','--ok','--ok-soft','--danger','--danger-soft','--info','--info-soft'];
function decl(o,ind){return ORDER.map(function(k){return ind+k+': '+o[k]+';';}).join('\n');}
var out={pal:[],css:'',scoped:'',stats:{}};
var css='/* Kasane palettes — generated. Usage: <html data-accent="ai">. Light, dark (prefers-color-scheme) and data-theme are all handled. */\n';
var scoped='';
PAL.forEach(function(p){
  var b=K.build(p), ev={light:K.evaluate(b.light,'light',b.states,p.h),dark:K.evaluate(b.dark,'dark',b.states,p.h)};
  var req=0,ok=0,ratios={};
  ['light','dark'].forEach(function(t){ev[t].forEach(function(e){if(e.kind==='req'){req++;if(e.pass)ok++;}ratios[t+':'+e.id]=+e.ratio.toFixed(2);});});
  out.pal.push({id:p.id,name:p.name,en:p.en,h:p.h,light:b.light,dark:b.dark,req:req,ok:ok,ratios:ratios,near:[150,25].some(function(s){return K.hd(p.h,s)<30&&p.cf>0;})});
  var first=p.id==='yamabuki',s1=':root[data-accent="'+p.id+'"]'+(first?', :root:not([data-accent])':''),s2=':root[data-accent="'+p.id+'"]:not([data-theme="light"])'+(first?', :root:not([data-accent]):not([data-theme="light"])':''),s3=':root[data-accent="'+p.id+'"][data-theme="dark"]'+(first?', :root:not([data-accent])[data-theme="dark"]':'');
  css+='\n/* '+p.name+' ('+p.en+')'+(first?' — default':'')+' */\n'+s1+' {\n'+decl(b.light,'  ')+'\n  color-scheme: light;\n}\n'
     +'@media (prefers-color-scheme: dark) {\n  '+s2+' {\n'+decl(b.dark,'    ')+'\n    color-scheme: dark;\n  }\n}\n'
     +s3+' {\n'+decl(b.dark,'  ')+'\n  color-scheme: dark;\n}\n';
  ['light','dark'].forEach(function(t){scoped+='.pv[data-accent="'+p.id+'"][data-scheme="'+t+'"]{'+ORDER.map(function(k){return k+':'+(t==='light'?b.light:b.dark)[k]+';';}).join('')+'}\n';});
});
out.css=css;out.scoped=scoped;
fs.writeFileSync(path.join(OUT,'palettes.json'),JSON.stringify(out.pal));
fs.writeFileSync(path.join(OUT,'kasane-palettes.css'),css);
out.pal.forEach(function(p){if(process.env.VERBOSE)console.log(p.name,p.id,'必須',p.ok+'/'+p.req,'fill L/D',p.ratios['light:fill'],p.ratios['dark:fill'],'accent',p.light['--accent'],p.dark['--accent'],'ink',p.light['--accent-ink'],'on',p.light['--on-accent'],p.near?'NEAR':'');});
