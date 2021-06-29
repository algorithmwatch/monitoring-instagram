import browser from 'webextension-polyfill'
import { IMPLANTED_SCRIPT_RESULT_MESSAGE } from '../../constantes'

/** Implant a script in the actual DOM, in order to access its variables.
 * Then wait for a msg and resolve with the content of this msg.
 * The given script must broadcast a msg `IMPLANTED_SCRIPT_RESULT_MESSAGE`
 */
const implantScript = script => {
  return new Promise(resolve => {
    function handleEvent(event) {
      if (
        event.source == window &&
        event.data &&
        event.data.message === IMPLANTED_SCRIPT_RESULT_MESSAGE
      ) {
        resolve(event.data.payload)
        s.remove()
        window.removeEventListener('message', handleEvent)
      }
    }
    window.addEventListener('message', handleEvent)
    let url = browser.runtime.getURL(script)
    var th = document.getElementsByTagName('body')[0]
    var s = document.createElement('script')
    s.setAttribute('type', 'text/javascript')
    s.setAttribute('src', url)
    th.appendChild(s)
  })
}

export default implantScript
