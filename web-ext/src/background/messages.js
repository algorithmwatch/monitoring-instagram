import browser from 'webextension-polyfill'
import { closeIGTab } from './igContentScript'
import checkLoginAndFollowing from './checkLoginAndFollowing'
import pushCollectedData from './pushCollectedData'
import { dispatch, getState } from './store'
import {
  LOCAL_STATE_SET_LOGGED_IN,
  LOCAL_STATE_SET_ALLOW_TO_RUN,
  LOCAL_STATE_SET_FOLLOWING_ACCOUNTS,
  MESSAGE_IS_LOGGED,
  MESSAGE_COLLECTED_DATA,
  MESSAGE_ASK_FOR_LOGIN_CHECK,
  MESSAGE_AGREE_TO_RUN,
  MESSAGE_FETCH_STORE,
  MESSAGE_DISPATCH,
} from '../constantes'

export function sendMessage(data) {
  return browser.runtime.sendMessage(data).catch(err => {
    console.error(err.message)
  })
}

export function registerMessageHandler() {
  function handleMessage(request) {
    if (process.env.NODE_ENV !== 'production') {
      console.log('MSG', request.name, request)
    }
    switch (request.name) {
      case MESSAGE_FETCH_STORE:
        return Promise.resolve(getState())
      case MESSAGE_AGREE_TO_RUN:
        // save the agreement to the store
        dispatch({
          type: LOCAL_STATE_SET_ALLOW_TO_RUN,
          payload: true,
        })
        // save the supposed following users to the store
        dispatch({
          type: LOCAL_STATE_SET_FOLLOWING_ACCOUNTS,
          payload: request.payload.accounts,
        })
        checkLoginAndFollowing()
        break
      case MESSAGE_IS_LOGGED:
        // IG page responded with the loggin status. We update then the local state
        dispatch({
          type: LOCAL_STATE_SET_LOGGED_IN,
          payload: request.payload,
        })
        // // if not logged-in, we can close the tab
        if (!request.payload.isLoggedIn) {
          closeIGTab()
        }
        break
      case MESSAGE_ASK_FOR_LOGIN_CHECK:
        // That will check the loggin status and fetch data
        checkLoginAndFollowing()
        break
      case MESSAGE_COLLECTED_DATA:
        // collected data has arrived ! We send them to the server
        pushCollectedData(request.payload)
        // close the tab
        closeIGTab()
        break
      // Will dispatch the action to the store
      case MESSAGE_DISPATCH:
        dispatch(request.action)
        break
      default:
        break
    }
  }
  browser.runtime.onMessage.addListener(handleMessage)
}
