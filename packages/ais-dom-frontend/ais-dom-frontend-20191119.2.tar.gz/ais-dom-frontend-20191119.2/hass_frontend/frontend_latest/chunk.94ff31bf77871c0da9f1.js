(self.webpackJsonp=self.webpackJsonp||[]).push([[105],{174:function(e,t,i){"use strict";var r=i(8);t.a=Object(r.a)(e=>(class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},181:function(e,t,i){"use strict";i.d(t,"a",function(){return n});var r=i(8),o=i(15);const n=Object(r.a)(e=>(class extends e{fire(e,t,i){return i=i||{},Object(o.a)(i.node||this,e,t,i)}}))},204:function(e,t,i){"use strict";var r=i(197);t.a=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):e=>r.a.format(e,"haDateTime")},205:function(e,t,i){"use strict";var r=i(4),o=i(30);i(95);customElements.define("ha-config-section",class extends o.a{static get template(){return r.a`
      <style include="iron-flex ha-style">
        .content {
          padding: 28px 20px 0;
          max-width: 1040px;
          margin: 0 auto;
        }

        .header {
          @apply --paper-font-display1;
          opacity: var(--dark-primary-opacity);
        }

        .together {
          margin-top: 32px;
        }

        .intro {
          @apply --paper-font-subhead;
          width: 100%;
          max-width: 400px;
          margin-right: 40px;
          opacity: var(--dark-primary-opacity);
        }

        .panel {
          margin-top: -24px;
        }

        .panel ::slotted(*) {
          margin-top: 24px;
          display: block;
        }

        .narrow.content {
          max-width: 640px;
        }
        .narrow .together {
          margin-top: 20px;
        }
        .narrow .header {
          @apply --paper-font-headline;
        }
        .narrow .intro {
          font-size: 14px;
          padding-bottom: 20px;
          margin-right: 0;
          max-width: 500px;
        }
      </style>
      <div class$="[[computeContentClasses(isWide)]]">
        <div class="header"><slot name="header"></slot></div>
        <div class$="[[computeClasses(isWide)]]">
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},240:function(e,t,i){"use strict";i(86),i(187);var r=i(4),o=i(30);customElements.define("ha-progress-button",class extends o.a{static get template(){return r.a`
      <style>
        .container {
          position: relative;
          display: inline-block;
        }

        mwc-button {
          transition: all 1s;
        }

        .success mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-green-500);
          transition: none;
        }

        .error mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-red-500);
          transition: none;
        }

        .progress {
          @apply --layout;
          @apply --layout-center-center;
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
        }
      </style>
      <div class="container" id="container">
        <mwc-button
          id="button"
          disabled="[[computeDisabled(disabled, progress)]]"
          on-click="buttonTapped"
        >
          <slot></slot>
        </mwc-button>
        <template is="dom-if" if="[[progress]]">
          <div class="progress"><paper-spinner active=""></paper-spinner></div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},progress:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1}}}tempClass(e){var t=this.$.container.classList;t.add(e),setTimeout(()=>{t.remove(e)},1e3)}ready(){super.ready(),this.addEventListener("click",e=>this.buttonTapped(e))}buttonTapped(e){this.progress&&e.stopPropagation()}actionSuccess(){this.tempClass("success")}actionError(){this.tempClass("error")}computeDisabled(e,t){return e||t}})},276:function(e,t,i){"use strict";var r=i(8),o=i(99);t.a=Object(r.a)(e=>(class extends e{navigate(...e){Object(o.a)(this,...e)}}))},397:function(e,t,i){"use strict";i.d(t,"a",function(){return o});var r=i(48);const o=(e,t)=>Object(r.a)(e,{message:t.localize("ui.common.successfully_saved")})},400:function(e,t,i){"use strict";var r=i(0),o=(i(240),i(15));customElements.define("ha-call-api-button",class extends r.a{render(){return r.f`
      <ha-progress-button
        .progress="${this.progress}"
        @click="${this._buttonTapped}"
        ?disabled="${this.disabled}"
        ><slot></slot
      ></ha-progress-button>
    `}constructor(){super(),this.method="POST",this.data={},this.disabled=!1,this.progress=!1}static get properties(){return{hass:{},progress:Boolean,path:String,method:String,data:{},disabled:Boolean}}get progressButton(){return this.renderRoot.querySelector("ha-progress-button")}async _buttonTapped(){this.progress=!0;const e={method:this.method,path:this.path,data:this.data};try{const i=await this.hass.callApi(this.method,this.path,this.data);this.progress=!1,this.progressButton.actionSuccess(),e.success=!0,e.response=i}catch(t){this.progress=!1,this.progressButton.actionError(),e.success=!1,e.response=t}Object(o.a)(this,"hass-api-called",e)}})},518:function(e,t,i){"use strict";i.d(t,"a",function(){return r}),i.d(t,"b",function(){return o});const r=e=>e.callWS({type:"cloud/alexa/entities"}),o=e=>e.callWS({type:"cloud/alexa/sync"})},771:function(e,t,i){"use strict";i.r(t);i(86),i(182);var r=i(4),o=i(30),n=(i(176),i(400),i(150),i(95),i(205),i(0)),a=(i(142),i(187),i(194),i(517)),s=i(322),c=i(15);function l(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t,i){return(m="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function g(e){return(g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let y=function(e,t,i,r){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!u(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=h(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var a=t(function(e){o.initializeInstanceElements(e,s.elements)},i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(p(n.descriptor)||p(o.descriptor)){if(u(n)||u(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(u(n)){if(u(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(a.d.map(l)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}(null,function(e,t){class r extends t{constructor(){super(),e(this),this._progress=[]}}return{F:r,d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_cloudHooks",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_localHooks",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_progress",value:void 0},{kind:"method",key:"connectedCallback",value:function(){m(g(r.prototype),"connectedCallback",this).call(this),this._fetchData()}},{kind:"method",key:"render",value:function(){return n.f`
      ${this.renderStyle()}
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.webhooks.title")}
      >
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.info")}
          ${this._renderBody()}

          <div class="footer">
            <a href="https://www.nabucasa.com/config/webhooks" target="_blank">
              ${this.hass.localize("ui.panel.config.cloud.account.webhooks.link_learn_more")}
            </a>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"updated",value:function(e){m(g(r.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&this.cloudStatus&&(this._cloudHooks=this.cloudStatus.prefs.cloudhooks||{})}},{kind:"method",key:"_renderBody",value:function(){return this.cloudStatus&&this._localHooks&&this._cloudHooks?0===this._localHooks.length?n.f`
        <div class="body-text">
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet")}
          <a href="/config/integrations"
            >${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet_link_integration")}</a
          >
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet2")}
          <a href="/config/automation/new"
            >${this.hass.localize("ui.panel.config.cloud.account.webhooks.no_hooks_yet_link_automation")}</a
          >.
        </div>
      `:this._localHooks.map(e=>n.f`
        <div class="webhook" .entry="${e}">
          <paper-item-body two-line>
            <div>
              ${e.name}
              ${e.domain===e.name.toLowerCase()?"":` (${e.domain})`}
            </div>
            <div secondary>${e.webhook_id}</div>
          </paper-item-body>
          ${this._progress.includes(e.webhook_id)?n.f`
                <div class="progress">
                  <paper-spinner active></paper-spinner>
                </div>
              `:this._cloudHooks[e.webhook_id]?n.f`
                <mwc-button @click="${this._handleManageButton}">
                  ${this.hass.localize("ui.panel.config.cloud.account.webhooks.manage")}
                </mwc-button>
              `:n.f`
                <ha-switch @click="${this._enableWebhook}"></ha-switch>
              `}
        </div>
      `):n.f`
        <div class="body-text">
          ${this.hass.localize("ui.panel.config.cloud.account.webhooks.loading")}
        </div>
      `}},{kind:"method",key:"_showDialog",value:function(e){const t=this._localHooks.find(t=>t.webhook_id===e),r=this._cloudHooks[e];var o,n;o=this,n={webhook:t,cloudhook:r,disableHook:()=>this._disableWebhook(e)},Object(c.a)(o,"show-dialog",{dialogTag:"dialog-manage-cloudhook",dialogImport:()=>Promise.all([i.e(1),i.e(29)]).then(i.bind(null,754)),dialogParams:n})}},{kind:"method",key:"_handleManageButton",value:function(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}},{kind:"method",key:"_enableWebhook",value:async function(e){const t=e.currentTarget.parentElement.entry;let i;this._progress=[...this._progress,t.webhook_id];try{i=await Object(s.d)(this.hass,t.webhook_id)}catch(r){return void alert(r.message)}finally{this._progress=this._progress.filter(e=>e!==t.webhook_id)}this._cloudHooks=Object.assign({},this._cloudHooks,{[t.webhook_id]:i}),0===this._progress.length&&this._showDialog(t.webhook_id)}},{kind:"method",key:"_disableWebhook",value:async function(e){this._progress=[...this._progress,e];try{await Object(s.e)(this.hass,e)}catch(i){return void alert(`${this.hass.localize("ui.panel.config.cloud.account.webhooks.disable_hook_error_msg")} ${i.message}`)}finally{this._progress=this._progress.filter(t=>t!==e)}const t=function(e,t){if(null==e)return{};var i,r,o={},n=Object.keys(e);for(r=0;r<n.length;r++)i=n[r],t.indexOf(i)>=0||(o[i]=e[i]);return o}(this._cloudHooks,[e].map(f));this._cloudHooks=t}},{kind:"method",key:"_fetchData",value:async function(){this._localHooks=this.hass.config.components.includes("webhook")?await Object(a.a)(this.hass):[]}},{kind:"method",key:"renderStyle",value:function(){return n.f`
      <style>
        .body-text {
          padding: 8px 0;
        }
        .webhook {
          display: flex;
          padding: 4px 0;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding-top: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}}]}},n.a);customElements.define("cloud-webhooks",y);var v=i(518);function b(e){var t,i=x(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function w(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function k(e){return e.decorators&&e.decorators.length}function _(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function E(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function x(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let z=function(e,t,i,r){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!k(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=x(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=E(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=E(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var a=t(function(e){o.initializeInstanceElements(e,s.elements)},i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(_(n.descriptor)||_(o.descriptor)){if(k(n)||k(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(k(n)){if(k(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}w(n,o)}else t.push(n)}return t}(a.d.map(b)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"_syncing",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return n.f``;const{alexa_enabled:e,alexa_report_state:t}=this.cloudStatus.prefs;return n.f`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.alexa.title")}
      >
        <div class="switch">
          <ha-switch
            .checked=${e}
            @change=${this._enabledToggleChanged}
          ></ha-switch>
        </div>
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.alexa.info")}
          <ul>
            <li>
              <a
                href="https://skills-store.amazon.com/deeplink/dp/B0772J1QKB?deviceType=app"
                target="_blank"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.alexa.enable_ha_skill")}
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/amazon_alexa/"
                target="_blank"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.alexa.config_documentation")}
              </a>
            </li>
          </ul>
          ${e?n.f`
                <div class="state-reporting">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.alexa.enable_state_reporting")}
                  </h3>
                  <div class="state-reporting-switch">
                    <ha-switch
                      .checked=${t}
                      @change=${this._reportToggleChanged}
                    ></ha-switch>
                  </div>
                </div>
                <p>
                  ${this.hass.localize("ui.panel.config.cloud.account.alexa.info_state_reporting")}
                </p>
              `:""}
        </div>
        <div class="card-actions">
          <mwc-button @click=${this._handleSync} .disabled=${this._syncing}>
            ${this.hass.localize("ui.panel.config.cloud.account.alexa.sync_entities")}
          </mwc-button>
          <div class="spacer"></div>
          <a href="/config/cloud/alexa">
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.alexa.manage_entities")}</mwc-button
            >
          </a>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_handleSync",value:async function(){this._syncing=!0;try{await Object(v.b)(this.hass)}catch(e){alert(`${this.hass.localize("ui.panel.config.cloud.account.alexa.sync_entities_error")} ${e.body.message}`)}finally{this._syncing=!1}}},{kind:"method",key:"_enabledToggleChanged",value:async function(e){const t=e.target;try{await Object(s.k)(this.hass,{alexa_enabled:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(i){t.checked=!t.checked}}},{kind:"method",key:"_reportToggleChanged",value:async function(e){const t=e.target;try{await Object(s.k)(this.hass,{alexa_report_state:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(i){alert(`${this.hass.localize("ui.panel.config.cloud.account.alexa.state_reporting_error","enable_disable",this.hass.localize(t.checked?"ui.panel.config.cloud.account.alexa.enable":"ui.panel.config.cloud.account.alexa.disable"))} ${i.message}`),t.checked=!t.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
      .state-reporting {
        display: flex;
        margin-top: 1.5em;
      }
      .state-reporting + p {
        margin-top: 0.5em;
      }
      .state-reporting h3 {
        flex-grow: 1;
        margin: 0;
      }
      .state-reporting-switch {
        margin-top: 0.25em;
        margin-right: 7px;
        margin-left: 0.5em;
      }
    `}}]}},n.a);customElements.define("cloud-alexa-pref",z);var P=i(397);function O(e){var t,i=T(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function S(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function j(e){return e.decorators&&e.decorators.length}function D(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function C(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function T(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let $=function(e,t,i,r){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!j(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=T(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=C(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=C(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var a=t(function(e){o.initializeInstanceElements(e,s.elements)},i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(D(n.descriptor)||D(o.descriptor)){if(j(n)||j(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(j(n)){if(j(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}S(n,o)}else t.push(n)}return t}(a.d.map(O)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return n.f``;const{google_enabled:e,google_report_state:t,google_secure_devices_pin:i}=this.cloudStatus.prefs;return n.f`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.google.title")}
      >
        <div class="switch">
          <ha-switch
            id="google_enabled"
            .checked="${e}"
            @change="${this._enableToggleChanged}"
          ></ha-switch>
        </div>
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.google.info")}
          <ul>
            <li>
              <a
                href="https://assistant.google.com/services/a/uid/00000091fd5fb875?hl=en-US"
                target="_blank"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.google.enable_ha_skill")}
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/google_assistant/"
                target="_blank"
              >
                ${this.hass.localize("ui.panel.config.cloud.account.google.config_documentation")}
              </a>
            </li>
          </ul>
          ${e?n.f`
                <div class="state-reporting">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.google.enable_state_reporting")}
                  </h3>
                  <div class="state-reporting-switch">
                    <ha-switch
                      .checked=${t}
                      @change=${this._reportToggleChanged}
                    ></ha-switch>
                  </div>
                </div>
                <p>
                  ${this.hass.localize("ui.panel.config.cloud.account.google.info_state_reporting")}
                </p>
                <div class="secure_devices">
                  <h3>
                    ${this.hass.localize("ui.panel.config.cloud.account.google.security_devices")}
                  </h3>
                  ${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_info")}
                  <paper-input
                    label="${this.hass.localize("ui.panel.config.cloud.account.google.devices_pin")}"
                    id="google_secure_devices_pin"
                    placeholder="${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_hint")}"
                    .value=${i||""}
                    @change="${this._pinChanged}"
                  ></paper-input>
                </div>
              `:""}
        </div>
        <div class="card-actions">
          <ha-call-api-button
            .hass="${this.hass}"
            .disabled="${!e}"
            path="cloud/google_actions/sync"
          >
            ${this.hass.localize("ui.panel.config.cloud.account.google.sync_entities")}
          </ha-call-api-button>
          <div class="spacer"></div>
          <a href="/config/cloud/google-assistant">
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.google.manage_entities")}</mwc-button
            >
          </a>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_enableToggleChanged",value:async function(e){const t=e.target;try{await Object(s.k)(this.hass,{[t.id]:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(i){t.checked=!t.checked}}},{kind:"method",key:"_reportToggleChanged",value:async function(e){const t=e.target;try{await Object(s.k)(this.hass,{google_report_state:t.checked}),Object(c.a)(this,"ha-refresh-cloud-status")}catch(i){alert(`Unable to ${t.checked?"enable":"disable"} report state. ${i.message}`),t.checked=!t.checked}}},{kind:"method",key:"_pinChanged",value:async function(e){const t=e.target;try{await Object(s.k)(this.hass,{[t.id]:t.value||null}),Object(P.a)(this,this.hass),Object(c.a)(this,"ha-refresh-cloud-status")}catch(i){alert(`${this.hass.localize("ui.panel.config.cloud.account.google.enter_pin_error")} ${i.message}`),t.value=this.cloudStatus.prefs.google_secure_devices_pin}}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      ha-call-api-button {
        color: var(--primary-color);
        font-weight: 500;
      }
      .secure_devices {
        padding-top: 8px;
      }
      paper-input {
        width: 250px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
      .state-reporting {
        display: flex;
        margin-top: 1.5em;
      }
      .state-reporting + p {
        margin-top: 0.5em;
      }
      h3 {
        margin: 0 0 8px 0;
      }
      .state-reporting h3 {
        flex-grow: 1;
        margin: 0;
      }
      .state-reporting-switch {
        margin-top: 0.25em;
        margin-right: 7px;
        margin-left: 0.5em;
      }
    `}}]}},n.a);customElements.define("cloud-google-pref",$);function A(e){var t,i=W(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function F(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function I(e){return e.decorators&&e.decorators.length}function R(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function L(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function W(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}!function(e,t,i,r){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!I(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=W(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=L(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=L(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var a=t(function(e){o.initializeInstanceElements(e,s.elements)},i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(R(n.descriptor)||R(o.descriptor)){if(I(n)||I(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(I(n)){if(I(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}F(n,o)}else t.push(n)}return t}(a.d.map(A)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(n.d)("cloud-remote-pref")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return n.f``;const{remote_connected:e,remote_domain:t,remote_certificate:i}=this.cloudStatus;return i?n.f`
      <ha-card
        header=${this.hass.localize("ui.panel.config.cloud.account.remote.title")}
      >
        <div class="switch">
          <ha-switch
            .checked="${e}"
            @change="${this._toggleChanged}"
          ></ha-switch>
        </div>
        <div class="card-content">
          ${this.hass.localize("ui.panel.config.cloud.account.remote.info")}
          ${e?this.hass.localize("ui.panel.config.cloud.account.remote.instance_is_available"):this.hass.localize("ui.panel.config.cloud.account.remote.instance_will_be_available")}
          <a href="https://${t}" target="_blank" class="break-word">
            https://${t}</a
          >.
        </div>
        <div class="card-actions">
          <a href="https://www.nabucasa.com/config/remote/" target="_blank">
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.account.remote.link_learn_how_it_works")}</mwc-button
            >
          </a>
          ${i?n.f`
                <div class="spacer"></div>
                <mwc-button @click=${this._openCertInfo}>
                  ${this.hass.localize("ui.panel.config.cloud.account.remote.certificate_info")}
                </mwc-button>
              `:""}
        </div>
      </ha-card>
    `:n.f`
        <ha-card
          header=${this.hass.localize("ui.panel.config.cloud.account.remote.title")}
        >
          <div class="preparing">
            ${this.hass.localize("ui.panel.config.cloud.account.remote.access_is_being_prepared")}
          </div>
        </ha-card>
      `}},{kind:"method",key:"_openCertInfo",value:function(){var e,t;e=this,t={certificateInfo:this.cloudStatus.remote_certificate},Object(c.a)(e,"show-dialog",{dialogTag:"dialog-cloud-certificate",dialogImport:()=>Promise.all([i.e(1),i.e(39)]).then(i.bind(null,755)),dialogParams:t})}},{kind:"method",key:"_toggleChanged",value:async function(e){const t=e.target;try{t.checked?await Object(s.b)(this.hass):await Object(s.f)(this.hass),Object(c.a)(this,"ha-refresh-cloud-status")}catch(i){alert(i.message),t.checked=!t.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      .preparing {
        padding: 0 16px 16px;
      }
      a {
        color: var(--primary-color);
      }
      .break-word {
        overflow-wrap: break-word;
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
    `}}]}},n.a);var B=i(181),M=i(204),H=i(174);customElements.define("cloud-account",class extends(Object(B.a)(Object(H.a)(o.a))){static get template(){return r.a`
      <style include="iron-flex ha-style">
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
      </style>
      <hass-subpage header="[[localize('ui.panel.config.cloud.caption')]]">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header"
              >[[localize('ui.panel.config.cloud.caption')]]</span
            >
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.account.thank_you_note')]]
              </p>
            </div>

            <ha-card
              header="[[localize('ui.panel.config.cloud.account.nabu_casa_account')]]"
            >
              <div class="account-row">
                <paper-item-body two-line="">
                  [[cloudStatus.email]]
                  <div secondary class="wrap">
                    [[_formatSubscription(_subscription)]]
                  </div>
                </paper-item-body>
              </div>

              <div class="account-row">
                <paper-item-body
                  >[[localize('ui.panel.config.cloud.account.connection_status')]]</paper-item-body
                >
                <div class="status">[[cloudStatus.cloud]]</div>
              </div>

              <div class="card-actions">
                <a href="https://account.nabucasa.com" target="_blank"
                  ><mwc-button
                    >[[localize('ui.panel.config.cloud.account.manage_account')]]</mwc-button
                  ></a
                >
                <mwc-button style="float: right" on-click="handleLogout"
                  >[[localize('ui.panel.config.cloud.account.sign_out')]]</mwc-button
                >
              </div>
            </ha-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header"
              >[[localize('ui.panel.config.cloud.account.integrations')]]</span
            >
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.account.integrations_introduction')]]
              </p>
              <p>
                [[localize('ui.panel.config.cloud.account.integrations_introduction2')]]
                <a href="https://www.nabucasa.com" target="_blank"
                  >[[localize('ui.panel.config.cloud.account.integrations_link_all_features')]]</a
                >.
              </p>
            </div>

            <cloud-remote-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-remote-pref>

            <cloud-alexa-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-alexa-pref>

            <cloud-google-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-google-pref>

            <cloud-webhooks
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,cloudStatus:Object,_subscription:{type:Object,value:null}}}ready(){super.ready(),this._fetchSubscriptionInfo()}_computeRemoteConnected(e){return e?this.hass.localize("ui.panel.config.cloud.account.connected"):this.hass.localize("ui.panel.config.cloud.account.not_connected")}async _fetchSubscriptionInfo(){this._subscription=await Object(s.h)(this.hass),this._subscription.provider&&this.cloudStatus&&"connected"!==this.cloudStatus.cloud&&this.fire("ha-refresh-cloud-status")}handleLogout(){this.hass.callApi("post","cloud/logout").then(()=>this.fire("ha-refresh-cloud-status"))}_formatSubscription(e){if(null===e)return this.hass.localize("ui.panel.config.cloud.account.fetching_subscription");let t=e.human_description;return e.plan_renewal_date&&(t=t.replace("{periodEnd}",Object(M.a)(new Date(1e3*e.plan_renewal_date),this.hass.language))),t}});i(108),i(83),i(111),i(240);var q=i(276);i(230);customElements.define("cloud-login",class extends(Object(H.a)(Object(q.a)(Object(B.a)(o.a)))){static get template(){return r.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        paper-item {
          cursor: pointer;
        }
        ha-card {
          overflow: hidden;
        }
        ha-card .card-header {
          margin-bottom: -8px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--google-red-500);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        [hidden] {
          display: none;
        }
        .flash-msg {
          padding-right: 44px;
        }
        .flash-msg paper-icon-button {
          position: absolute;
          top: 8px;
          right: 8px;
          color: var(--secondary-text-color);
        }
      </style>
      <hass-subpage header="[[localize('ui.panel.config.cloud.caption')]]">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header"
              >[[localize('ui.panel.config.cloud.caption')]]</span
            >
            <div slot="introduction">
              <p>
                [[localize('ui.panel.config.cloud.login.introduction')]]
              </p>
              <p>
                [[localize('ui.panel.config.cloud.login.introduction2')]]
                <a href="https://www.nabucasa.com" target="_blank"
                  >Nabu&nbsp;Casa,&nbsp;Inc</a
                >
                [[localize('ui.panel.config.cloud.login.introduction2a')]]
              </p>
              <p>
                [[localize('ui.panel.config.cloud.login.introduction3')]]
              </p>
              <p>
                <a href="https://www.nabucasa.com" target="_blank"
                  >[[localize('ui.panel.config.cloud.login.learn_more_link')]]</a
                >
              </p>
            </div>

            <ha-card hidden$="[[!flashMessage]]">
              <div class="card-content flash-msg">
                [[flashMessage]]
                <paper-icon-button icon="hass:close" on-click="_dismissFlash"
                  >[[localize('ui.panel.config.cloud.login.dismiss')]]</paper-icon-button
                >
                <paper-ripple id="flashRipple" noink=""></paper-ripple>
              </div>
            </ha-card>

            <ha-card
              header="[[localize('ui.panel.config.cloud.login.sign_in')]]"
            >
              <div class="card-content">
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
                <paper-input
                  label="[[localize('ui.panel.config.cloud.login.email')]]"
                  id="email"
                  type="email"
                  value="{{email}}"
                  on-keydown="_keyDown"
                  error-message="[[localize('ui.panel.config.cloud.login.email_error_msg')]]"
                ></paper-input>
                <paper-input
                  id="password"
                  label="[[localize('ui.panel.config.cloud.login.password')]]"
                  value="{{_password}}"
                  type="password"
                  on-keydown="_keyDown"
                  error-message="[[localize('ui.panel.config.cloud.login.password_error_msg')]]"
                ></paper-input>
              </div>
              <div class="card-actions">
                <ha-progress-button
                  on-click="_handleLogin"
                  progress="[[_requestInProgress]]"
                  >[[localize('ui.panel.config.cloud.login.sign_in')]]</ha-progress-button
                >
                <button
                  class="link"
                  hidden="[[_requestInProgress]]"
                  on-click="_handleForgotPassword"
                >
                  [[localize('ui.panel.config.cloud.login.forgot_password')]]
                </button>
              </div>
            </ha-card>

            <ha-card>
              <paper-item on-click="_handleRegister">
                <paper-item-body two-line="">
                  [[localize('ui.panel.config.cloud.login.start_trial')]]
                  <div secondary="">
                    [[localize('ui.panel.config.cloud.login.trial_info')]]
                  </div>
                </paper-item-body>
                <ha-icon-next></ha-icon-next>
              </paper-item>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,email:{type:String,notify:!0},_password:{type:String,value:""},_requestInProgress:{type:Boolean,value:!1},flashMessage:{type:String,notify:!0},_error:String}}static get observers(){return["_inputChanged(email, _password)"]}connectedCallback(){super.connectedCallback(),this.flashMessage&&requestAnimationFrame(()=>requestAnimationFrame(()=>this.$.flashRipple.simulatedRipple()))}_inputChanged(){this.$.email.invalid=!1,this.$.password.invalid=!1,this._error=!1}_keyDown(e){13===e.keyCode&&(this._handleLogin(),e.preventDefault())}_handleLogin(){let e=!1;this.email&&this.email.includes("@")||(this.$.email.invalid=!0,this.$.email.focus(),e=!0),this._password.length<8&&(this.$.password.invalid=!0,e||(e=!0,this.$.password.focus())),e||(this._requestInProgress=!0,this.hass.callApi("post","cloud/login",{email:this.email,password:this._password}).then(()=>{this.fire("ha-refresh-cloud-status"),this.setProperties({email:"",_password:""})},e=>{this._password="";const t=e&&e.body&&e.body.code;if("PasswordChangeRequired"===t)return alert("[[localize('ui.panel.config.cloud.login.alert_password_change_required')]]"),void this.navigate("/config/cloud/forgot-password");const i={_requestInProgress:!1,_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"};"UserNotConfirmed"===t&&(i._error="[[localize('ui.panel.config.cloud.login.alert_email_confirm_necessary')]]"),this.setProperties(i),this.$.email.focus()}))}_handleRegister(){this.flashMessage="",this.navigate("/config/cloud/register")}_handleForgotPassword(){this.flashMessage="",this.navigate("/config/cloud/forgot-password")}_dismissFlash(){setTimeout(()=>{this.flashMessage=""},200)}});var N=i(132),U=i(99);function J(e){var t,i=X(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function K(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function Q(e){return e.decorators&&e.decorators.length}function G(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function V(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function X(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function Y(e,t,i){return(Y="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=Z(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function Z(e){return(Z=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const ee=["account","google-assistant","alexa"],te=["login","register","forgot-password"];!function(e,t,i,r){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(i){t.forEach(function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}},this)},this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!Q(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=X(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),i=V(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:i,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=V(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var a=t(function(e){o.initializeInstanceElements(e,s.elements)},i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(G(n.descriptor)||G(o.descriptor)){if(Q(n)||Q(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(Q(n)){if(Q(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}K(n,o)}else t.push(n)}return t}(a.d.map(J)),e);o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([Object(n.d)("ha-config-cloud")],function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[Object(n.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"isWide",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"narrow",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"route",value:void 0},{kind:"field",decorators:[Object(n.g)()],key:"cloudStatus",value:void 0},{kind:"field",key:"routerOptions",value(){return{defaultPage:"login",showLoading:!0,initialLoad:()=>this._cloudStatusLoaded,beforeRender:e=>{if(this.cloudStatus.logged_in){if(!ee.includes(e))return"account"}else if(!te.includes(e))return"login"},routes:{login:{tag:"cloud-login"},register:{tag:"cloud-register",load:()=>i.e(28).then(i.bind(null,751))},"forgot-password":{tag:"cloud-forgot-password",load:()=>i.e(26).then(i.bind(null,752))},account:{tag:"cloud-account"},"google-assistant":{tag:"cloud-google-assistant",load:()=>Promise.all([i.e(12),i.e(27)]).then(i.bind(null,795))},alexa:{tag:"cloud-alexa",load:()=>Promise.all([i.e(12),i.e(25)]).then(i.bind(null,753))}}}}},{kind:"field",decorators:[Object(n.g)()],key:"_flashMessage",value:()=>""},{kind:"field",decorators:[Object(n.g)()],key:"_loginEmail",value:()=>""},{kind:"field",key:"_resolveCloudStatusLoaded",value:void 0},{kind:"field",key:"_cloudStatusLoaded",value(){return new Promise(e=>{this._resolveCloudStatusLoaded=e})}},{kind:"method",key:"firstUpdated",value:function(e){Y(Z(r.prototype),"firstUpdated",this).call(this,e),this.addEventListener("cloud-done",e=>{this._flashMessage=e.detail.flashMessage,Object(U.a)(this,"/config/cloud/login")})}},{kind:"method",key:"updated",value:function(e){if(Y(Z(r.prototype),"updated",this).call(this,e),e.has("cloudStatus")){const t=e.get("cloudStatus");void 0===t?this._resolveCloudStatusLoaded():t.logged_in!==this.cloudStatus.logged_in&&Object(U.a)(this,this.route.prefix,!0)}}},{kind:"method",key:"createElement",value:function(e){const t=Y(Z(r.prototype),"createElement",this).call(this,e);return t.addEventListener("email-changed",e=>{this._loginEmail=e.detail.value}),t.addEventListener("flash-message-changed",e=>{this._flashMessage=e.detail.value}),t}},{kind:"method",key:"updatePageEl",value:function(e){this.cloudStatus&&!this.cloudStatus.logged_in&&ee.includes(this._currentPage)||("setProperties"in e?e.setProperties({hass:this.hass,email:this._loginEmail,isWide:this.isWide,cloudStatus:this.cloudStatus,flashMessage:this._flashMessage}):(e.hass=this.hass,e.email=this._loginEmail,e.isWide=this.isWide,e.narrow=this.narrow,e.cloudStatus=this.cloudStatus,e.flashMessage=this._flashMessage))}}]}},N.a)}}]);
//# sourceMappingURL=chunk.94ff31bf77871c0da9f1.js.map