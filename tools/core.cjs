var Kasane=(function(){
  function s2l(c){return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4);}
  function l2s(c){return c<=0.0031308?12.92*c:1.055*Math.pow(c,1/2.4)-0.055;}
  function lin(L,C,h){var r=h*Math.PI/180,a=C*Math.cos(r),b=C*Math.sin(r);
    var l_=L+0.3963377774*a+0.2158037573*b,m_=L-0.1055613458*a-0.0638541728*b,s_=L-0.0894841775*a-1.2914855480*b;
    var l=l_*l_*l_,m=m_*m_*m_,s=s_*s_*s_;
    return [4.0767416621*l-3.3077115913*m+0.2309699292*s,-1.2684380046*l+2.6097574011*m-0.3413193965*s,-0.0041960863*l-0.7034186147*m+1.7076147010*s];}
  function ing(v){return v[0]>=-0.0005&&v[0]<=1.0005&&v[1]>=-0.0005&&v[1]<=1.0005&&v[2]>=-0.0005&&v[2]<=1.0005;}
  var cache={},cusps={};
  function maxC(L,h){var k=Math.round(L*1000)+'/'+Math.round(h*10);if(cache[k]!==undefined)return cache[k];
    var lo=0,hi=0.4;for(var i=0;i<20;i++){var m=(lo+hi)/2;if(ing(lin(L,m,h)))lo=m;else hi=m;}return(cache[k]=lo);}
  function cuspL(h){var k=Math.round(h);if(cusps[k]!==undefined)return cusps[k];var best=.6,bc=-1;
    for(var L=.30;L<=.96;L+=.01){var c=maxC(L,h);if(c>bc){bc=c;best=L;}}return(cusps[k]=best);}
  function hex(L,C,h){C=Math.min(C,maxC(L,h));var v=lin(L,C,h);
    return '#'+v.map(function(c){c=Math.max(0,Math.min(1,l2s(Math.max(0,Math.min(1,c)))));return Math.round(c*255).toString(16).padStart(2,'0');}).join('');}
  function rgb(x){return [1,3,5].map(function(i){return s2l(parseInt(x.substr(i,2),16)/255);});}
  function Y(x){var c=rgb(x);return .2126*c[0]+.7152*c[1]+.0722*c[2];}
  function cr(a,b){var x=Y(a),y=Y(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
  function minCr(x,list){var m=99;list.forEach(function(o){m=Math.min(m,cr(x,o));});return m;}
  function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
  function fit(L0,dir,mkf,ok){var L=L0,x;for(var i=0;i<90;i++){x=mkf(L);if(ok(x))return {hex:x,L:L,ok:true};L+=dir*.01;if(L<.03||L>.985)break;}
    return {hex:mkf(clamp(L,.03,.985)),L:L,ok:false};}
  function hd(a,b){var d=Math.abs(a-b)%360;return d>180?360-d:d;}
  var CMAX=0.15,BASE={ok:150,danger:25,info:250},PREF={ok:1,danger:-1,info:-1};

  function build(p){
    var h=p.h,cf=p.cf,t=p.tint,deep=!!p.deep;
    var rel=function(L,f,hh){hh=hh===undefined?h:hh;return hex(L,f*CMAX,hh);};
    var abs=function(L,C,hh){return hex(L,C,hh===undefined?h:hh);};
    var cusp=cuspL(h),meta={cusp:cusp};
    /* states: move away from the accent hue when it would collide */
    var actualC=Math.min(cf*CMAX,maxC(deep?.5:.78,h)),st={};
    Object.keys(BASE).forEach(function(k){var sh=BASE[k],moved=false;
      
      st[k]={hue:sh,moved:moved};});
    /* light */
    var L={};
    L['--bg']=abs(.945,.026*t);L['--surface']=abs(.985,.014*t);L['--surface-2']=abs(.915,.028*t);L['--surface-3']=abs(.875,.032*t);
    L['--ink']=abs(.24,.012*t);
    var acc;
    if(p.accL!==undefined){var tc=p.accL<.6?'#ffffff':L['--ink'];acc=fit(p.accL,p.accL<.6?-1:1,function(l){return rel(l,cf);},function(x){return cr(x,tc)>=4.5;});L['--on-accent']=tc;}
    else if(deep){acc=fit(clamp(cusp,.46,.60),-1,function(l){return rel(l,cf);},function(x){return cr(x,'#ffffff')>=4.5;});L['--on-accent']='#ffffff';}
    else{acc=fit(clamp(cusp,.68,.86),1,function(l){return rel(l,cf);},function(x){return cr(x,L['--ink'])>=4.5;});L['--on-accent']=L['--ink'];}
    L['--accent']=acc.hex;
    L['--accent-soft']=abs(.93,.5*cf*CMAX);
    var bgs=[L['--bg'],L['--surface'],L['--surface-2']];
    L['--accent-ink']=fit(p.inkL0||.46,-1,function(l){return rel(l,cf);},function(x){return minCr(x,[L['--accent-soft']].concat(bgs))>=4.5;}).hex;
    L['--focus']=fit(.55,-1,function(l){return rel(l,cf);},function(x){return minCr(x,bgs)>=3;}).hex;
    L['--muted']=fit(.52,-1,function(l){return abs(l,.02*t);},function(x){return minCr(x,bgs)>=4.5;}).hex;
    L['--line']=fit(.72,-1,function(l){return abs(l,.03*t);},function(x){return cr(x,L['--surface'])>=3;}).hex;
    L['--switch-off']=L['--line'];L['--notice-head']=L['--ink'];
    Object.keys(st).forEach(function(k){var sh=st[k].hue;
      var sc=k==='info'?[.014,.03]:[.05,.14];
      L['--'+k+'-soft']=abs(.925,sc[0],sh);
      L['--'+k]=fit(.48,-1,function(l){return abs(l,sc[1],sh);},function(x){return cr(x,L['--'+k+'-soft'])>=4.5;}).hex;});
    /* dark */
    var D={};
    D['--bg']=abs(.205,.008*t);D['--surface']=abs(.250,.009*t);D['--surface-2']=abs(.285,.010*t);D['--surface-3']=abs(.325,.011*t);
    D['--ink']=abs(.93,.006*t);D['--on-accent']=D['--bg'];
    var dacc=fit(p.accLd!==undefined?p.accLd:(deep?clamp(cusp,.62,.74):clamp(cusp,.70,.86)),1,function(l){return rel(l,cf*.9);},function(x){return cr(x,D['--on-accent'])>=4.5;});
    D['--accent']=dacc.hex;
    D['--accent-soft']=abs(.32,.45*cf*CMAX);
    var dbgs=[D['--bg'],D['--surface'],D['--surface-2']];
    D['--accent-ink']=fit(.80,1,function(l){return rel(l,cf*.9);},function(x){return minCr(x,[D['--accent-soft']].concat(dbgs))>=4.5;}).hex;
    D['--focus']=fit(.70,1,function(l){return rel(l,cf*.9);},function(x){return minCr(x,dbgs)>=3;}).hex;
    D['--muted']=fit(.66,1,function(l){return abs(l,.02*t);},function(x){return minCr(x,dbgs)>=4.5;}).hex;
    D['--line']=fit(.45,1,function(l){return abs(l,.02*t);},function(x){return cr(x,D['--surface'])>=3;}).hex;
    D['--switch-off']=D['--line'];D['--notice-head']=D['--accent-ink'];
    Object.keys(st).forEach(function(k){var sh=st[k].hue;
      var sc=k==='info'?[.012,.03]:[.045,.13];
      D['--'+k+'-soft']=abs(.30,sc[0],sh);
      D['--'+k]=fit(.80,1,function(l){return abs(l,sc[1],sh);},function(x){return cr(x,D['--'+k+'-soft'])>=4.5;}).hex;});
    return {light:L,dark:D,states:st,meta:meta};
  }

  /* checks: [id, label, ratio, min, kind]  kind: 'req' must pass, 'ref' informational */
  function evaluate(T,theme,states,h){
    var o=[],g=function(k){return T[k];};
    var add=function(id,label,ratio,min,kind){o.push({id:id,label:label,ratio:ratio,min:min,kind:kind,pass:ratio>=min});};
    add('onAccent','ボタン上の文字',cr(g('--on-accent'),g('--accent')),4.5,'req');
    add('inkSurface','アクセント色の文字(カード上)',cr(g('--accent-ink'),g('--surface')),4.5,'req');
    add('inkSoft','アクセント色の文字(薄い面の上)',cr(g('--accent-ink'),g('--accent-soft')),4.5,'req');
    add('muted','補足の文字',minCr(g('--muted'),[g('--bg'),g('--surface'),g('--surface-2')]),4.5,'req');
    add('line','入力欄の枠・スイッチOFF',cr(g('--line'),g('--surface')),3,'req');
    add('focus','フォーカスのリング',minCr(g('--focus'),[g('--bg'),g('--surface'),g('--surface-2')]),3,'req');
    var sm=99;['ok','danger','info'].forEach(function(k){sm=Math.min(sm,cr(g('--'+k),g('--'+k+'-soft')));});
    add('state','状態色の文字(薄い面の上)',sm,4.5,'req');
    add('fill','アクセントの塗りと面の差',cr(g('--accent'),g('--surface')),3,'ref');
    add('step','面どうしの差(カード/背景)',cr(g('--surface'),g('--bg')),1.08,'ref');
    return o;
  }
  return {CMAX:CMAX,build:build,evaluate:evaluate,hex:hex,maxC:maxC,cuspL:cuspL,cr:cr,hd:hd,BASE:BASE};
})();
if(typeof module!=='undefined')module.exports=Kasane;
