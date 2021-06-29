import browser from 'webextension-polyfill'
import { MESSAGE_DISPATCH } from '../constantes'

export default function sendDispatchMsg(action) {
  return browser.runtime.sendMessage({
    name: MESSAGE_DISPATCH,
    action,
  })
}
