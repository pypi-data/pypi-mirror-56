!function(e,t){"function"==typeof define&&define.amd?define(t):"object"==typeof exports?module.exports=t():t()(e.lunr)}(this,function(){return function(o){o.multiLanguage=function(){for(var e=Array.prototype.slice.call(arguments),t=e.join("-"),i="",r=[],n=[],s=0;s<e.length;++s)"en"==e[s]?(i+="\\w",r.unshift(o.stopWordFilter),r.push(o.stemmer),n.push(o.stemmer)):(i+=o[e[s]].wordCharacters,o[e[s]].stopWordFilter&&r.unshift(o[e[s]].stopWordFilter),o[e[s]].stemmer&&(r.push(o[e[s]].stemmer),n.push(o[e[s]].stemmer)));var p=o.trimmerSupport.generateTrimmer(i);return o.Pipeline.registerFunction(p,"lunr-multi-trimmer-"+t),r.unshift(p),function(){this.pipeline.reset(),this.pipeline.add.apply(this.pipeline,r),this.searchPipeline&&(this.searchPipeline.reset(),this.searchPipeline.add.apply(this.searchPipeline,n))}}}});