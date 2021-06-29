import React from 'react'
import ReactDOM from 'react-dom'
import { ThemeProvider } from '@material-ui/core/styles'
import CssBaseline from '@material-ui/core/CssBaseline'
import Typography from '@material-ui/core/Typography'
import Box from '@material-ui/core/Box'
import I18n, { getMessage } from '../dashboard/I18n'
import theme from '../utils/theme'

const App = () => {
  React.useEffect(() => {
    document.title = getMessage('extension_name')
  }, [])
  return (
    <>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box my={8} mx={4}>
          <Typography variant="h1">{getMessage('extension_name')}</Typography>
          <Box mt={6}>
            <I18n name="dashboard_doNotClosePage_body" />
          </Box>
        </Box>
      </ThemeProvider>
    </>
  )
}
ReactDOM.render(<App />, document.getElementById('app'))
