import browser from 'webextension-polyfill'
import React from 'react'
import Box from '@material-ui/core/Box'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemText from '@material-ui/core/ListItemText'
import ListItemAvatar from '@material-ui/core/ListItemAvatar'
import Avatar from '@material-ui/core/Avatar'
import Alert from '@material-ui/lab/Alert'
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction'
import CircularProgress from '@material-ui/core/CircularProgress'
import ErrorIcon from '@material-ui/icons/Error'
import SuccessIcon from '@material-ui/icons/CheckCircleOutline'
import { useAddonState } from './hooks/useAddonState'
import { MESSAGE_ASK_FOR_LOGIN_CHECK } from '../constantes'
import I18n from './I18n'

const FollowingStatus = () => {
  const { sharedState } = useAddonState()
  const [retryCount, setRetryCount] = React.useState(0)
  const retryTimeoutRef = React.useRef()

  React.useEffect(() => {
    let isLoading =
      sharedState.isLoggedIn &&
      !sharedState.supposedFollowingAccounts.every(
        account => sharedState.followingAccounts[account.ig_username]
      )
    if (isLoading) {
      if (retryTimeoutRef.current === undefined && retryCount < 5) {
        retryTimeoutRef.current = setTimeout(() => {
          // retry
          browser.runtime.sendMessage({
            name: MESSAGE_ASK_FOR_LOGIN_CHECK,
          })
          retryTimeoutRef.current = undefined
          setRetryCount(retryCount + 1)
        }, 15000)
      }
    } else {
      clearTimeout(retryTimeoutRef.current)
      retryTimeoutRef.current = undefined
      setRetryCount(0)
    }
  }, [sharedState, retryCount])

  if (!sharedState.isLoggedIn) {
    return null
  }
  return (
    <div>
      <I18n name="dashboard_followingStatus_title" variant="h5" gutterBottom />
      {retryCount > 0 && (
        <I18n
          name="dashboard_followingStatus_retrying"
          args={[retryCount]}
          variant="subtitle1"
          component="span"
        />
      )}
      {sharedState.followingAccounts &&
        Object.keys(sharedState.followingAccounts).some(
          key => sharedState.followingAccounts[key].isFollowing === false
        ) && (
          <Alert color="error">
            <I18n name="dashboard_followingStatus_error" />
          </Alert>
        )}

      {sharedState.followingAccounts &&
        Object.keys(sharedState.followingAccounts).length ===
          sharedState.supposedFollowingAccounts.length &&
        Object.keys(sharedState.followingAccounts).every(
          key => sharedState.followingAccounts[key].isFollowing === true
        ) && (
          <Alert color="success">
            <I18n name="dashboard_followingStatus_success" />
          </Alert>
        )}
      <Box maxWidth={400}>
        <List>
          {sharedState.supposedFollowingAccounts.map(account => (
            <ListItem
              button
              component="a"
              dense
              key={account.id}
              href={`https://www.instagram.com/${account.ig_username}/`}
              rel="noopener noreferrer nofollow"
              target="_blank"
            >
              <ListItemAvatar>
                <Avatar src={account.ig_profile_pic}></Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={`${account.ig_full_name}`}
                secondary={`@${account.ig_username}`}
              />
              <ListItemSecondaryAction>
                {sharedState.followingAccounts[account.ig_username] ? (
                  sharedState.followingAccounts[account.ig_username]
                    .isFollowing ? (
                    <SuccessIcon style={{ color: 'green' }} />
                  ) : (
                    <ErrorIcon style={{ color: 'red' }} />
                  )
                ) : (
                  <CircularProgress
                    style={{ width: 30, height: 30 }}
                    variant="indeterminate"
                  />
                )}
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </Box>
    </div>
  )
}

export default FollowingStatus
