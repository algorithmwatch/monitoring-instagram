import browser from 'webextension-polyfill'
import { selectorThereIsAProblem } from '../store'

export default function iconMiddleware(state) {
  const hasProbem = selectorThereIsAProblem(state)
  const projectIsActive = state.projectIsActive
  let color = 'black'
  if (!projectIsActive) {
    color = 'blue'
  } else if (hasProbem) {
    color = 'red'
  }
  browser.browserAction.setIcon({
    path: {
      16: `icons/eye-${color}-16.png`,
      32: `icons/eye-${color}-32.png`,
    },
  })
}
