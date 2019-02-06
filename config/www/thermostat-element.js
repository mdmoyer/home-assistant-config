import {
  LitElement,
  html
} from 'https://unpkg.com/@polymer/lit-element@^0.5.2/lit-element.js?module';

class ThermostatElement extends LitElement {
  static get properties() {
    return {
      hass: Object,
      config: Object,
    }
  }

  _render({
    hass,
    config
  }) {
    const entityId = config.entity;
    const hvacState = hass.states[config.hvac_state].state;
    const temperatureUnits = hass.states['sensor.dining_room_thermostat_nest_temperature'].attributes['unit_of_measurement'];
    const currentTemperature = hass.states[entityId].attributes['current_temperature']
    const operation_mode = hass.states[entityId].attributes['operation_mode']

    return html `
      <style>
        .box {
          width: 40px;
          height: 40px;
          border-radius: 20px;
          line-height: 40px;
          text-align: center;
          color: white;
        }
        .temp-value {
          font-size: 14pt;
          font-weight: bold;
        }
        .temp-units {
          font-size: 10pt;
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
      </style>
      <div class$="box ${hvacState}">
        <span class="temp-value">${currentTemperature}</span>
      </div>
    `;
  }

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

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;

    this.addEventListener("click", event => {
      event.stopPropagation();
      this._fire("hass-more-info", {
        entityId: config.entity
      });
    });
  }
}
customElements.define('thermostat-element', ThermostatElement);
