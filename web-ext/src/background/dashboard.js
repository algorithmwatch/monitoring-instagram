import browser from 'webextension-polyfill'

/**
 * Close previous tab and open the dashboard in the active window
 */
export async function openDashboard() {
  //   close previous tab
  const tabs = await browser.tabs.query({
    url: browser.runtime.getURL('dashboard/main.html'),
  })
  await Promise.all(tabs.map(t => browser.tabs.remove(t.id)))
  const windowId = await getWindowId()
  return await browser.tabs.create({
    windowId: windowId,
    url: 'dashboard/main.html',
  })
}

async function getWindowId() {
  const { pageId } = await browser.storage.local.get('pageId')
  const windows = await browser.windows.getAll({ populate: true })
  let allWindowsExceptBgW = windows.filter(w => w.id !== pageId)
  let windowId
  if (allWindowsExceptBgW.length < 1) {
    windowId = (await browser.windows.create()).id
  } else {
    windowId = allWindowsExceptBgW[0].id
  }
  return windowId
}
