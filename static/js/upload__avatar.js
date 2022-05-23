document.addEventListener('DOMContentLoaded', () => {

    const closeBtn = document.querySelector('.avatar__top i'),
          modalLayout = document.querySelector('.modal__layout'),
          avatarLayout = document.querySelector('.avatar__layout'),
          uploadForm = document.querySelector('.upload__form'),
          file = uploadForm.querySelector('.file'),
          upload = document.querySelector('.upload');


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
        if (e.target.classList.contains('modal__layout')) {
            closeLayout()
        }
    })

    upload.addEventListener('click', (e) => {
        e.preventDefault()
        file.click();
    })
})