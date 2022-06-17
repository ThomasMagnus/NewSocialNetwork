document.addEventListener('DOMContentLoaded', () => {
    const photosBtn = document.querySelector('.photos__btn'),
          photosList = document.querySelector('.photos__list'),
          photosForm = document.querySelector('.photos__form'),
          modalPhoto = document.querySelector('.modalPhoto'),
          modalPhotoImg = document.querySelector('.modalPhoto__img img'),
          photosInput = document.querySelector('.file'),
          photosLink = document.querySelector('.photos__link'),
          photosAdd = document.querySelector('.photos__add'),
          trashBtn = document.querySelector('.fa-trash'),
          imgWrapper = document.querySelector('.img__wrapper');

    let photosItem = document.querySelectorAll('.photos__item');
    let photoCount = 0

    document.querySelector('.errorlist').remove()

    const postData = async (url, body) => {
        const result = await fetch(url, {
            method: 'POST',
            body,
        })

        if (result.status !== 200) throw new Error(`Ошибка отправки запроса: ${result.statusText}`)

        return result.json()
    }

    const getAllPhotos = (e) => {
        e.preventDefault()

        photoCount += 6

        let data = new FormData(photosForm)
        data.append('photoCount', photoCount)

        postData('http://localhost:8000/photo/allPhoto/', data)
            .then(data => {
                data['all_photos'].forEach(item => {
                    const html = `
                        <li class="photos__item">
                            <div class="photos__img">
                                <img src=${ item } alt="">
                            </div>
                        </li>
                    `
                    photosList.innerHTML += html
                })
                photosItem = document.querySelectorAll('.photos__item');

                photosItem.forEach(item => {
                    item.addEventListener('click', e => showPhoto(e))
                })
                console.log(photosItem)
                if (data['pagination'] === false) photosBtn.remove()
            })
    }

    const showPhoto = (e) => {
        const target = e.target
        modalPhoto.style.display = 'flex'

        const srcPath = target.getAttribute('src')
        const dataId = target.dataset.id

        modalPhotoImg.setAttribute('src', srcPath)
        modalPhotoImg.setAttribute('data-id', dataId)
    }

    const hidePhoto = (e) => {
        const target = e.target
        if (target.className === 'modalPhoto') modalPhoto.style.display = 'none'
    }

    photosItem.forEach(item => item.addEventListener('click', e => showPhoto(e)))

    const getPhotoInput = (e) => {
        e.preventDefault()
        photosInput.click()
    }

    const addPhotos = (e) => {
        e.preventDefault()
        const data = new FormData(photosAdd)

        postData('http://localhost:8000/photo/addPhoto/', data)
            .finally(() => document.location.reload())
    }

    const mouseHover = (e) => {
        const target = e.target
        if (target.tagName === 'IMG' || target.tagName === 'I' || target.className === 'img__wrapper') trashBtn.style.opacity = '1'
    }
    const mouseHide = () => trashBtn.style.opacity = '0'

    const removePhoto = () => {
        const dataset = modalPhotoImg.dataset.id

        postData('http://localhost:8000/photo/delPhoto/', JSON.stringify({photoId: dataset}))
            .then(response => console.log(response))
            .finally(() => document.location.reload())
    }

    photosBtn.addEventListener('click', (e) => getAllPhotos(e))

    modalPhoto.addEventListener('click', e => hidePhoto(e))

    photosLink.addEventListener('click', e => getPhotoInput(e))

    photosInput.addEventListener('change', addPhotos)

    imgWrapper.addEventListener('mouseenter', mouseHover)

    imgWrapper.addEventListener('mouseleave', mouseHide)

    trashBtn.addEventListener('click', removePhoto)
})