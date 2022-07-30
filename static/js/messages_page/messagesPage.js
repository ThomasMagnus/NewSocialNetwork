document.addEventListener('DOMContentLoaded', () => {
    'use strict'

    const main = () => {

        const get_chats_data = () => {
            fetch('chats/')
                .then(response => {
                    console.log(response)
                    return response.json()
                })
                .then(data => {
                    console.log(data)
                })
        }

        get_chats_data()
    }

    main()
})