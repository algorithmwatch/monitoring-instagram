import browser from 'webextension-polyfill'
import getBrowser from './getBrowser'
import { dispatch, getState, selectorThereIsAProblem } from './store'
import {
  INSTAGRAM_URL,
  MESSAGE_IS_LOGGED,
  LOCAL_STATE_START_CHECK_LOGIN_AND_FOLLOWING,
  INJECT_SCRIPT_END_MESSAGE,
} from '../constantes'
import { getOrCreateWindow } from './igContentScript'
import startCron from './cron'

const executeScriptAndWaitForMsg = (script, waitResponseMsgName, tabId) => {
  return new Promise((resolve, reject) => {
    function onTabUpdated(updatedtabId, changeInfo) {
      if (updatedtabId == tabId && changeInfo.status === 'complete') {
        browser.tabs.onUpdated.removeListener(onTabUpdated)
        browser.tabs
          .executeScript(tabId, {
            file: script,
          })
          .then(() => {
            const listener = request => {
              if (request.name === waitResponseMsgName) {
                clearTimeout(timeout)
                browser.runtime.onMessage.removeListener(listener)
                resolve(request)
              }
            }
            let timeout = setTimeout(() => {
              browser.runtime.onMessage.removeListener(listener)
              reject(
                `timeout ! script: ${script}, waitResponseMsgName: ${waitResponseMsgName}`
              )
            }, 5000)
            browser.runtime.onMessage.addListener(listener)
          })
      }
    }
    browser.tabs.onUpdated.addListener(onTabUpdated)
  })
}

export default async function checkLoginAndFollowing() {
  dispatch({
    type: LOCAL_STATE_START_CHECK_LOGIN_AND_FOLLOWING,
  })
  let windowIg = await getOrCreateWindow()
  let igTab = await browser.tabs.create({
    url: INSTAGRAM_URL,
    active: false,
    windowId: windowIg.id,
  })
  await executeScriptAndWaitForMsg(
    '/dist/inject-home-check-login.js',
    MESSAGE_IS_LOGGED,
    igTab.id
  )
  await browser.tabs.remove(igTab.id)

  const { isLoggedIn, supposedFollowingAccounts } = getState()
  if (isLoggedIn) {
    for (let idx = 0; idx < supposedFollowingAccounts.length; idx++) {
      const account = supposedFollowingAccounts[idx]
      let igTab = await browser.tabs.create({
        url: `${INSTAGRAM_URL}${account.ig_username}/`,
        active: false,
        windowId: windowIg.id,
      })
      await executeScriptAndWaitForMsg(
        'dist/inject-profile-page-check-following.js',
        INJECT_SCRIPT_END_MESSAGE,
        igTab.id
      )
      await browser.tabs.remove(igTab.id)
    }
    let hasProbem = selectorThereIsAProblem(getState())
    // notify the backend about the user status
    await fetch(`${process.env.BACKEND_URL}/api/v2/donor/`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ig_username: isLoggedIn,
        following: supposedFollowingAccounts.map(({ id }) => id),
        last_status: !hasProbem,
        version: browser.runtime.getManifest().version,
        browser: getBrowser(),
      }),
    })
    startCron()
  }
}
