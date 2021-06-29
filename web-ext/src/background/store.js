import browser from 'webextension-polyfill'
import { sendMessage } from './messages'
import {
  MESSAGE_UPDATED_STATE,
  LOCAL_STATE_SET_LOGGED_IN,
  LOCAL_STATE_SET_ALLOW_TO_RUN,
  LOCAL_STATE_UPDATE_FOLLOWING,
  LOCAL_STATE_CANCEL_CHECK_LOGIN_AND_FOLLOWING,
  LOCAL_STATE_SET_PROJECT,
  LOCAL_STATE_START_CHECK_LOGIN_AND_FOLLOWING,
  LOCAL_STATE_SET_FOLLOWING_ACCOUNTS,
  LOCAL_STATE_SET_PROJECT_STATUS,
} from '../constantes'

const STATE = {
  actualState: {
    isLoggedIn: undefined,
    isAllowedToRun: false,
    supposedFollowingAccounts: [],
    followingAccounts: {},
    project: undefined,
    projectIsActive: true,
  },
}

const MIDDLEWARES = []

export function getState() {
  return STATE.actualState
}

export function registerMiddleware(m) {
  MIDDLEWARES.push(m)
}

function setState(state) {
  STATE.actualState = state
  browser.storage.local.set({ store: state })
}

export function dispatch(action) {
  let prevState = getState()
  const newState = reducer(prevState, action)
  setState(newState)
  MIDDLEWARES.forEach(middleware => {
    middleware(newState, prevState)
  })
  if (process.env.NODE_ENV !== 'production') {
    console.log(action.type, { newState, prevState, action })
  }
  sendMessage({
    name: MESSAGE_UPDATED_STATE,
    payload: newState,
  })
}
function reducer(state, action) {
  switch (action.type) {
    case LOCAL_STATE_SET_ALLOW_TO_RUN:
      return {
        ...state,
        isAllowedToRun: action.payload,
      }
    case LOCAL_STATE_SET_FOLLOWING_ACCOUNTS:
      return {
        ...state,
        supposedFollowingAccounts: action.payload,
      }
    case LOCAL_STATE_SET_LOGGED_IN:
      return {
        ...state,
        isLoggedIn: action.payload.isLoggedIn && action.payload.igUsername,
      }
    case LOCAL_STATE_CANCEL_CHECK_LOGIN_AND_FOLLOWING:
      return {
        ...state,
        isLoggedIn: false,
        followingAccounts: {},
      }
    case LOCAL_STATE_START_CHECK_LOGIN_AND_FOLLOWING:
      return {
        ...state,
        isLoggedIn: undefined,
        followingAccounts: {},
      }
    case LOCAL_STATE_UPDATE_FOLLOWING:
      // sends followers
      sendFollowersCount(
        state.isLoggedIn,
        action.payload.igUsername,
        action.payload.userData
      )
      return {
        ...state,
        followingAccounts: {
          ...state.followingAccounts,
          [action.payload.igUsername]: {
            isFollowing: action.payload.isFollowing,
          },
        },
      }
    case LOCAL_STATE_SET_PROJECT:
      return {
        ...state,
        project: action.payload,
      }
    case LOCAL_STATE_SET_PROJECT_STATUS:
      return {
        ...state,
        projectIsActive: action.payload,
      }
    default:
      return state
  }
}

export async function createStore({ middlewares }) {
  // register middlewares
  if (middlewares && middlewares.length > 0) {
    middlewares.forEach(registerMiddleware)
  }
  // dehydrate store from localstorage
  const { store } = await browser.storage.local.get('store')
  if (store) {
    // Note: MIGRATION v2.x
    // there is already a store, so the ext has been already installed.
    // we check if the project state (v2.x) exists, or we set it with the initial value.
    // Only for upgrading v1.x users
    if (store.project === undefined) {
      store.project = 1
    }
    setState(store)
  }
}
/**
 * Returns true if at least one supposed followed accounts is not followed.
 * This is for ex. used to show a red icon in case of issue.
 * @param {*} state
 */
export function selectorThereIsAProblem(state) {
  return (
    !state.isLoggedIn ||
    state.supposedFollowingAccounts.length !== 3 ||
    Object.keys(state.followingAccounts).length !== 3 ||
    Object.keys(state.followingAccounts).some(
      key => !state.followingAccounts[key].isFollowing
    )
  )
}

/**
 * Returns true if all supposed followed accounts are not followed.
 * This is used to valid condition before we collect data.
 * @param {*} state
 */
export function selectorThereIsReallyAProblem(state) {
  return (
    !state.isLoggedIn ||
    state.supposedFollowingAccounts.length !== 3 ||
    Object.keys(state.followingAccounts).length !== 3 ||
    Object.keys(state.followingAccounts).every(
      key => !state.followingAccounts[key].isFollowing
    )
  )
}

function sendFollowersCount(author, igUsername, userData) {
  // sends followers
  return fetch(`${process.env.BACKEND_URL}/api/v2/user-followed-by/`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ig_username: igUsername,
      author: author,
      count: userData.edge_followed_by.count,
    }),
  })
}
