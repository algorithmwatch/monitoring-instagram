import React from 'react'
import { ThemeProvider } from '@material-ui/core/styles'
import { DataStateProvider } from './hooks/useAddonState'
import Dashboard from './Dashboard'
import theme from '../utils/theme'
import CssBaseline from '@material-ui/core/CssBaseline'

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <DataStateProvider>
        <Dashboard />
      </DataStateProvider>
    </ThemeProvider>
  )
}

export default App
