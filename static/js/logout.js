document.addEventListener('DOMContentLoaded', () => {
    const logout = document.querySelectorAll('.logout')

    const logoutUser = e => {
        e.preventDefault()

        fetch('http://localhost:8000/users/')
            .then(response => {
                document.location = response.url
            })
    }

    logout.forEach(item => {
        item.addEventListener('click', logoutUser)
    })
})