import browser from 'webextension-polyfill'
import { INSTAGRAM_URL } from '../constantes'
import { getState } from './store'

const DO_NOT_CLOSE_URL = browser.runtime.getURL('./do-not-close-page/main.html')

async function collectExplore() {
  const windowIg = await getOrCreateWindow()
  return new Promise(resolve => {
    function listener(details) {
      let filter = browser.webRequest.filterResponseData(details.requestId)
      let decoder = new TextDecoder('utf-8')
      let encoder = new TextEncoder()
      let data = []

      filter.ondata = event => {
        data.push(event.data)
      }

      filter.onstop = () => {
        let str = ''
        if (data.length == 1) {
          str = decoder.decode(data[0])
        } else {
          for (let i = 0; i < data.length; i++) {
            let stream = i == data.length - 1 ? false : true
            str += decoder.decode(data[i], { stream })
          }
        }
        let payload = JSON.parse(str)
        const { isLoggedIn } = getState()

        fetch(`${process.env.BACKEND_URL}/api/v2/donation/`, {
          method: 'POST',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            data: {
              ig_username: isLoggedIn,
              payload,
            },
            data_source: 'explore',
          }),
        }).then(() => {
          resolve()
        })
        filter.write(encoder.encode(str))
        filter.close()
      }
      browser.webRequest.onBeforeRequest.removeListener(listener)
      return {}
    }

    console.log('explore')

    const exploreigTab = browser.tabs.create({
      url: INSTAGRAM_URL + 'explore/',
      active: false,
      windowId: windowIg.id,
    })
    browser.webRequest.onBeforeRequest.addListener(
      listener,
      { urls: [INSTAGRAM_URL + 'explore/grid/*'], tabId: exploreigTab.id },
      ['requestBody', 'blocking']
    )
  })
}

export async function runScriptOnce() {
  const windowIg = await getOrCreateWindow()
  // remove existing IG tab
  await closeIGTab()
  if (browser.webRequest.filterResponseData) {
    await collectExplore()
  }

  // open a new IG tab
  const igTab = await browser.tabs.create({
    url: INSTAGRAM_URL,
    active: false,
    windowId: windowIg.id,
  })

  windowIg.tabs.map(t => {
    browser.browserAction.disable(t.id)
  })
  return browser.tabs.executeScript(igTab.id, {
    runAt: 'document_end',
    file: 'dist/inject-collect-feed.js',
  })
}

async function windowExists(pageId) {
  return browser.windows
    .get(pageId)
    .then(() => true)
    .catch(() => false)
}

export async function getOrCreateWindow() {
  let existingWindow = await findWindowId()
  if (existingWindow) {
    // reuse the window
    return await browser.windows.get(existingWindow, { populate: true })
  } else {
    // create a new window
    let windowIg
    windowIg = await browser.windows.create({
      url: DO_NOT_CLOSE_URL,
      state: 'minimized',
    })
    // save the new window id
    await browser.storage.local.set({
      pageId: windowIg.id,
    })
    return windowIg
  }
}

export async function closeIGTab() {
  console.log('closing all tabs')
  let existingWindow = await findWindowId()
  const tabs = await browser.tabs.query({
    url: INSTAGRAM_URL + '*',
    windowId: existingWindow,
  })
  try {
    console.log('trying to remove all tabs', existingWindow, tabs)
    await browser.tabs.remove(tabs.map(t => t.id))
  } catch (error) {
    console.error("couldn't remove all tabs", error)
  }
}

async function findWindowId() {
  const { pageId } = await browser.storage.local.get('pageId')
  if (pageId && (await windowExists(pageId))) {
    return pageId
  }
  const windows = await browser.windows.getAll({ populate: true })
  let foundWindowId
  for (let index = 0; index < windows.length; index++) {
    const win = windows[index]
    for (let index = 0; index < win.tabs.length; index++) {
      const tab = win.tabs[index]
      if (tab.url === browser.runtime.getURL('do-not-close-page/main.html')) {
        foundWindowId = win.id
        break
      }
    }
    if (foundWindowId) {
      break
    }
  }
  return foundWindowId
}
