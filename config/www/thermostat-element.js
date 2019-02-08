class ThermostatElement extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({
      mode: 'open'
    });
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }

    const root = this.shadowRoot;
    const style = document.createElement('style');
    style.textContent = `
      .temp-value {
        font-size: 14pt;
        font-weight: bold;
      }
      .cool {
        background-color: #0080FF;
      }
      .heat {
        background-color: #F48013;
      }
      .off {
        background-color: black;
      }
    `;
    root.appendChild(style);

    this.addEventListener("click", event => {
      this._fire("hass-more-info", {
        entityId: config.entity
      });
    });

    this.config = config;
  }

  set hass(hass) {
    const root = this.shadowRoot;
    if (!this.content) {
      this.content = document.createElement('div');
      this.content.style.width = '40px';
      this.content.style.height = '40px';
      this.content.style.borderRadius = '20px';
      this.content.style.backgroundColor = 'black';
      this.content.style.lineHeight = '40px';
      this.content.style.textAlign = 'center';
      this.content.style.color = 'white';
      root.appendChild(this.content);
    }

    const entityId = this.config.entity;
    const hvacState = hass.states[this.config.hvac_state].state;
    const temperatureUnits = hass.states['sensor.dining_room_thermostat_nest_temperature'].attributes['unit_of_measurement'];
    const currentTemperature = hass.states[entityId].attributes['current_temperature']
    const operation_mode = hass.states[entityId].attributes['operation_mode']

    this.content.innerHTML = `
      <span class="temp-value">${currentTemperature}</span>
    `;

    var svgElt = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svgElt.style = document.createElement('style');
    svgElt.style.position = 'absolute';
    svgElt.style.top = '0px';
    svgElt.style.left = '0px';
    svgElt.style.width = '100%';
    svgElt.style.height = '100%';
    svgElt = this.drawTicks(svgElt, 60, 80);
    this.content.appendChild(svgElt);
  }

  drawTicks(svgElt, gapWidth, numTicks) {
    var angle = 270 - (gapWidth / 2);
    for (var x = 0; x < numTicks; x++) {
      svgElt.appendChild(this.drawTick(angle, 40, 49));
      angle -= (360 - gapWidth) / (numTicks - 1);
    }
    return svgElt;
  }

  drawTick(angle, pctStart, pctEnd) {
    var start = this.radToCart(angle, pctStart);
    var end = this.radToCart(angle, pctEnd);
    var line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', start[0]);
    line.setAttribute('y1', start[1]);
    line.setAttribute('x2', end[0]);
    line.setAttribute('y2', end[1]);
    line.setAttribute('style', 'stroke:white; stroke-width:.5');
    return line;
  }

  /**
   * Converts radial coordinates to TOP and LEFT coordinates for HTML, in percent.
   */
  radToCart(angle, radius) {
    var left = radius * Math.cos(this.degToRad(angle)) + 50;
    var top = -radius * Math.sin(this.degToRad(angle)) + 50;
    return [Number.parseFloat(left).toPrecision(3) + "%", Number.parseFloat(top).toPrecision(3) + "%"];
  }

  /**
   * Degrees to radians
   */
  degToRad(degrees) {
    return degrees * (Math.PI / 180);
  }

  /**
   * From https://github.com/ciotlosm/custom-lovelace/blob/master/bignumber-card/bignumber-card.js
   */
  _fire(type, detail, options) {
    const node = this.shadowRoot;
    options = options || {};
    detail = (detail === null || detail === undefined) ? {} : detail;
    const event = new Event(type, {
      bubbles: options.bubbles === undefined ? true : options.bubbles,
      cancelable: Boolean(options.cancelable),
      composed: options.composed === undefined ? true : options.composed
    });
    event.detail = detail;
    node.dispatchEvent(event);
    return event;
  }
}

customElements.define('thermostat-element', ThermostatElement);
