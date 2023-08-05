/*! *****************************************************************************
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
MERCHANTABLITY OR NON-INFRINGEMENT.

See the Apache Version 2.0 License for specific language governing permissions
and limitations under the License.
***************************************************************************** */
function t(t,e,s,o){var i,r=arguments.length,a=r<3?e:null===o?o=Object.getOwnPropertyDescriptor(e,s):o;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)a=Reflect.decorate(t,e,s,o);else for(var n=t.length-1;n>=0;n--)(i=t[n])&&(a=(r<3?i(a):r>3?i(e,s,a):i(e,s))||a);return r>3&&a&&Object.defineProperty(e,s,a),a
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */}const e=new WeakMap,s=t=>"function"==typeof t&&e.has(t),o=void 0!==window.customElements&&void 0!==window.customElements.polyfillWrapFlushCallback,i=(t,e,s=null)=>{for(;e!==s;){const s=e.nextSibling;t.removeChild(e),e=s}},r={},a={},n=`{{lit-${String(Math.random()).slice(2)}}}`,c=`\x3c!--${n}--\x3e`,p=new RegExp(`${n}|${c}`),h="$lit$";class l{constructor(t,e){this.parts=[],this.element=e;const s=[],o=[],i=document.createTreeWalker(e.content,133,null,!1);let r=0,a=-1,c=0;const{strings:l,values:{length:u}}=t;for(;c<u;){const t=i.nextNode();if(null!==t){if(a++,1===t.nodeType){if(t.hasAttributes()){const e=t.attributes,{length:s}=e;let o=0;for(let t=0;t<s;t++)d(e[t].name,h)&&o++;for(;o-- >0;){const e=l[c],s=g.exec(e)[2],o=s.toLowerCase()+h,i=t.getAttribute(o);t.removeAttribute(o);const r=i.split(p);this.parts.push({type:"attribute",index:a,name:s,strings:r}),c+=r.length-1}}"TEMPLATE"===t.tagName&&(o.push(t),i.currentNode=t.content)}else if(3===t.nodeType){const e=t.data;if(e.indexOf(n)>=0){const o=t.parentNode,i=e.split(p),r=i.length-1;for(let e=0;e<r;e++){let s,r=i[e];if(""===r)s=m();else{const t=g.exec(r);null!==t&&d(t[2],h)&&(r=r.slice(0,t.index)+t[1]+t[2].slice(0,-h.length)+t[3]),s=document.createTextNode(r)}o.insertBefore(s,t),this.parts.push({type:"node",index:++a})}""===i[r]?(o.insertBefore(m(),t),s.push(t)):t.data=i[r],c+=r}}else if(8===t.nodeType)if(t.data===n){const e=t.parentNode;null!==t.previousSibling&&a!==r||(a++,e.insertBefore(m(),t)),r=a,this.parts.push({type:"node",index:a}),null===t.nextSibling?t.data="":(s.push(t),a--),c++}else{let e=-1;for(;-1!==(e=t.data.indexOf(n,e+1));)this.parts.push({type:"node",index:-1}),c++}}else i.currentNode=o.pop()}for(const t of s)t.parentNode.removeChild(t)}}const d=(t,e)=>{const s=t.length-e.length;return s>=0&&t.slice(s)===e},u=t=>-1!==t.index,m=()=>document.createComment(""),g=/([ \x09\x0a\x0c\x0d])([^\0-\x1F\x7F-\x9F "'>=/]+)([ \x09\x0a\x0c\x0d]*=[ \x09\x0a\x0c\x0d]*(?:[^ \x09\x0a\x0c\x0d"'`<>=]*|"[^"]*|'[^']*))$/;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
class y{constructor(t,e,s){this.__parts=[],this.template=t,this.processor=e,this.options=s}update(t){let e=0;for(const s of this.__parts)void 0!==s&&s.setValue(t[e]),e++;for(const t of this.__parts)void 0!==t&&t.commit()}_clone(){const t=o?this.template.element.content.cloneNode(!0):document.importNode(this.template.element.content,!0),e=[],s=this.template.parts,i=document.createTreeWalker(t,133,null,!1);let r,a=0,n=0,c=i.nextNode();for(;a<s.length;)if(r=s[a],u(r)){for(;n<r.index;)n++,"TEMPLATE"===c.nodeName&&(e.push(c),i.currentNode=c.content),null===(c=i.nextNode())&&(i.currentNode=e.pop(),c=i.nextNode());if("node"===r.type){const t=this.processor.handleTextExpression(this.options);t.insertAfterNode(c.previousSibling),this.__parts.push(t)}else this.__parts.push(...this.processor.handleAttributeExpressions(c,r.name,r.strings,this.options));a++}else this.__parts.push(void 0),a++;return o&&(document.adoptNode(t),customElements.upgrade(t)),t}}
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const v=` ${n} `;class f{constructor(t,e,s,o){this.strings=t,this.values=e,this.type=s,this.processor=o}getHTML(){const t=this.strings.length-1;let e="",s=!1;for(let o=0;o<t;o++){const t=this.strings[o],i=t.lastIndexOf("\x3c!--");s=(i>-1||s)&&-1===t.indexOf("--\x3e",i+1);const r=g.exec(t);e+=null===r?t+(s?v:c):t.substr(0,r.index)+r[1]+r[2]+h+r[3]+n}return e+=this.strings[t]}getTemplateElement(){const t=document.createElement("template");return t.innerHTML=this.getHTML(),t}}
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const _=t=>null===t||!("object"==typeof t||"function"==typeof t),b=t=>Array.isArray(t)||!(!t||!t[Symbol.iterator]);class w{constructor(t,e,s){this.dirty=!0,this.element=t,this.name=e,this.strings=s,this.parts=[];for(let t=0;t<s.length-1;t++)this.parts[t]=this._createPart()}_createPart(){return new $(this)}_getValue(){const t=this.strings,e=t.length-1;let s="";for(let o=0;o<e;o++){s+=t[o];const e=this.parts[o];if(void 0!==e){const t=e.value;if(_(t)||!b(t))s+="string"==typeof t?t:String(t);else for(const e of t)s+="string"==typeof e?e:String(e)}}return s+=t[e]}commit(){this.dirty&&(this.dirty=!1,this.element.setAttribute(this.name,this._getValue()))}}class ${constructor(t){this.value=void 0,this.committer=t}setValue(t){t===r||_(t)&&t===this.value||(this.value=t,s(t)||(this.committer.dirty=!0))}commit(){for(;s(this.value);){const t=this.value;this.value=r,t(this)}this.value!==r&&this.committer.commit()}}class x{constructor(t){this.value=void 0,this.__pendingValue=void 0,this.options=t}appendInto(t){this.startNode=t.appendChild(m()),this.endNode=t.appendChild(m())}insertAfterNode(t){this.startNode=t,this.endNode=t.nextSibling}appendIntoPart(t){t.__insert(this.startNode=m()),t.__insert(this.endNode=m())}insertAfterPart(t){t.__insert(this.startNode=m()),this.endNode=t.endNode,t.endNode=this.startNode}setValue(t){this.__pendingValue=t}commit(){for(;s(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=r,t(this)}const t=this.__pendingValue;t!==r&&(_(t)?t!==this.value&&this.__commitText(t):t instanceof f?this.__commitTemplateResult(t):t instanceof Node?this.__commitNode(t):b(t)?this.__commitIterable(t):t===a?(this.value=a,this.clear()):this.__commitText(t))}__insert(t){this.endNode.parentNode.insertBefore(t,this.endNode)}__commitNode(t){this.value!==t&&(this.clear(),this.__insert(t),this.value=t)}__commitText(t){const e=this.startNode.nextSibling,s="string"==typeof(t=null==t?"":t)?t:String(t);e===this.endNode.previousSibling&&3===e.nodeType?e.data=s:this.__commitNode(document.createTextNode(s)),this.value=t}__commitTemplateResult(t){const e=this.options.templateFactory(t);if(this.value instanceof y&&this.value.template===e)this.value.update(t.values);else{const s=new y(e,t.processor,this.options),o=s._clone();s.update(t.values),this.__commitNode(o),this.value=s}}__commitIterable(t){Array.isArray(this.value)||(this.value=[],this.clear());const e=this.value;let s,o=0;for(const i of t)void 0===(s=e[o])&&(s=new x(this.options),e.push(s),0===o?s.appendIntoPart(this):s.insertAfterPart(e[o-1])),s.setValue(i),s.commit(),o++;o<e.length&&(e.length=o,this.clear(s&&s.endNode))}clear(t=this.startNode){i(this.startNode.parentNode,t.nextSibling,this.endNode)}}class S{constructor(t,e,s){if(this.value=void 0,this.__pendingValue=void 0,2!==s.length||""!==s[0]||""!==s[1])throw new Error("Boolean attributes can only contain a single expression");this.element=t,this.name=e,this.strings=s}setValue(t){this.__pendingValue=t}commit(){for(;s(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=r,t(this)}if(this.__pendingValue===r)return;const t=!!this.__pendingValue;this.value!==t&&(t?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name),this.value=t),this.__pendingValue=r}}class k extends w{constructor(t,e,s){super(t,e,s),this.single=2===s.length&&""===s[0]&&""===s[1]}_createPart(){return new P(this)}_getValue(){return this.single?this.parts[0].value:super._getValue()}commit(){this.dirty&&(this.dirty=!1,this.element[this.name]=this._getValue())}}class P extends ${}let C=!1;try{const t={get capture(){return C=!0,!1}};window.addEventListener("test",t,t),window.removeEventListener("test",t,t)}catch(t){}class T{constructor(t,e,s){this.value=void 0,this.__pendingValue=void 0,this.element=t,this.eventName=e,this.eventContext=s,this.__boundHandleEvent=t=>this.handleEvent(t)}setValue(t){this.__pendingValue=t}commit(){for(;s(this.__pendingValue);){const t=this.__pendingValue;this.__pendingValue=r,t(this)}if(this.__pendingValue===r)return;const t=this.__pendingValue,e=this.value,o=null==t||null!=e&&(t.capture!==e.capture||t.once!==e.once||t.passive!==e.passive),i=null!=t&&(null==e||o);o&&this.element.removeEventListener(this.eventName,this.__boundHandleEvent,this.__options),i&&(this.__options=A(t),this.element.addEventListener(this.eventName,this.__boundHandleEvent,this.__options)),this.value=t,this.__pendingValue=r}handleEvent(t){"function"==typeof this.value?this.value.call(this.eventContext||this.element,t):this.value.handleEvent(t)}}const A=t=>t&&(C?{capture:t.capture,passive:t.passive,once:t.once}:t.capture);
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const E=new class{handleAttributeExpressions(t,e,s,o){const i=e[0];if("."===i){return new k(t,e.slice(1),s).parts}return"@"===i?[new T(t,e.slice(1),o.eventContext)]:"?"===i?[new S(t,e.slice(1),s)]:new w(t,e,s).parts}handleTextExpression(t){return new x(t)}};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */function z(t){let e=N.get(t.type);void 0===e&&(e={stringsArray:new WeakMap,keyString:new Map},N.set(t.type,e));let s=e.stringsArray.get(t.strings);if(void 0!==s)return s;const o=t.strings.join(n);return void 0===(s=e.keyString.get(o))&&(s=new l(t,t.getTemplateElement()),e.keyString.set(o,s)),e.stringsArray.set(t.strings,s),s}const N=new Map,R=new WeakMap;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
(window.litHtmlVersions||(window.litHtmlVersions=[])).push("1.1.2");const M=(t,...e)=>new f(t,e,"html",E),V=133;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */function U(t,e){const{element:{content:s},parts:o}=t,i=document.createTreeWalker(s,V,null,!1);let r=L(o),a=o[r],n=-1,c=0;const p=[];let h=null;for(;i.nextNode();){n++;const t=i.currentNode;for(t.previousSibling===h&&(h=null),e.has(t)&&(p.push(t),null===h&&(h=t)),null!==h&&c++;void 0!==a&&a.index===n;)a.index=null!==h?-1:a.index-c,a=o[r=L(o,r)]}p.forEach(t=>t.parentNode.removeChild(t))}const D=t=>{let e=11===t.nodeType?0:1;const s=document.createTreeWalker(t,V,null,!1);for(;s.nextNode();)e++;return e},L=(t,e=-1)=>{for(let s=e+1;s<t.length;s++){const e=t[s];if(u(e))return s}return-1};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const I=(t,e)=>`${t}--${e}`;let O=!0;void 0===window.ShadyCSS?O=!1:void 0===window.ShadyCSS.prepareTemplateDom&&(console.warn("Incompatible ShadyCSS version detected. Please update to at least @webcomponents/webcomponentsjs@2.0.2 and @webcomponents/shadycss@1.3.1."),O=!1);const q=t=>e=>{const s=I(e.type,t);let o=N.get(s);void 0===o&&(o={stringsArray:new WeakMap,keyString:new Map},N.set(s,o));let i=o.stringsArray.get(e.strings);if(void 0!==i)return i;const r=e.strings.join(n);if(void 0===(i=o.keyString.get(r))){const s=e.getTemplateElement();O&&window.ShadyCSS.prepareTemplateDom(s,t),i=new l(e,s),o.keyString.set(r,i)}return o.stringsArray.set(e.strings,i),i},j=["html","svg"],H=new Set,B=(t,e,s)=>{H.add(t);const o=s?s.element:document.createElement("template"),i=e.querySelectorAll("style"),{length:r}=i;if(0===r)return void window.ShadyCSS.prepareTemplateStyles(o,t);const a=document.createElement("style");for(let t=0;t<r;t++){const e=i[t];e.parentNode.removeChild(e),a.textContent+=e.textContent}(t=>{j.forEach(e=>{const s=N.get(I(e,t));void 0!==s&&s.keyString.forEach(t=>{const{element:{content:e}}=t,s=new Set;Array.from(e.querySelectorAll("style")).forEach(t=>{s.add(t)}),U(t,s)})})})(t);const n=o.content;s?function(t,e,s=null){const{element:{content:o},parts:i}=t;if(null==s)return void o.appendChild(e);const r=document.createTreeWalker(o,V,null,!1);let a=L(i),n=0,c=-1;for(;r.nextNode();){for(c++,r.currentNode===s&&(n=D(e),s.parentNode.insertBefore(e,s));-1!==a&&i[a].index===c;){if(n>0){for(;-1!==a;)i[a].index+=n,a=L(i,a);return}a=L(i,a)}}}(s,a,n.firstChild):n.insertBefore(a,n.firstChild),window.ShadyCSS.prepareTemplateStyles(o,t);const c=n.querySelector("style");if(window.ShadyCSS.nativeShadow&&null!==c)e.insertBefore(c.cloneNode(!0),e.firstChild);else if(s){n.insertBefore(a,n.firstChild);const t=new Set;t.add(a),U(s,t)}};window.JSCompiler_renameProperty=(t,e)=>t;const F={toAttribute(t,e){switch(e){case Boolean:return t?"":null;case Object:case Array:return null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){switch(e){case Boolean:return null!==t;case Number:return null===t?null:Number(t);case Object:case Array:return JSON.parse(t)}return t}},W=(t,e)=>e!==t&&(e==e||t==t),J={attribute:!0,type:String,converter:F,reflect:!1,hasChanged:W},G=Promise.resolve(!0),Y=1,K=4,Q=8,X=16,Z=32,tt="finalized";class et extends HTMLElement{constructor(){super(),this._updateState=0,this._instanceProperties=void 0,this._updatePromise=G,this._hasConnectedResolver=void 0,this._changedProperties=new Map,this._reflectingProperties=void 0,this.initialize()}static get observedAttributes(){this.finalize();const t=[];return this._classProperties.forEach((e,s)=>{const o=this._attributeNameForProperty(s,e);void 0!==o&&(this._attributeToPropertyMap.set(o,s),t.push(o))}),t}static _ensureClassProperties(){if(!this.hasOwnProperty(JSCompiler_renameProperty("_classProperties",this))){this._classProperties=new Map;const t=Object.getPrototypeOf(this)._classProperties;void 0!==t&&t.forEach((t,e)=>this._classProperties.set(e,t))}}static createProperty(t,e=J){if(this._ensureClassProperties(),this._classProperties.set(t,e),e.noAccessor||this.prototype.hasOwnProperty(t))return;const s="symbol"==typeof t?Symbol():`__${t}`;Object.defineProperty(this.prototype,t,{get(){return this[s]},set(e){const o=this[t];this[s]=e,this._requestUpdate(t,o)},configurable:!0,enumerable:!0})}static finalize(){const t=Object.getPrototypeOf(this);if(t.hasOwnProperty(tt)||t.finalize(),this[tt]=!0,this._ensureClassProperties(),this._attributeToPropertyMap=new Map,this.hasOwnProperty(JSCompiler_renameProperty("properties",this))){const t=this.properties,e=[...Object.getOwnPropertyNames(t),..."function"==typeof Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(t):[]];for(const s of e)this.createProperty(s,t[s])}}static _attributeNameForProperty(t,e){const s=e.attribute;return!1===s?void 0:"string"==typeof s?s:"string"==typeof t?t.toLowerCase():void 0}static _valueHasChanged(t,e,s=W){return s(t,e)}static _propertyValueFromAttribute(t,e){const s=e.type,o=e.converter||F,i="function"==typeof o?o:o.fromAttribute;return i?i(t,s):t}static _propertyValueToAttribute(t,e){if(void 0===e.reflect)return;const s=e.type,o=e.converter;return(o&&o.toAttribute||F.toAttribute)(t,s)}initialize(){this._saveInstanceProperties(),this._requestUpdate()}_saveInstanceProperties(){this.constructor._classProperties.forEach((t,e)=>{if(this.hasOwnProperty(e)){const t=this[e];delete this[e],this._instanceProperties||(this._instanceProperties=new Map),this._instanceProperties.set(e,t)}})}_applyInstanceProperties(){this._instanceProperties.forEach((t,e)=>this[e]=t),this._instanceProperties=void 0}connectedCallback(){this._updateState=this._updateState|Z,this._hasConnectedResolver&&(this._hasConnectedResolver(),this._hasConnectedResolver=void 0)}disconnectedCallback(){}attributeChangedCallback(t,e,s){e!==s&&this._attributeToProperty(t,s)}_propertyToAttribute(t,e,s=J){const o=this.constructor,i=o._attributeNameForProperty(t,s);if(void 0!==i){const t=o._propertyValueToAttribute(e,s);if(void 0===t)return;this._updateState=this._updateState|Q,null==t?this.removeAttribute(i):this.setAttribute(i,t),this._updateState=this._updateState&~Q}}_attributeToProperty(t,e){if(this._updateState&Q)return;const s=this.constructor,o=s._attributeToPropertyMap.get(t);if(void 0!==o){const t=s._classProperties.get(o)||J;this._updateState=this._updateState|X,this[o]=s._propertyValueFromAttribute(e,t),this._updateState=this._updateState&~X}}_requestUpdate(t,e){let s=!0;if(void 0!==t){const o=this.constructor,i=o._classProperties.get(t)||J;o._valueHasChanged(this[t],e,i.hasChanged)?(this._changedProperties.has(t)||this._changedProperties.set(t,e),!0!==i.reflect||this._updateState&X||(void 0===this._reflectingProperties&&(this._reflectingProperties=new Map),this._reflectingProperties.set(t,i))):s=!1}!this._hasRequestedUpdate&&s&&this._enqueueUpdate()}requestUpdate(t,e){return this._requestUpdate(t,e),this.updateComplete}async _enqueueUpdate(){let t,e;this._updateState=this._updateState|K;const s=this._updatePromise;this._updatePromise=new Promise((s,o)=>{t=s,e=o});try{await s}catch(t){}this._hasConnected||await new Promise(t=>this._hasConnectedResolver=t);try{const t=this.performUpdate();null!=t&&await t}catch(t){e(t)}t(!this._hasRequestedUpdate)}get _hasConnected(){return this._updateState&Z}get _hasRequestedUpdate(){return this._updateState&K}get hasUpdated(){return this._updateState&Y}performUpdate(){this._instanceProperties&&this._applyInstanceProperties();let t=!1;const e=this._changedProperties;try{(t=this.shouldUpdate(e))&&this.update(e)}catch(e){throw t=!1,e}finally{this._markUpdated()}t&&(this._updateState&Y||(this._updateState=this._updateState|Y,this.firstUpdated(e)),this.updated(e))}_markUpdated(){this._changedProperties=new Map,this._updateState=this._updateState&~K}get updateComplete(){return this._getUpdateComplete()}_getUpdateComplete(){return this._updatePromise}shouldUpdate(t){return!0}update(t){void 0!==this._reflectingProperties&&this._reflectingProperties.size>0&&(this._reflectingProperties.forEach((t,e)=>this._propertyToAttribute(e,this[e],t)),this._reflectingProperties=void 0)}updated(t){}firstUpdated(t){}}et[tt]=!0;
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const st=t=>e=>"function"==typeof e?((t,e)=>(window.customElements.define(t,e),e))(t,e):((t,e)=>{const{kind:s,elements:o}=e;return{kind:s,elements:o,finisher(e){window.customElements.define(t,e)}}})(t,e),ot=(t,e)=>"method"!==e.kind||!e.descriptor||"value"in e.descriptor?{kind:"field",key:Symbol(),placement:"own",descriptor:{},initializer(){"function"==typeof e.initializer&&(this[e.key]=e.initializer.call(this))},finisher(s){s.createProperty(e.key,t)}}:Object.assign({},e,{finisher(s){s.createProperty(e.key,t)}}),it=(t,e,s)=>{e.constructor.createProperty(s,t)};function rt(t){return(e,s)=>void 0!==s?it(t,e,s):ot(t,e)}
/**
@license
Copyright (c) 2019 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const at="adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,nt=Symbol();class ct{constructor(t,e){if(e!==nt)throw new Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t}get styleSheet(){return void 0===this._styleSheet&&(at?(this._styleSheet=new CSSStyleSheet,this._styleSheet.replaceSync(this.cssText)):this._styleSheet=null),this._styleSheet}toString(){return this.cssText}}const pt=(t,...e)=>{const s=e.reduce((e,s,o)=>e+(t=>{if(t instanceof ct)return t.cssText;if("number"==typeof t)return t;throw new Error(`Value passed to 'css' function must be a 'css' function result: ${t}. Use 'unsafeCSS' to pass non-literal values, but\n            take care to ensure page security.`)})(s)+t[o+1],t[0]);return new ct(s,nt)};
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
(window.litElementVersions||(window.litElementVersions=[])).push("2.2.1");const ht=t=>t.flat?t.flat(1/0):function t(e,s=[]){for(let o=0,i=e.length;o<i;o++){const i=e[o];Array.isArray(i)?t(i,s):s.push(i)}return s}(t);class lt extends et{static finalize(){super.finalize.call(this),this._styles=this.hasOwnProperty(JSCompiler_renameProperty("styles",this))?this._getUniqueStyles():this._styles||[]}static _getUniqueStyles(){const t=this.styles,e=[];if(Array.isArray(t)){ht(t).reduceRight((t,e)=>(t.add(e),t),new Set).forEach(t=>e.unshift(t))}else t&&e.push(t);return e}initialize(){super.initialize(),this.renderRoot=this.createRenderRoot(),window.ShadowRoot&&this.renderRoot instanceof window.ShadowRoot&&this.adoptStyles()}createRenderRoot(){return this.attachShadow({mode:"open"})}adoptStyles(){const t=this.constructor._styles;0!==t.length&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow?at?this.renderRoot.adoptedStyleSheets=t.map(t=>t.styleSheet):this._needsShimAdoptedStyleSheets=!0:window.ShadyCSS.ScopingShim.prepareAdoptedCssText(t.map(t=>t.cssText),this.localName))}connectedCallback(){super.connectedCallback(),this.hasUpdated&&void 0!==window.ShadyCSS&&window.ShadyCSS.styleElement(this)}update(t){super.update(t);const e=this.render();e instanceof f&&this.constructor.render(e,this.renderRoot,{scopeName:this.localName,eventContext:this}),this._needsShimAdoptedStyleSheets&&(this._needsShimAdoptedStyleSheets=!1,this.constructor._styles.forEach(t=>{const e=document.createElement("style");e.textContent=t.cssText,this.renderRoot.appendChild(e)}))}render(){}}function dt(){if(customElements.get("hui-view"))return!0;const t=document.createElement("partial-panel-resolver");t.hass=document.querySelector("home-assistant").hass,t.route={path:"/lovelace/"};try{document.querySelector("home-assistant").appendChild(t).catch(t=>{})}catch(e){document.querySelector("home-assistant").removeChild(t)}return!!customElements.get("hui-view")}lt.finalized=!0,lt.render=(t,e,s)=>{if(!s||"object"!=typeof s||!s.scopeName)throw new Error("The `scopeName` option is required.");const o=s.scopeName,r=R.has(e),a=O&&11===e.nodeType&&!!e.host,n=a&&!H.has(o),c=n?document.createDocumentFragment():e;if(((t,e,s)=>{let o=R.get(e);void 0===o&&(i(e,e.firstChild),R.set(e,o=new x(Object.assign({templateFactory:z},s))),o.appendInto(e)),o.setValue(t),o.commit()})(t,c,Object.assign({templateFactory:q(o)},s)),n){const t=R.get(c);R.delete(c);const s=t.value instanceof y?t.value.template:void 0;B(o,c,s),i(e,e.firstChild),e.appendChild(c),R.set(e,t)}!r&&a&&window.ShadyCSS.styleElement(e.host)};const ut=(t,e)=>{history.replaceState(null,"",e)};const mt=[pt`
    :host {
      @apply --paper-font-body1;
    }

    app-header-layout,
    ha-app-layout {
      background-color: var(--primary-background-color);
    }

    app-header, app-toolbar {
      background-color: var(--primary-color);
      font-weight: 400;
      color: var(--text-primary-color, white);
    }

    app-toolbar ha-menu-button + [main-title],
    app-toolbar ha-paper-icon-button-arrow-prev + [main-title],
    app-toolbar paper-icon-button + [main-title] {
      margin-left: 24px;
    }

    button.link {
      background: none;
      color: inherit;
      border: none;
      padding: 0;
      font: inherit;
      text-align: left;
      text-decoration: underline;
      cursor: pointer;
    }

    .card-actions a {
      text-decoration: none;
    }

    .card-actions .warning {
      --mdc-theme-primary: var(--google-red-500);
    }
`,pt`
    :host {
      font-family: var(--paper-font-body1_-_font-family); -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing); font-size: var(--paper-font-body1_-_font-size); font-weight: var(--paper-font-body1_-_font-weight); line-height: var(--paper-font-body1_-_line-height);
    }

    app-header-layout, ha-app-layout {
      background-color: var(--primary-background-color);
    }

    app-header, app-toolbar, paper-tabs {
      background-color: var(--primary-color);
      font-weight: 400;
      text-transform: uppercase;
      color: var(--text-primary-color, white);
    }

    paper-tabs {
      --paper-tabs-selection-bar-color: #fff;
      margin-left: 12px;
    }

    app-toolbar ha-menu-button + [main-title], app-toolbar ha-paper-icon-button-arrow-prev + [main-title], app-toolbar paper-icon-button + [main-title] {
      margin-left: 24px;
    }
`,pt`
    :root {
        font-family: var(--paper-font-body1_-_font-family);
        -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
        font-size: var(--paper-font-body1_-_font-size);
        font-weight: var(--paper-font-body1_-_font-weight);
        line-height: var(--paper-font-body1_-_line-height);
    }
    a {
        text-decoration: none;
        color: var(--dark-primary-color);
    }
    h1 {
        font-family: var(--paper-font-title_-_font-family);
        -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
        white-space: var(--paper-font-title_-_white-space);
        overflow: var(--paper-font-title_-_overflow);
        text-overflow: var(--paper-font-title_-_text-overflow);
        font-size: var(--paper-font-title_-_font-size);
        font-weight: var(--paper-font-title_-_font-weight);
        line-height: var(--paper-font-title_-_line-height);
        @apply --paper-font-title;
    }
    .title {
        margin-bottom: 16px;
        padding-top: 4px;
        color: var(--primary-text-color);
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
    }
    .addition {
        color: var(--secondary-text-color);
        position: relative;
        height: auto;
        line-height: 1.2em;
        text-overflow: ellipsis;
        overflow: hidden;
    }
    paper-card {
        cursor: pointer;
    }
    ha-card {
      margin: 8px;
    }
    ha-icon {
        height: 24px;
        width: 24px;
        margin-right: 16px;
        float: left;
        color: var(--primary-text-color);
    }
    ha-icon.installed {
        color: var(--hacs-status-installed, #126e15);
    }
    ha-icon.pending-upgrade {
        color: var(--hacs-status-pending-update, #ffab40);
    }
    ha-icon.pending-restart {
        color: var(--hacs-status-pending-restart, var(--google-red-500));
    }
    ha-icon.not-loaded {
        color: var(--hacs-status-not-loaded, var(--google-red-500));
    }
    ha-icon.new {
        color: var(--hacs-badge-color, var(--primary-color));
      }
`,pt`

`];let gt=class extends lt{render(){return M`
        <a href="#">
            <ha-icon
                title="Help"
                class="float"
                icon="mdi:help-circle-outline"
                @click=${this.openHelp}>
            </ha-icon>
        </a>
        `}openHelp(){var t=window.location.pathname.split("/")[2];console.log(t),"integration"===t&&(t="stores"),"plugin"===t&&(t="stores"),"appdaemon"===t&&(t="stores"),"python_script"===t&&(t="stores"),"theme"===t&&(t="stores"),window.open(`https://hacs.xyz/docs/navigation/${t}`,"Help","noreferrer")}static get styles(){return[mt,pt`
            .float{
                position: fixed;
                width: 60px;
                height:60px;
                bottom: 40px;
                right: 40px;
                border-radius: 50px;
                text-align: center;
                color: var(--accent-color);
                background-color: var(--paper-card-background-color, var(--primary-background-color));
            }
        `]}};function yt(t,e,s){if("yaml"===s.lovelace_mode)return!0;if(void 0!==e){var o=!1,i=`/community_plugin/${t.full_name.split("/")[1]}/${t.file_name}`;return void 0!==e.resources&&e.resources.forEach(t=>{o||t.url===i&&(o=!0)}),o}return!0}gt=t([st("hacs-help-button")],gt);class vt extends lt{static get styles(){return mt}}t([rt()],vt.prototype,"hass",void 0),t([rt()],vt.prototype,"repository",void 0),t([rt()],vt.prototype,"status",void 0);let ft=class extends vt{render(){return M`
            <mwc-button @click=${this.ExecuteAction}>
                ${this.hass.localize("component.hacs.store.clear_new")}
            </mwc-button>
        `}ExecuteAction(){var t={type:"hacs/settings",action:"clear_new",category:this.category};this.hass.connection.sendMessage(t)}};t([rt()],ft.prototype,"category",void 0),ft=t([st("hacs-button-clear-new")],ft);let _t=class extends lt{constructor(){super(...arguments),this.repository_view=!1,this.SearchTerm=""}render(){if("repository"===this.panel)return M`
      <hacs-panel-repository
        .hass=${this.hass}
        .route=${this.route}
        .status=${this.status}
        .configuration=${this.configuration}
        .repositories=${this.repositories}
        .repository=${this.repository}
        .lovelaceconfig=${this.lovelaceconfig}
      >
      </hacs-panel-repository>`;{const o=this.panel;var t=[];const i=this.configuration;this.SearchTerm=localStorage.getItem("hacs-search");var e=this.SearchTerm,s=this.repositories.filter((function(s){if("installed"!==o){if("172733314"===s.id)return!1;if(s.hide)return!1;if("ALL"!==i.country&&void 0!==s.country&&i.country!==s.country)return!1}else if(s.installed)return!0;return s.category===o&&(""!==e?!!s.name.toLowerCase().includes(e)||(!!s.description.toLowerCase().includes(e)||(!!s.full_name.toLowerCase().includes(e)||(!!String(s.authors).toLowerCase().includes(e)||!!String(s.topics).toLowerCase().includes(e)))):(s.new&&t.push(s),!0))}));return M`
      <paper-input
        class="search-bar search-bar-${this.panel}"
        type="text"
        id="Search"
        @input=${this.DoSearch}
        placeholder="  ${this.hass.localize("component.hacs.store.placeholder_search")}."
        autofocus
        .value=${this.SearchTerm}
      >
        ${this.SearchTerm.length>0?M`
          <ha-icon slot="suffix" icon="mdi:close" @click="${this.clearSearch}"></ha-icon>
        `:""}
      </paper-input>

    ${0!==t.length?M`
    <div class="card-group">
      <h1>${this.hass.localize("component.hacs.store.new_repositories")}</h1>
      ${t.sort((t,e)=>t.name>e.name?1:-1).map(t=>M`
          ${"Table"!==this.configuration.frontend_mode?M`
          <paper-card @click="${this.ShowRepository}" .RepoID="${t.id}">
          <div class="card-content">
            <div>
              <ha-icon
                icon="mdi:new-box"
                class="${this.StatusAndDescription(t).status}"
                title="${this.StatusAndDescription(t).description}"
                >
              </ha-icon>
              <div>
                <div class="title">${t.name}</div>
                <div class="addition">${t.description}</div>
              </div>
            </div>
          </div>
          </paper-card>

        `:M`

        <paper-item .RepoID=${t.id} @click="${this.ShowRepository}">
          <div class="icon">
            <ha-icon
              icon="mdi:new-box"
              class="${this.StatusAndDescription(t).status}"
              title="${this.StatusAndDescription(t).description}"
          </ha-icon>
          </div>
          <paper-item-body two-line>
            <div>${t.name}</div>
            <div class="addition">${t.description}</div>
          </paper-item-body>
        </paper-item>
        `}
      `)}
    </div>
    <div class="card-group">
      <hacs-button-clear-new .hass=${this.hass} .category=${o}></hacs-button-clear-new>
    </div>
    <hr>
    `:""}

    <div class="card-group">
    ${s.sort((t,e)=>t.name>e.name?1:-1).map(t=>M`

      ${"Table"!==this.configuration.frontend_mode?M`
        <paper-card @click="${this.ShowRepository}" .RepoID="${t.id}">
        <div class="card-content">
          <div>
            <ha-icon
              icon=${t.new?"mdi:new-box":"mdi:cube"}
              class="${this.StatusAndDescription(t).status}"
              title="${this.StatusAndDescription(t).description}"
              >
            </ha-icon>
            <div>
              <div class="title">${t.name}</div>
              <div class="addition">${t.description}</div>
            </div>
          </div>
        </div>
        </paper-card>

      `:M`

      <paper-item .RepoID=${t.id} @click="${this.ShowRepository}">
        <div class="icon">
          <ha-icon
            icon=${t.new?"mdi:new-box":"mdi:cube"}
            class="${this.StatusAndDescription(t).status}"
            title="${this.StatusAndDescription(t).description}"
        </ha-icon>
        </div>
        <paper-item-body two-line>
          <div>${t.name}</div>
          <div class="addition">${t.description}</div>
        </paper-item-body>
      </paper-item>
      `}


      `)}
    </div>
    <script>
    var objDiv = document.getElementById("191563578");
    objDiv.scrollTop = objDiv.scrollHeight;
    console.log("done")
    </script>
          `}}StatusAndDescription(t){var e=t.status,s=t.status_description;return t.installed&&!this.status.background_task&&("plugin"!==t.category||yt(t,this.lovelaceconfig,this.status)||(e="not-loaded",s="Not loaded in lovelace")),{status:e,description:s}}DoSearch(t){this.SearchTerm=t.composedPath()[0].value.toLowerCase(),localStorage.setItem("hacs-search",this.SearchTerm)}clearSearch(){this.SearchTerm="",localStorage.setItem("hacs-search",this.SearchTerm)}ShowRepository(t){var e;t.composedPath().forEach(t=>{t.RepoID&&(e=t.RepoID)}),this.panel="repository",this.repository=e,this.repository_view=!0,this.requestUpdate(),ut(0,`/${this._rootPath}/repository/${e}`)}get _rootPath(){return"hacs_dev"===window.location.pathname.split("/")[1]?"hacs_dev":"hacs"}static get styles(){return[mt,pt`
      hr {
        width: 95%
      }
      paper-item {
        margin-bottom: 24px;
      }
      paper-item:hover {
        outline: 0;
        background: var(--table-row-alternative-background-color);
    }
      .search-bar {
        display: block;
        width: 92%;
        margin-left: 3.4%;
        margin-top: 2%;
        background-color: var(--primary-background-color);
        color: var(--primary-text-color);
        line-height: 32px;
        border-color: var(--dark-primary-color);
        border-width: inherit;
        border-bottom-width: thin;
      }

      .search-bar-installed, .search-bar-settings {
        display: none;
      }

      .card-group {
          margin-top: 24px;
          width: 95%;
          margin-left: 2.5%;
        }

        .card-group .title {
          color: var(--primary-text-color);
          margin-bottom: 12px;
        }

        .card-group .description {
          font-size: 0.5em;
          font-weight: 500;
          margin-top: 4px;
        }

        .card-group paper-card {
          --card-group-columns: 3;
          width: calc((100% - 12px * var(--card-group-columns)) / var(--card-group-columns));
          margin: 4px;
          vertical-align: top;
          height: 136px;
        }

        @media screen and (max-width: 1200px) and (min-width: 601px) {
          .card-group paper-card {
            --card-group-columns: 2;
          }
        }

        @media screen and (max-width: 600px) and (min-width: 0) {
          .card-group paper-card {
            width: 100%;
            margin: 4px 0;
          }
          .content {
            padding: 0;
          }
        }
    `]}};t([rt()],_t.prototype,"hass",void 0),t([rt()],_t.prototype,"repositories",void 0),t([rt()],_t.prototype,"configuration",void 0),t([rt()],_t.prototype,"route",void 0),t([rt()],_t.prototype,"panel",void 0),t([rt()],_t.prototype,"status",void 0),t([rt()],_t.prototype,"repository_view",void 0),t([rt()],_t.prototype,"repository",void 0),t([rt()],_t.prototype,"SearchTerm",void 0),t([rt()],_t.prototype,"lovelaceconfig",void 0),_t=t([st("hacs-panel")],_t);
/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */
const bt=new WeakMap,wt=(t=>(...s)=>{const o=t(...s);return e.set(o,!0),o})(t=>e=>{if(!(e instanceof x))throw new Error("unsafeHTML can only be used in text bindings");const s=bt.get(e);if(void 0!==s&&_(t)&&t===s.value&&e.value===s.fragment)return;const o=document.createElement("template");o.innerHTML=t;const i=document.importNode(o.content,!0);e.setValue(i),bt.set(e,{value:t,fragment:i})});function $t(t,e,s,o){let i;i=void 0!==o?{type:"hacs/repository/data",action:s,repository:e,data:o}:{type:"hacs/repository",action:s,repository:e},t.connection.sendMessage(i)}let xt=class extends lt{render(){return"0"===String(this.authors.length)?M``:M`
            <div class="autors">
                <p><b>${this.hass.localize("component.hacs.repository.authors")}: </b>

                    ${this.authors.map(t=>M`
                        <a href="https://github.com/${t.replace("@","")}"
                                target="_blank" rel='noreferrer'>
                            ${t.replace("@","")}
                        </a>`)}

                </p>
            </div>
            `}static get styles(){return[mt,pt`
            .autors {

            }
        `]}};t([rt()],xt.prototype,"hass",void 0),t([rt()],xt.prototype,"authors",void 0),xt=t([st("hacs-authors")],xt);let St=class extends lt{render(){return M`
        <paper-menu-button no-animations horizontal-align="right" role="group" aria-haspopup="true" vertical-align="top" aria-disabled="false">
        <paper-icon-button icon="hass:dots-vertical" slot="dropdown-trigger" role="button"></paper-icon-button>
            <paper-listbox slot="dropdown-content" role="listbox" tabindex="0">


                <paper-item @click=${this.RepositoryReload}>
                    ${this.hass.localize("component.hacs.repository.update_information")}
                </paper-item>


                ${"version"===this.repository.version_or_commit?M`
                <paper-item @click=${this.RepositoryBeta}>
                    ${this.repository.beta?this.hass.localize("component.hacs.repository.hide_beta"):this.hass.localize("component.hacs.repository.show_beta")}
                </paper-item>`:""}


                ${this.repository.custom||this.repository.installed?"":M`
                <paper-item @click=${this.RepositoryHide}>
                    ${this.hass.localize("component.hacs.repository.hide")}
                </paper-item>`}


                <a href="https://github.com/${this.repository.full_name}" rel='noreferrer' target="_blank">
                <paper-item>
                    <ha-icon class="link-icon" icon="mdi:open-in-new"></ha-icon>
                    ${this.hass.localize("component.hacs.repository.open_issue")}
                </paper-item>
                </a>


                <a href="https://github.com/hacs/default/issues/new?assignees=ludeeus&labels=flag&template=flag.md&title=${this.repository.full_name}" rel='noreferrer' target="_blank">
                <paper-item>
                    <ha-icon class="link-icon" icon="mdi:open-in-new"></ha-icon>
                    ${this.hass.localize("component.hacs.repository.flag_this")}
                </paper-item>
                </a>


            </paper-listbox>
        </paper-menu-button>
        `}static get styles(){return[mt,pt`
        paper-dropdown-menu {
            width: 250px;
            margin-top: -24px;

          }
          paper-menu-button {
            float: right;
            top: -65px;
          }
        `]}RepositoryReload(){$t(this.hass,this.repository.id,"set_state","other"),$t(this.hass,this.repository.id,"update")}RepositoryBeta(){$t(this.hass,this.repository.id,"set_state","other"),this.repository.beta?$t(this.hass,this.repository.id,"hide_beta"):$t(this.hass,this.repository.id,"show_beta")}RepositoryHide(){$t(this.hass,this.repository.id,"set_state","other"),this.repository.hide?$t(this.hass,this.repository.id,"unhide"):$t(this.hass,this.repository.id,"hide")}};t([rt()],St.prototype,"hass",void 0),t([rt()],St.prototype,"repository",void 0),St=t([st("hacs-repository-menu")],St);let kt=class extends vt{render(){if("plugin"!=this.repository.category)return M``;if(!this.repository.installed)return M``;const t=this.repository.local_path.split("/");return M`
            <a href="/community_plugin/${t.pop()}/${this.repository.file_name}" target="_blank">
                <mwc-button>
                    ${this.hass.localize("component.hacs.repository.open_plugin")}
                </mwc-button>
            </a>
        `}};kt=t([st("hacs-button-open-plugin")],kt);let Pt=class extends vt{render(){return M`
            <a href="https://github.com/${this.repository.full_name}" rel='noreferrer' target="_blank">
                <mwc-button>
                    ${this.hass.localize("component.hacs.repository.repository")}
                </mwc-button>
            </a>
        `}};Pt=t([st("hacs-button-open-repository")],Pt);let Ct=class extends vt{render(){if(!this.repository.installed)return M``;const t=this.hass.localize("component.hacs.repository.uninstall");return this.status.background_task?M`
                <mwc-button disabled>
                    ${t}
                </mwc-button>
            `:M`
            <mwc-button @click=${this.RepositoryUnInstall}>
                ${"uninstalling"==this.repository.state?M`<paper-spinner active></paper-spinner>`:M`${t}`}
            </mwc-button>
        `}RepositoryUnInstall(){window.confirm(this.hass.localize("component.hacs.confirm.uninstall","item",this.repository.name))&&this.ExecuteAction()}ExecuteAction(){$t(this.hass,this.repository.id,"set_state","uninstalling"),$t(this.hass,this.repository.id,"uninstall")}};Ct=t([st("hacs-button-uninstall")],Ct);let Tt=class extends vt{constructor(){super(...arguments),this.pathExists=!1}firstUpdated(){this.hass.connection.sendMessagePromise({type:"hacs/check_path",path:this.repository.local_path}).then(t=>{this.pathExists=t.exist},t=>{console.error("[hacs/check_path] Message failed!",t)})}render(){const t=this.hass.localize(`component.hacs.repository.${this.repository.main_action.toLowerCase()}`);return this.status.background_task?M`
                <mwc-button disabled>
                    ${t}
                </mwc-button>
            `:M`
            <mwc-button
            @click=${this.RepositoryInstall}>
                ${"installing"==this.repository.state?M`<paper-spinner active></paper-spinner>`:M`${t}`}
            </mwc-button>
        `}RepositoryInstall(){this.repository.can_install?this.pathExists&&!this.repository.installed?window.confirm(this.hass.localize("component.hacs.confirm.exsist","item",this.repository.local_path)+"\n"+this.hass.localize("component.hacs.confirm.overwrite")+"\n"+this.hass.localize("component.hacs.confirm.continue"))&&this.ExecuteAction():this.ExecuteAction():window.alert(`This repository version requires Home Assistant version ${this.repository.homeassistant}`)}ExecuteAction(){$t(this.hass,this.repository.id,"set_state","installing"),$t(this.hass,this.repository.id,"install")}};t([rt()],Tt.prototype,"pathExists",void 0),Tt=t([st("hacs-button-main-action")],Tt);let At=class extends vt{render(){if(!this.repository.pending_upgrade)return M``;var t=`https://github.com/${this.repository.full_name}/releases`;return"commit"===this.repository.version_or_commit&&(t=`https://github.com/${this.repository.full_name}/compare/${this.repository.installed_version}...${this.repository.available_version}`),M`
        <a href="${t}" rel='noreferrer' target="_blank">
          <mwc-button>
          ${this.hass.localize("component.hacs.repository.changelog")}
          </mwc-button>
        </a>
        `}RepositoryInstall(){$t(this.hass,this.repository.id,"set_state","installing"),$t(this.hass,this.repository.id,"uninstall")}};At=t([st("hacs-button-changelog")],At);let Et=class extends lt{render(){return M`
            <div class="lovelace-hint">
                <p class="example-title">${this.hass.localize("component.hacs.repository.lovelace_instruction")}:</p>
                <pre id="LovelaceExample" class="yaml">
- url: /community_plugin/${this.repository.full_name.split("/")[1]}/${this.repository.file_name}
  type: ${void 0!==this.repository.javascript_type?M`${this.repository.javascript_type}`:M`${this.hass.localize("component.hacs.repository.lovelace_no_js_type")}`}</pre>

                <paper-icon-button
                    title="${this.hass.localize("component.hacs.repository.lovelace_copy_example")}"
                    icon="mdi:content-copy"
                    @click="${this.CopyToLovelaceExampleToClipboard}"
                    role="button"
                ></paper-icon-button>
            </div>
            `}CopyToLovelaceExampleToClipboard(t){var e=t.composedPath()[4].children[0].children[1].innerText;document.addEventListener("copy",t=>{t.clipboardData.setData("text/plain",e),t.preventDefault(),document.removeEventListener("copy",null)}),document.execCommand("copy")}static get styles(){return[mt,pt`
            .lovelace-hint {

            }
            .example-title {
                margin-block-end: 0em;
            }
            .yaml {
                font-family: monospace, monospace;
                font-size: 1em;
                border-style: solid;
                border-width: thin;
                margin: 0;
                overflow: auto;
                display: inline-flex;
                width: calc(100% - 46px);
                white-space: pre-wrap;
            }

        `]}};t([rt()],Et.prototype,"hass",void 0),t([rt()],Et.prototype,"configuration",void 0),t([rt()],Et.prototype,"repository",void 0),Et=t([st("hacs-lovelace-hint")],Et);let zt=class extends lt{render(){return M`
            <div class="repository-note">
            <p>${this.hass.localize("component.hacs.repository.note_installed")} '${this.repository.local_path}'

            ${"appdaemon"===this.repository.category?M`,
            ${this.hass.localize(`component.hacs.repository.note_${this.repository.category}`)}`:""}

            ${"integration"===this.repository.category?M`,
            ${this.hass.localize(`component.hacs.repository.note_${this.repository.category}`)}`:""}

            ${"plugin"===this.repository.category?M`,
            ${this.hass.localize(`component.hacs.repository.note_${this.repository.category}`)}`:""}

            .</p>

                ${"plugin"===this.repository.category?M`
                    <hacs-lovelace-hint
                        .hass=${this.hass}
                        .configuration=${this.configuration}
                        .repository=${this.repository}
                    ></hacs-lovelace-hint>
                `:""}
            </div>
            `}static get styles(){return[mt,pt`
            .repository-note {
                border-top: 1px solid var(--primary-text-color);
            }
            p {
                font-style: italic;
            }
        `]}};t([rt()],zt.prototype,"hass",void 0),t([rt()],zt.prototype,"configuration",void 0),t([rt()],zt.prototype,"repository",void 0),zt=t([st("hacs-repository-note")],zt);let Nt=class extends vt{render(){return this.configuration.experimental&&this.repository.installed?null===this.repository.javascript_type?M``:M`
            <mwc-button @click=${this.RepositoryAddToLovelace}>
                Add to Lovelace
            </mwc-button>
        `:M``}RepositoryAddToLovelace(){window.confirm("Do you want to add this to your lovelace resources?")&&this.hass.connection.sendMessagePromise({type:"lovelace/config",force:!1}).then(t=>{var e=t;const s={type:this.repository.javascript_type,url:`/community_plugin/${this.repository.full_name.split("/")[1]}/${this.repository.file_name}`};e.resources?e.resources.push(s):e.resources=[s],this.hass.callWS({type:"lovelace/config/save",config:e})},t=>{console.error(t)})}};t([rt()],Nt.prototype,"lovelaceconfig",void 0),t([rt()],Nt.prototype,"configuration",void 0),Nt=t([st("hacs-button-add-to-lovelace")],Nt);let Rt=class extends lt{render(){if(!this.repository.installed)return M``;var t="",e="",s="";if("pending-restart"==this.repository.status)s="alert",e="Restart pending",t="\n            You need to restart Home Assistant.\n            ";else if("plugin"==this.repository.category){if(void 0!==this.lovelaceconfig)yt(this.repository,this.lovelaceconfig,this.status)||(s="warning",e="Not Loaded",t="\n                    This plugin is not added to your Lovelace resources.\n                    ")}return 0==t.length?M``:"plugin"!==this.repository.category?M`
            <ha-card header="${e}" class="${s}">
                <div class="card-content">
                    ${t}
                </div>
            </ha-card>
            `:M`
            <ha-card header="${e}" class="${s}">
                <div class="card-content">
                    ${t}
                </div>
                <div class="card-actions">
                    <hacs-button-add-to-lovelace
                        .hass=${this.hass}
                        .configuration=${this.configuration}
                        .repository=${this.repository}
                        .lovelaceconfig=${this.lovelaceconfig}>
                    </hacs-button-add-to-lovelace>
                </div>
            </ha-card>
        `}static get styles(){return[mt,pt`
            ha-card {
                width: 90%;
                margin-left: 5%;
            }
            .alert {
                background-color: var(--hacs-status-pending-restart);
                color: var(--text-primary-color);
            }
            .warning {
                background-color: var(--hacs-status-pending-update)
                color: var(--text-primary-color);
            }
            .info {

            }
        `]}};t([rt()],Rt.prototype,"hass",void 0),t([rt()],Rt.prototype,"repository",void 0),t([rt()],Rt.prototype,"status",void 0),t([rt()],Rt.prototype,"configuration",void 0),t([rt()],Rt.prototype,"lovelaceconfig",void 0),Rt=t([st("hacs-repository-banner-note")],Rt);let Mt=class extends lt{constructor(){super(...arguments),this.repository_view=!1}firstUpdated(){this.repo.updated_info||($t(this.hass,this.repo.id,"set_state","other"),$t(this.hass,this.repo.id,"update"))}render(){if(void 0===this.repository)return M`
      <hacs-panel
        .hass=${this.hass}
        .configuration=${this.configuration}
        .repositories=${this.repositories}
        .panel=${this.panel}
        .route=${this.route}
        .status=${this.status}
        .repository_view=${this.repository_view}
        .repository=${this.repository}
        .lovelaceconfig=${this.lovelaceconfig}
      >
      </hacs-panel>
      `;var t=this.repository,e=this.repositories.filter((function(e){return e.id===t}));if(this.repo=e[0],this.repo.installed)var s=this.hass.localize("component.hacs.common.installed");else{if("appdaemon"===this.repo.category)var o="appdaemon_apps";else o=`${this.repo.category}s`;s=this.hass.localize(`component.hacs.common.${o}`)}return M`

    <div class="getBack">
      <mwc-button @click=${this.GoBackToStore} title="${s}">
      <ha-icon  icon="mdi:arrow-left"></ha-icon>
        ${this.hass.localize("component.hacs.repository.back_to")}
        ${s}
      </mwc-button>
      ${"other"==this.repo.state?M`<paper-spinner active class="loader"></paper-spinner>`:""}
    </div>

    <hacs-repository-banner-note
      .hass=${this.hass}
      .status=${this.status}
      .repository=${this.repo}
      .lovelaceconfig=${this.lovelaceconfig}
      .configuration=${this.configuration}>
    </hacs-repository-banner-note>

    <ha-card header="${this.repo.name}">
      <hacs-repository-menu .hass=${this.hass} .repository=${this.repo}></hacs-repository-menu>


      <div class="card-content">

        <div class="description addition">
          ${this.repo.description}
        </div>

        <div class="information">
          ${this.repo.installed?M`
          <div class="version installed">
            <b>${this.hass.localize("component.hacs.repository.installed")}: </b> ${this.repo.installed_version}
          </div>
          `:""}

        ${"0"===String(this.repo.releases.length)?M`
              <div class="version-available">
                  <b>${this.hass.localize("component.hacs.repository.available")}: </b> ${this.repo.available_version}
              </div>
          `:M`
              <div class="version-available">
                  <paper-dropdown-menu @value-changed="${this.SetVersion}"
                    label="${this.hass.localize("component.hacs.repository.available")}:
                     (${this.hass.localize("component.hacs.repository.newest")}: ${this.repo.releases[0]})">
                      <paper-listbox slot="dropdown-content" selected="-1">
                          ${this.repo.releases.map(t=>M`<paper-item>${t}</paper-item>`)}
                          ${"hacs/integration"!==this.repo.full_name?M`
                          <paper-item>${this.repo.default_branch}</paper-item>
                          `:""}
                      </paper-listbox>
                  </paper-dropdown-menu>
              </div>`}
        </div>
        <hacs-authors .hass=${this.hass} .authors=${this.repo.authors}></hacs-authors>
      </div>


      <div class="card-actions">
        <hacs-button-main-action .hass=${this.hass} .repository=${this.repo} .status=${this.status}></hacs-button-main-action>
        <hacs-button-changelog .hass=${this.hass} .repository=${this.repo}></hacs-button-changelog>
        <hacs-button-open-repository .hass=${this.hass} .repository=${this.repo}></hacs-button-open-repository>
        ${"plugin"===this.repo.category?M`
          <hacs-button-open-plugin .hass=${this.hass} .repository=${this.repo}></hacs-button-open-plugin>
        `:""}
        <hacs-button-uninstall class="right" .hass=${this.hass} .repository=${this.repo} .status=${this.status}></hacs-button-uninstall>
      </div>

    </ha-card>

    <ha-card class="additional">
      <div class="card-content">
        <div class="more_info">
          ${wt(this.repo.additional_info)}
        </div>
      <hacs-repository-note
        .hass=${this.hass}
        .configuration=${this.configuration}
        .repository=${this.repo}
      ></hacs-repository-note>
      </div>
    </ha-card>
          `}SetVersion(t){t.detail.value.length>0&&($t(this.hass,this.repo.id,"set_state","other"),$t(this.hass,this.repo.id,"set_version",t.detail.value))}GoBackToStore(){this.repository=void 0,this.repo.installed?this.panel="installed":this.panel=this.repo.category,ut(0,`/${this._rootPath}/${this.panel}`),this.requestUpdate()}get _rootPath(){return"hacs_dev"===window.location.pathname.split("/")[1]?"hacs_dev":"hacs"}static get styles(){return[mt,pt`
      paper-spinner.loader {
        position: absolute;
        top: 20%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 99;
        width: 300px;
        height: 300px;
     }
     paper-dropdown-menu {
        width: 80%;
     }
      .description {
        font-style: italic;
        padding-bottom: 16px;
      }
      .version {
        padding-bottom: 8px;
      }
      .options {
        float: right;
        width: 40%;
      }
      .information {
        width: 60%;
      }
      .additional {
        margin-bottom: 108px;
      }
      .getBack {
        margin-top: 8px;
        margin-bottom: 4px;
        margin-left: 5%;
      }
      .right {
        float: right;
      }
      .loading {
        text-align: center;
        width: 100%;
      }
      ha-card {
        width: 90%;
        margin-left: 5%;
      }
      .link-icon {
        color: var(--dark-primary-color);
        margin-right: 8px;
      }

    `]}};t([rt()],Mt.prototype,"hass",void 0),t([rt()],Mt.prototype,"repositories",void 0),t([rt()],Mt.prototype,"configuration",void 0),t([rt()],Mt.prototype,"repository",void 0),t([rt()],Mt.prototype,"panel",void 0),t([rt()],Mt.prototype,"route",void 0),t([rt()],Mt.prototype,"status",void 0),t([rt()],Mt.prototype,"repository_view",void 0),t([rt()],Mt.prototype,"repo",void 0),t([rt()],Mt.prototype,"lovelaceconfig",void 0),Mt=t([st("hacs-panel-repository")],Mt);let Vt=class extends lt{updated(){this.SaveSpinner=!1}Delete(t){if(window.confirm(this.hass.localize("component.hacs.confirm.delete","item",t.composedPath()[3].innerText))){var e=t.composedPath()[4].repoID;$t(this.hass,e,"delete")}}Save(t){this.SaveSpinner=!0;var e=t.composedPath()[1].children[1].selectedItem.category,s=t.composedPath()[1].children[0].value;$t(this.hass,s,"add",e)}render(){return this.custom=this.repositories.filter((function(t){return!!t.custom})),M`
        <ha-card header="${this.hass.localize("component.hacs.settings.custom_repositories")}">
            <div class="card-content">
            <div class="custom-repositories-list">

            ${this.custom.sort((t,e)=>t.full_name>e.full_name?1:-1).map(t=>M`
                <div class="row" .repoID=${t.id}>
                    <paper-item>
                        ${t.full_name}
                        <ha-icon
                        title="${this.hass.localize("component.hacs.settings.delete")}"
                        class="listicon" icon="mdi:delete"
                        @click=${this.Delete}
                        ></ha-icon>
                    </paper-item>
                </div>
                `)}
            </div>
            </div>

            <div class="card-actions">
                <paper-input class="inputfield" placeholder=${this.hass.localize("component.hacs.settings.add_custom_repository")} type="text"></paper-input>
                <paper-dropdown-menu class="category"
                label="${this.hass.localize("component.hacs.settings.category")}">
                  <paper-listbox slot="dropdown-content" selected="-1">
                      ${this.configuration.categories.map(t=>M`
                      <paper-item .category=${t}>
                        ${this.hass.localize(`component.hacs.common.${t}`)}
                      </paper-item>`)}
                  </paper-listbox>
              </paper-dropdown-menu>

                ${this.SaveSpinner?M`<paper-spinner active class="loading"></paper-spinner>`:M`
                <ha-icon title="${this.hass.localize("component.hacs.settings.save")}"
                    icon="mdi:content-save" class="saveicon"
                    @click=${this.Save}>
                </ha-icon>
                `}
            </div>

        </ha-card>
            `}static get styles(){return[mt,pt`
            ha-card {
                width: 90%;
                margin-left: 5%;
            }
            .custom-repositories {

            }

            .add-repository {

            }
            .inputfield {
                width: 60%;
            }
            .category {
                position: absolute;
                width: 30%;
                right: 54px;
                bottom: 5px;
            }
            .saveicon {
                color: var(--primary-color);
                position: absolute;
                right: 0;
                bottom: 24px;
            }
            .listicon {
                color: var(--primary-color);
                right: 0px;
                position: absolute;
            }
            .loading {
                position: absolute;
                right: 10px;
                bottom: 22px;
            }
        `]}};t([rt()],Vt.prototype,"hass",void 0),t([rt()],Vt.prototype,"repositories",void 0),t([rt()],Vt.prototype,"custom",void 0),t([rt()],Vt.prototype,"status",void 0),t([rt()],Vt.prototype,"configuration",void 0),t([rt()],Vt.prototype,"SaveSpinner",void 0),Vt=t([st("hacs-custom-repositories")],Vt);let Ut=class extends lt{UnHide(t){var e=t.composedPath()[4].repoID;$t(this.hass,e,"unhide")}render(){return this._hidden=this.repositories.filter((function(t){return t.hide})),0===this._hidden.length?M``:M`
        <ha-card header="${this.hass.localize("component.hacs.settings.hidden_repositories").toUpperCase()}">
            <div class="card-content">
            <div class="custom-repositories-list">

            ${this._hidden.sort((t,e)=>t.full_name>e.full_name?1:-1).map(t=>M`
                <div class="row" .repoID=${t.id}>
                    <paper-item>
                    <ha-icon
                    title="${this.hass.localize("component.hacs.settings.unhide")}"
                    class="listicon" icon="mdi:restore"
                    @click=${this.UnHide}
                    ></ha-icon>
                        ${t.full_name}
                    </paper-item>
                </div>
                `)}
            </div>
            </div>
        </ha-card>
            `}static get styles(){return[mt,pt`
            ha-card {
                width: 90%;
                margin-left: 5%;
            }
            .listicon {
                color: var(--primary-color);
                left: 0px;
            }
        `]}};t([rt()],Ut.prototype,"hass",void 0),t([rt()],Ut.prototype,"repositories",void 0),t([rt()],Ut.prototype,"_hidden",void 0),Ut=t([st("hacs-hidden-repositories")],Ut);let Dt=class extends lt{render(){return this.status.reloading_data,M`

    <ha-card header="${this.hass.localize("component.hacs.config.title")}">
      <div class="card-content">
        <p><b>${this.hass.localize("component.hacs.common.version")}:</b> ${this.configuration.version}</p>
        <p><b>${this.hass.localize("component.hacs.common.repositories")}:</b> ${this.repositories.length}</p>
        <div class="version-available">
        <ha-switch
          .checked=${"Table"===this.configuration.frontend_mode}
          @change=${this.SetFeStyle}
        >Table view</ha-switch>
    </div>
      </div>
      <div class="card-actions">

      ${this.status.reloading_data?M`
          <mwc-button raised disabled>
            <paper-spinner active></paper-spinner>
          </mwc-button>
      `:M`
          <mwc-button raised @click=${this.ReloadData}>
            ${this.hass.localize("component.hacs.settings.reload_data")}
          </mwc-button>
      `}


      ${this.status.upgrading_all?M`
          <mwc-button raised disabled>
            <paper-spinner active></paper-spinner>
          </mwc-button>
      `:M`
          <mwc-button raised @click=${this.UpgradeAll}>
            ${this.hass.localize("component.hacs.settings.upgrade_all")}
          </mwc-button>
      `}

      <a href="https://github.com/hacs/integration" target="_blank" rel="noreferrer">
        <mwc-button raised>
          ${this.hass.localize("component.hacs.settings.hacs_repo")}
        </mwc-button>
      </a>

      <a href="https://github.com/hacs/integration/issues" target="_blank" rel="noreferrer">
        <mwc-button raised>
          ${this.hass.localize("component.hacs.repository.open_issue")}
        </mwc-button>
      </a>
      </div>
    </ha-card>
    <hacs-custom-repositories
      .hass=${this.hass}
      .status=${this.status}
      .configuration=${this.configuration}
      .repositories=${this.repositories}
    >
    </hacs-custom-repositories>
    <hacs-hidden-repositories
    .hass=${this.hass}
    .status=${this.status}
    .configuration=${this.configuration}
    .repositories=${this.repositories}
    >
    </hacs-hidden-repositories
          `}SetFeStyle(){this.hass.connection.sendMessage({type:"hacs/settings",action:`set_fe_${"Table"!==this.configuration.frontend_mode?"table":"grid"}`})}ReloadData(){this.hass.connection.sendMessage({type:"hacs/settings",action:"reload_data"})}UpgradeAll(){var t=[];if(this.repositories.forEach(e=>{e.pending_upgrade&&t.push(e)}),t.length>0){var e="This will upgrade all of these repositores, make sure that you have read the release notes for all of them before proceeding.";if(e+="\n",e+="\n",t.forEach(t=>{e+=`${t.name} ${t.installed_version} -> ${t.available_version}\n`}),!window.confirm(e))return;this.hass.connection.sendMessage({type:"hacs/settings",action:"upgrade_all"})}else window.alert("No upgrades pending")}static get styles(){return[mt,pt`
    ha-card {
      width: 90%;
      margin-left: 5%;
    }
    mwc-button {
      margin: 0 8px 0 8px;
    }
    `]}};t([rt()],Dt.prototype,"hass",void 0),t([rt()],Dt.prototype,"repositories",void 0),t([rt()],Dt.prototype,"configuration",void 0),t([rt()],Dt.prototype,"status",void 0),Dt=t([st("hacs-panel-settings")],Dt);let Lt=class extends lt{render(){return this.status.background_task?M`
            <paper-progress indeterminate></paper-progress>
        `:M``}static get styles(){return[mt,pt`
            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--accent-color);
            }
        `]}};t([rt()],Lt.prototype,"status",void 0),Lt=t([st("hacs-progressbar")],Lt);let It=class extends lt{constructor(){super(...arguments),this.error=void 0}clearError(){this.error=void 0}firstUpdated(){this.hass.connection.subscribeEvents(t=>this.error=t.data,"hacs/error")}render(){if(void 0===this.error)return M``;var t=this.error.message,e="";return"add_repository"===this.error.action&&(e="Could not add this repository, make sure it is compliant with HACS."),M`
            <ha-card header="An error ocoured while prosessing" class="alert">
                <div class="card-content">
                    ${t} </br>
                    ${e}
                </div>
            <div class="card-actions">
                <mwc-button raised @click=${this.clearError}>
                    Acknowledge
                </mwc-button>
            ${"add_repository"===this.error.action?M`
            <a href="https://hacs.xyz/docs/publish/start" rel='noreferrer' target="_blank">
                <mwc-button raised>
                    Documentation
                </mwc-button>
            </a>
            `:""}
            </div>
            </ha-card>
            `}static get styles(){return[mt,pt`
            ha-card {
                width: 90%;
                margin-left: 5%;
            }
            .alert {
                background-color: var(--hacs-status-pending-restart);
                color: var(--text-primary-color);
            }
        `]}};t([rt()],It.prototype,"hass",void 0),t([rt()],It.prototype,"error",void 0),It=t([st("hacs-error")],It);let Ot=class extends lt{async Acknowledge(t){var e=t.composedPath()[3].repository;const s=await this.hass.connection.sendMessagePromise({type:"hacs/critical",repository:e});this.critical=s.data}render(){if(void 0===this.critical)return M``;var t=[];return this.critical.forEach(e=>{e.acknowledged||t.push(e)}),M`
            ${t.map(t=>M`
            <ha-card header="Critical Issue!" class="alert">
                <div class="card-content">
                    The repository "${t.repository}" has been flagged as a critical repository.</br>
                    The repository has now been uninstalled and removed.</br>
                    For information about how and why these are handled, see
                    <a href="https://hacs.xyz/docs/developer/maintaner#critical-repositories">
                        https://hacs.xyz/docs/developer/maintaner#critical-repositories
                    </a></br>
                    As a result of this Home Assistant was also restarted.</br></br>

                    <b>Reason: </b>${t.reason}
                </div>
                <div class="card-actions">
                    <mwc-button @click=${this.Acknowledge} .repository=${t.repository}>
                        Acknowledge
                    </mwc-button>
                    <a href="${t.link}" rel='noreferrer' target="_blank">
                        <mwc-button>
                            More information about this incident
                        </mwc-button>
                    </a>
                </div>
            </ha-card>`)}
            `}static get styles(){return[mt,pt`
            ha-card {
                width: 90%;
                margin-left: 5%;
            }
            .alert {
                background-color: var(--hacs-status-pending-restart);
                color: var(--text-primary-color);
            }
        `]}};t([rt()],Ot.prototype,"hass",void 0),t([rt()],Ot.prototype,"critical",void 0),Ot=t([st("hacs-critical")],Ot);let qt=class extends lt{constructor(){super(...arguments),this.repository_view=!1}getRepositories(){this.hass.connection.sendMessagePromise({type:"hacs/repositories"}).then(t=>{this.repositories=t,this.requestUpdate()},t=>{console.error("[hacs/repositories] Message failed!",t)})}getConfig(){this.hass.connection.sendMessagePromise({type:"hacs/config"}).then(t=>{this.configuration=t,this.requestUpdate()},t=>{console.error("[hacs/config] Message failed!",t)})}getCritical(){this.hass.connection.sendMessagePromise({type:"hacs/get_critical"}).then(t=>{this.critical=t,this.requestUpdate()},t=>{console.error("[hacs/get_critical] Message failed!",t)})}getStatus(){this.hass.connection.sendMessagePromise({type:"hacs/status"}).then(t=>{this.status=t,this.requestUpdate()},t=>{console.error("[hacs/status] Message failed!",t)})}getLovelaceConfig(){this.hass.connection.sendMessagePromise({type:"lovelace/config",force:!1}).then(t=>{this.lovelaceconfig=t},()=>{this.lovelaceconfig=void 0})}firstUpdated(){localStorage.setItem("hacs-search",""),this.panel=this._page,this.getRepositories(),this.getConfig(),this.getStatus(),this.getCritical(),this.getLovelaceConfig(),/repository\//i.test(this.panel)?(this.repository_view=!0,this.repository=this.panel.split("/")[1]):this.repository_view=!1,dt(),this.hass.connection.sendMessagePromise({type:"hacs/repository"}),this.hass.connection.sendMessagePromise({type:"hacs/config"}),this.hass.connection.sendMessagePromise({type:"hacs/status"}),this.hass.connection.subscribeEvents(()=>this.getRepositories(),"hacs/repository"),this.hass.connection.subscribeEvents(()=>this.getConfig(),"hacs/config"),this.hass.connection.subscribeEvents(()=>this.getStatus(),"hacs/status"),this.hass.connection.subscribeEvents(t=>this._reload(t),"hacs/reload"),this.hass.connection.subscribeEvents(()=>this.getLovelaceConfig(),"lovelace_updated")}_reload(t){window.location.reload(t.data.force)}render(){if(""===this.panel&&(ut(0,`/${this._rootPath}/installed`),this.panel="installed"),void 0===this.repositories||void 0===this.configuration||void 0===this.status)return M`<paper-spinner active class="loader"></paper-spinner>`;/repository\//i.test(this.panel)?(this.repository_view=!0,this.repository=this.panel.split("/")[1],this.panel=this.panel.split("/")[0]):this.repository_view=!1;const t=this.panel;return M`
    <app-header-layout has-scrolling-region>
      <app-header slot="header" fixed>
        <app-toolbar>
        <ha-menu-button .hass="${this.hass}" .narrow="${this.narrow}"></ha-menu-button>
          <div main-title>Home Assistant Community Store
          ${"hacs_dev"===this._rootPath?M`(DEVELOPMENT)`:""}
          </div>
        </app-toolbar>
      <paper-tabs scrollable attr-for-selected="page-name" .selected=${t} @iron-activate=${this.handlePageSelected}>

        <paper-tab page-name="installed">
          ${this.hass.localize("component.hacs.common.installed")}
        </paper-tab>

        <paper-tab page-name="integration">
          ${this.hass.localize("component.hacs.common.integrations")}
        </paper-tab>

        <paper-tab page-name="plugin">
          ${this.hass.localize("component.hacs.common.plugins")}
        </paper-tab>

        ${this.configuration.appdaemon?M`<paper-tab page-name="appdaemon">
            ${this.hass.localize("component.hacs.common.appdaemon_apps")}
        </paper-tab>`:""}

        ${this.configuration.python_script?M`<paper-tab page-name="python_script">
            ${this.hass.localize("component.hacs.common.python_scripts")}
        </paper-tab>`:""}

        ${this.configuration.theme?M`<paper-tab page-name="theme">
            ${this.hass.localize("component.hacs.common.themes")}
        </paper-tab>`:""}

        <paper-tab page-name="settings">
          ${this.hass.localize("component.hacs.common.settings")}
        </paper-tab>
      </paper-tabs>
    </app-header>

    <hacs-progressbar .status=${this.status}></hacs-progressbar>

    <hacs-critical .hass=${this.hass} .critical=${this.critical}></hacs-critical>
    <hacs-error .hass=${this.hass}></hacs-error>

    ${"settings"!==this.panel?M`
      <hacs-panel
        .hass=${this.hass}
        .configuration=${this.configuration}
        .repositories=${this.repositories}
        .panel=${this.panel}
        .route=${this.route}
        .status=${this.status}
        .repository_view=${this.repository_view}
        .repository=${this.repository}
        .lovelaceconfig=${this.lovelaceconfig}
      >
      </hacs-panel>`:M`
      <hacs-panel-settings
        .hass=${this.hass}
        .status=${this.status}
        .configuration=${this.configuration}
        .repositories=${this.repositories}>
      </hacs-panel-settings>`}
      <hacs-help-button></hacs-help-button>
    </app-header-layout>`}handlePageSelected(t){this.repository_view=!1;const e=t.detail.item.getAttribute("page-name");this.panel=e,this.requestUpdate(),e!==this._page&&ut(0,`/${this._rootPath}/${e}`),function(t,e){const s=e,o=Math.random(),i=Date.now(),r=s.scrollTop,a=0-r;t._currentAnimationId=o,function e(){const n=Date.now()-i;var c;n>200?s.scrollTop=0:t._currentAnimationId===o&&(s.scrollTop=(c=n,-a*(c/=200)*(c-2)+r),requestAnimationFrame(e.bind(t)))}.call(t)}(this,this.shadowRoot.querySelector("app-header-layout").header.scrollTarget)}get _page(){return null===this.route.path.substr(1)?"installed":this.route.path.substr(1)}get _rootPath(){return"hacs_dev"===window.location.pathname.split("/")[1]?"hacs_dev":"hacs"}static get styles(){return[mt,pt`
    paper-spinner.loader {
      position: absolute;
      top: 20%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 99;
      width: 300px;
      height: 300px;
   }
    `]}};t([rt()],qt.prototype,"hass",void 0),t([rt()],qt.prototype,"repositories",void 0),t([rt()],qt.prototype,"configuration",void 0),t([rt()],qt.prototype,"status",void 0),t([rt()],qt.prototype,"route",void 0),t([rt()],qt.prototype,"critical",void 0),t([rt()],qt.prototype,"narrow",void 0),t([rt()],qt.prototype,"panel",void 0),t([rt()],qt.prototype,"repository",void 0),t([rt()],qt.prototype,"repository_view",void 0),t([rt()],qt.prototype,"lovelaceconfig",void 0),qt=t([st("hacs-frontend")],qt);
