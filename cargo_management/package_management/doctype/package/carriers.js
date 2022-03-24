const carriers = {
    'USPS': {
        api: 'EasyPost',
        tracking_urls: [
            {
                "title": "USPS",
                "url": "https://tools.usps.com/go/TrackConfirmAction?tLabels="
            },
            {
                "title": "Parcels",
                "url": "https://parcelsapp.com/en/tracking/"
            },
            {
                "title": "AfterShip",
                "url": "https://www.aftership.com/track/"
            }
        ]
    },
    'FedEx': []
}