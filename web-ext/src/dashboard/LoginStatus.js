import browser from 'webextension-polyfill'
import React from 'react'
import Button from '@material-ui/core/Button'
import Box from '@material-ui/core/Box'
import CircularProgress from '@material-ui/core/CircularProgress'
import Alert from '@material-ui/lab/Alert'
import RefreshIcon from '@material-ui/icons/Refresh'
import {
  MESSAGE_ASK_FOR_LOGIN_CHECK,
  INSTAGRAM_LOGIN_URL,
  LOCAL_STATE_CANCEL_CHECK_LOGIN_AND_FOLLOWING,
} from '../constantes'
import { useAddonState } from './hooks/useAddonState'
import I18n, { getMessage } from './I18n'
import { Typography } from '@material-ui/core'
import sendDispatchMsg from '../utils/sendDispatchMsg'

const LoggingChecker = () => {
  const { sharedState } = useAddonState()
  const [retryCount, setRetryCount] = React.useState(0)
  const retryTimeoutRef = React.useRef()

  let isLoading = sharedState.isLoggedIn === undefined
  const maxRetry = 5
  const retryDelay = 15000
  React.useEffect(() => {
    if (isLoading) {
      if (retryTimeoutRef.current === undefined && retryCount < maxRetry) {
        retryTimeoutRef.current = setTimeout(() => {
          // retry
          askForLoginCheck()
          retryTimeoutRef.current = undefined
          setRetryCount(retryCount + 1)
        }, retryDelay)
      }
      // we tried enough
      if (retryTimeoutRef.current === undefined && retryCount >= maxRetry) {
        retryTimeoutRef.current = setTimeout(() => {
          // reset the related state
          sendDispatchMsg({
            type: LOCAL_STATE_CANCEL_CHECK_LOGIN_AND_FOLLOWING,
          })
          retryTimeoutRef.current = undefined
          // reset the retry count, if the user want to try again with the button
          setRetryCount(0)
        }, retryDelay)
      }
    } else {
      clearTimeout(retryTimeoutRef.current)
    }
  }, [isLoading, retryCount])

  const askForLoginCheck = () => {
    browser.runtime.sendMessage({
      name: MESSAGE_ASK_FOR_LOGIN_CHECK,
    })
  }

  return (
    <div>
      <Box mb={4} mt={8}>
        <Button
          variant="outlined"
          disabled={isLoading}
          onClick={askForLoginCheck}
          startIcon={<RefreshIcon />}
        >
          {isLoading
            ? retryCount > 0
              ? getMessage('dashboard_followingStatus_retrying', [retryCount])
              : getMessage('dashboard_loginStatus_refreshingButtonLabel')
            : getMessage('dashboard_loginStatus_refreshButtonLabel')}
        </Button>
      </Box>
      <Typography variant="h5" gutterBottom>
        {getMessage('dashboard_loginStatus_title')}
      </Typography>
      {isLoading && <CircularProgress variant="indeterminate" />}
      {!isLoading &&
        (sharedState.isLoggedIn ? (
          <Alert severity="success">
            <I18n name="dashboard_loginStatus_success" />
          </Alert>
        ) : (
          <Alert
            severity="error"
            action={
              <Button
                size="small"
                href={INSTAGRAM_LOGIN_URL}
                target="_blank"
                rel="noopener noreferrer"
              >
                {getMessage('dashboard_loginStatus_error_actionButtonLabel')}
              </Button>
            }
          >
            <I18n name="dashboard_loginStatus_error" />
          </Alert>
        ))}
    </div>
  )
}

export default LoggingChecker
