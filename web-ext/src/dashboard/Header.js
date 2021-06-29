import React from 'react'
import Box from '@material-ui/core/Box'
import RemoveRedEyeIcon from '@material-ui/icons/RemoveRedEye'
import { getMessage } from './I18n'
import { Typography } from '@material-ui/core'

const Header = () => {
  return (
    <Box component="header" bgcolor="primary">
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <span>
          <Typography variant="h1">{getMessage('extension_name')}</Typography>
          <Typography variant="subtitle1">
            {getMessage('dashboard_subtitle')}
          </Typography>
        </span>
        <RemoveRedEyeIcon style={{ marginRight: 20, width: 42, height: 42 }} />
      </Box>
    </Box>
  )
}

export default Header
