import { postMessage } from './common'

let user = window._sharedData.entry_data.ProfilePage[0].graphql.user
let igUsername = user.username
let isFollowing = user.followed_by_viewer

postMessage({ igUsername, isFollowing, userData: user })
