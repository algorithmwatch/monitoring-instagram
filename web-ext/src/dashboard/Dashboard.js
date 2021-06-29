import React from 'react'
import Box from '@material-ui/core/Box'
import Typography from '@material-ui/core/Typography'
import LoginStatus from './LoginStatus'
import Header from './Header'
import Footer from './Footer'
import FollowingStatus from './FollowingStatus'
import IntroAfterInstallation from './IntroAfterInstallation'
import { useAddonState } from './hooks/useAddonState'
import useCurrentProject from './hooks/useCurrentProject'
import TypographyMarked from './TypographyMarked'
import I18n, { getMessage } from './I18n'

const Dashboard = () => {
  const { sharedState } = useAddonState()
  const currentProject = useCurrentProject()

  React.useEffect(() => {
    document.title = getMessage('extension_name')
  }, [])
  if (sharedState.isAllowedToRun && !sharedState.projectIsActive) {
    return (
      <div>
        <Box maxWidth={800} margin="auto" my={4} px={2}>
          <Header />
          <Box pt={4}>
            <I18n
              name="dashboard_inactive_project"
              args={[currentProject && currentProject.name]}
            />
          </Box>
        </Box>
      </div>
    )
  }
  return (
    <div>
      <Box maxWidth={800} margin="auto" my={4} px={2}>
        <Header />
        {sharedState.isAllowedToRun ? (
          <div>
            <Box my={4}>
              <I18n name="dashboard_thankYou" />
              {currentProject && (
                <Box my={3}>
                  <Typography variant="h5">{currentProject.name}</Typography>
                  <Typography component="div">
                    <TypographyMarked md={currentProject.description} />
                  </Typography>
                </Box>
              )}
            </Box>
            <Box my={4}>
              <LoginStatus />
            </Box>
            <Box my={4}>
              <FollowingStatus />
            </Box>
          </div>
        ) : (
          <IntroAfterInstallation />
        )}
      </Box>
      <Footer />
    </div>
  )
}

export default Dashboard
