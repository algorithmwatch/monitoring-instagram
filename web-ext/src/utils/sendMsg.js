import browser from 'webextension-polyfill'

export default function sendMsg(name, payload) {
  return browser.runtime.sendMessage({
    name,
    payload,
  })
}
