/* eslint-disable react/prop-types */
import React, { createContext, useContext, useReducer } from 'react'
import { MESSAGE_UPDATED_STATE, MESSAGE_FETCH_STORE } from '../../constantes'
import browser from 'webextension-polyfill'

export const SET_NEW_SHARED_STATE =
  'undressingIG/dashboard/SET_NEW_SHARED_STATE'
const StateContext = createContext()
const DispatchContext = createContext()

const __initialState = {
  // shared with background
  sharedState: {},
}

const __reducer = (state, action) => {
  switch (action.type) {
    case SET_NEW_SHARED_STATE:
      return {
        ...state,
        sharedState: action.payload || {},
      }
    default:
      return { ...state }
  }
}

export const DataStateProvider = ({
  reducer = __reducer,
  initialState = __initialState,
  children,
}) => {
  const [state, dispatch] = useReducer(reducer, initialState)
  React.useEffect(() => {
    // ask for the current state
    browser.runtime.sendMessage({ name: MESSAGE_FETCH_STORE }).then(store =>
      dispatch({
        type: SET_NEW_SHARED_STATE,
        payload: store,
      })
    )
    // and subscribe for updates
    browser.runtime.onMessage.addListener(request => {
      if (request.name === MESSAGE_UPDATED_STATE) {
        dispatch({
          type: SET_NEW_SHARED_STATE,
          payload: request.payload,
        })
      }
    })
  }, [])

  return (
    <DispatchContext.Provider value={dispatch}>
      <StateContext.Provider value={state}>{children}</StateContext.Provider>
    </DispatchContext.Provider>
  )
}

export const useAddonState = () => useContext(StateContext)
export const useAddonStateDispatch = () => useContext(DispatchContext)
