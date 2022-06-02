document.addEventListener('DOMContentLoaded', () => {

    const closeBtn = document.querySelector('.avatar__top i'),
          modalLayout = document.querySelector('.modal__layout'),
          avatarLayout = document.querySelector('.avatar__layout'),
          uploadForm = document.querySelector('.upload__form'),
          file = uploadForm.querySelector('.file'),
          upload = document.querySelector('.upload'),
          uploadDone = document.querySelector('.upload__done'),
          refreshImg = document.querySelectorAll('.refresh_img'),
          uploadNoImg = document.querySelector('.upload__noImg'),
          uploadTitle = document.querySelector('.upload__title'),
          uploadTrash = document.querySelector('.upload_trash');


    const closeLayout = () => {
        modalLayout.style.display = 'none'
        document.body.style.overflow = ''
    }

    avatarLayout.addEventListener('click', () => {
        modalLayout.style.display = 'block'
        document.body.style.overflow = 'hidden'
    })

    closeBtn.addEventListener('click', () => {
        closeLayout()
    })

    modalLayout.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal__container')) {
            closeLayout()
        }
    })

    upload.addEventListener('click', (e) => {
        e.preventDefault()
        file.click();
    })

    uploadForm.addEventListener('change', (e) => {
        e.preventDefault()

        const data = new FormData(uploadForm)

        fetch('http://localhost:8000/users/changeAvatar/buffer', {
            method: 'POST',
            body: data
        })
            .then(response => response.text())
            .then(data => {

                refreshImg.forEach(item => {
                    const img = document.createElement('img')
                    img.setAttribute('src', data)
                        item.append(img)
                })

                uploadNoImg.style.display = 'none'
                uploadTitle.style.display = 'block'
                uploadTrash.style.display = 'block'
            })

    })

    uploadDone.addEventListener('click', () => {

        const data = new FormData(uploadForm)

        fetch('http://localhost:8000/users/changeAvatar/photo', {
            method: 'POST',
            body: data,
        })
            .then(response => {
                console.log(response)
                location.reload()
            })
    })


    uploadTrash.addEventListener('click', (e) => {
        e.preventDefault()

        fetch('http://localhost:8000/users/changeAvatar/buffer/del')
            .then(response => {
                console.log(response)
                return response.text()
            })
            .then(data => {

                refreshImg.forEach(item => item.remove())
                uploadNoImg.style.display = 'block'
                uploadTitle.style.display = 'none'
                uploadTrash.style.display = 'none'
            })
    })
})