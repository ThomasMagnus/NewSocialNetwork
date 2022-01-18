document.addEventListener('DOMContentLoaded', () => {
    'use strict'

    const userCover = document.querySelector(".userCover"),
          userCoverEdit = document.querySelector(".userCover__edit_wrapper"),
          editDots = document.querySelectorAll('.fa-ellipsis-v'),
          ellipsisList = document.querySelectorAll('.ellipsis__list'),
          editPostElem = document.querySelectorAll('.edit-post'),
          faTrash = document.querySelectorAll('fa-trash-o'),
          contentCancel = document.querySelectorAll('.cancel__wrapper'),
          communityLink = document.querySelectorAll('.community__link'),
          contentBtn = document.querySelector('.content__btn'),
          comment = document.querySelector('#comment'),
          content__form = document.querySelector('.content__form');

    let target, parentElement, contentTextEdit, contentPanel;

    const showEdit = () => {
        userCoverEdit.classList.toggle('edit__active')
    }

    const hideEdit = () => {
        userCoverEdit.classList.remove('edit__active')
    }

    const announceVars = e => {
        target = e.target
        parentElement = target.closest('.content__item')
        contentTextEdit = parentElement.querySelector('.content__text-edit')
        contentPanel = parentElement.querySelector('.content__panel')
    }

    const showEditDotsMessege = e => {

        let index = detectDotsMessage()

        announceVars(e)

        const element = target.parentElement.querySelector('.ellipsis__list')

        if (index && ellipsisList[index] == element) {
            element.classList.remove('active_disp')
            return
        }

        element.classList.add('active_disp')
    }

    const detectDotsMessage = () => {
        let indexElem;

        ellipsisList.forEach((item, i) => {
            if (item.classList.contains('active_disp')) {
                item.classList.remove('active_disp')
                indexElem = i
            }
        })

        return indexElem

    }

    const editPost = e => {

        announceVars(e)

        const element = parentElement.querySelector('.content__text')
        const texarea = document.createElement('textarea')
        const contentTextEdit = parentElement.querySelector('.content__text-edit')
        const contentPanel = parentElement.querySelector('.content__panel')

        detectDotsMessage()
        element.style.display = 'none'

        texarea.classList.add('edit__content')
        texarea.value = element.textContent
        contentTextEdit.before(texarea)

        contentPanel.style.display = 'flex'
    }

    const cancelEditPost = e => {
        announceVars(e)

        const element = parentElement.querySelector('.edit__content')
        const contentText = parentElement.querySelector('.content__text')
        element.remove()

        contentPanel.style.display = 'none'
        contentText.style.display = 'block'
    }

    userCover.addEventListener("mouseenter", showEdit)
    userCover.addEventListener("mouseleave", hideEdit)

    editDots.forEach(element => {
        element.addEventListener('click', showEditDotsMessege)
    });

    editPostElem.forEach(item => {
        item.addEventListener('click', editPost)
    })

    contentCancel.forEach(item => {
        item.addEventListener('click', cancelEditPost)
    })

    const postData = e => {
        e.preventDefault()

        const getCookie = name => {
            let cookieValue = null
            
            if (document.cookie && document.cookie != '') {
                const cookies = document.cookie.split(';')
                for (let i=0; i <= cookies.length - 1; i++) {
                    if (cookies[i].substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookies[i].substring(name.length + 1))
                    }
                }
            }

            return cookieValue
        }
        // Заголовки для CORS
        const headers = new Headers()
        headers.append('X-CSRFToken', getCookie('csrftoken'))

        const formData = new FormData(content__form)

        fetch('http://localhost:8000/createPost/', {
            method: 'POST',
            body: formData,
            headers: headers,
            credentials: 'include'
        })
        .then(response => {
            console.log(response)
            document.location.reload()
        })
    }

    contentBtn.addEventListener('click', e => {
        postData(e)
    })
})