export default async function pushCollectedData(collectedUserData) {
  await fetch(`${process.env.BACKEND_URL}/api/v2/donation/`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      data: collectedUserData,
      data_source: '__additionalData',
    }),
  })
}
