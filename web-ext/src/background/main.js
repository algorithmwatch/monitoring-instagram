import browser from 'webextension-polyfill'
import registerOnInstalledhandler from './registerOnInstalledhandler'
import { openDashboard } from './dashboard'
import { registerMessageHandler } from './messages'
import { createStore, getState } from './store'
import checkLoginAndFollowing from './checkLoginAndFollowing'
import iconMiddleware from './middlewares/iconMiddleware'
import detectProject from './detectProject'
import checkProjectStatus from './checkProjectStatus'

async function init() {
  // init store
  await createStore({
    middlewares: [iconMiddleware],
  })
  // if not set, detect the project based on user locale
  await detectProject()
  // handle messages with pages (dashboard and IG)
  registerMessageHandler()
  // open the dashboard on browserAction click
  browser.browserAction.onClicked.addListener(openDashboard)
  // check the login and following status (cron will start if succeed)
  if (getState().isAllowedToRun && getState().projectIsActive) {
    await checkLoginAndFollowing()
  }
  await checkProjectStatus()
}
// detecting addon installation
registerOnInstalledhandler()
init()
