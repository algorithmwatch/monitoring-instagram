import React from 'react'
import browser from 'webextension-polyfill'
import propTypes from 'prop-types'
import TypographyMarked from './TypographyMarked'
import { Typography } from '@material-ui/core'

const I18n = ({ name, args, componentArg, ...props }) => {
  if (componentArg) {
    let msgArray = getMessage(name, '$$$COMP_PLACEHOLDER$$$').split(
      '$$$COMP_PLACEHOLDER$$$'
    )
    return (
      <>
        <Typography component="span">{msgArray[0]}</Typography>
        {componentArg}
        <Typography component="span">{msgArray[1]}</Typography>
      </>
    )
  } else {
    return <TypographyMarked md={getMessage(name, args)} {...props} />
  }
}

I18n.propTypes = {
  name: propTypes.string.isRequired,
  componentArg: propTypes.element,
  args: propTypes.arrayOf(propTypes.string),
}

export default React.memo(I18n)

export const getMessage = (name, args) => browser.i18n.getMessage(name, args)

// NOTE: useful to check if everything has been marked as translatable
// export const getMessage = (name, args) => '⚠️'
