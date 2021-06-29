import React from 'react'
import Box from '@material-ui/core/Box'
import Button from '@material-ui/core/Button'
import Link from '@material-ui/core/Link'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemText from '@material-ui/core/ListItemText'
import ListItemAvatar from '@material-ui/core/ListItemAvatar'
import Avatar from '@material-ui/core/Avatar'
import CircularProgress from '@material-ui/core/CircularProgress'
import Alert from '@material-ui/lab/Alert'
import LinkIcon from '@material-ui/icons/Launch'
import { MESSAGE_AGREE_TO_RUN } from '../constantes'
import { useAddonState } from './hooks/useAddonState'
import ChangeProjectLink from './ChangeProjectLink'
import sendMsg from '../utils/sendMsg'
import TypographyMarked from './TypographyMarked'
import I18n, { getMessage } from './I18n'
import useCurrentProject from './hooks/useCurrentProject'

const IntroAfterInstallation = () => {
  const [accounts, setAccounts] = React.useState()
  const currentProject = useCurrentProject()

  const {
    sharedState: { project },
  } = useAddonState()

  React.useEffect(() => {
    if (project) {
      fetch(`${process.env.BACKEND_URL}/api/v2/account/?project=${project}`)
        .then(req => req.text())
        .then(JSON.parse)
        .then(res => res.results)
        .then(setAccounts)
    }
  }, [project])

  const handleIAgreeClick = () => {
    sendMsg(MESSAGE_AGREE_TO_RUN, { accounts })
  }
  return (
    <Box maxWidth={600} mt={8} mb={15}>
      <Box mb={4}>
        <I18n name="dashboard_introduction" />
        {currentProject && (
          <I18n
            name="dashboard_introduction_currentProject"
            args={[currentProject.name]}
          />
        )}
        <Box mt={2} mb={4}>
          <ChangeProjectLink />
        </Box>
        <I18n
          name="dashboard_introduction_projectDescription_title"
          gutterBottom
          variant="h5"
        />
        {currentProject && (
          <TypographyMarked md={currentProject.description} gutterBottom />
        )}
        <I18n
          name="dashboard_introduction_requirements"
          componentArg={
            <Link
              href="https://www.instagram.com/accounts/login/"
              target="_blank"
              rel="noopener noreferrer nofollow"
            >
              Instagram
              <LinkIcon style={{ width: 16 }} />
            </Link>
          }
        />
        {accounts ? (
          <List>
            {accounts.map(account => (
              <ListItemLink
                button
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
                  primary={`${account.ig_full_name} – ${getMessage(
                    'dashboard_introduction_requirements_openAccountInNewTabAction'
                  )}`}
                  secondary={`@${account.ig_username}`}
                />
              </ListItemLink>
            ))}
          </List>
        ) : (
          <CircularProgress variant="indeterminate" />
        )}
        <I18n name="dashboard_introduction_requirements_inviteToAcceptTheTOS" />
      </Box>
      <Alert color="warning">
        {getMessage(
          'dashboard_introduction_requirements_alertAboutFBContainerPluggin'
        )}
      </Alert>
      <Box my={4}>
        <Button
          onClick={handleIAgreeClick}
          variant="contained"
          color="primary"
          size="large"
        >
          {getMessage(
            'dashboard_introduction_requirements_acceptTOSLabelButton'
          )}
        </Button>
      </Box>
    </Box>
  )
}

function ListItemLink(props) {
  return <ListItem button component="a" {...props} />
}

export default IntroAfterInstallation
