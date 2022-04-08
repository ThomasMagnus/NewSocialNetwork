document.addEventListener('DOMContentLoaded', () => {
    'use strict'

    const choiceLink = document.querySelectorAll('.choiceLink'),
          friendsData = document.querySelector('.friends__data'),
          friendsRequests = document.querySelector('.friends__requests'),
          friendsListBtn = document.querySelector('.friends__listBtn'),
          friendsRequestsBtn = document.querySelector('.friends__requestsBtn');

    const deleteActiveClass = () => {
        choiceLink.forEach(item => {
            item.classList.remove('active')

            item.parentElement.style.border = 'none'
        })
    }

    const getFriendsBtnsActive = e => {
        e.preventDefault()

        const target = e.target
        deleteActiveClass()

        if (target.parentElement.classList[0] === 'friends__listBtn') {

            friendsRequests.style.display = 'none'
            friendsData.style.display = 'block'

            friendsRequestsBtn.style.cssText = `
                border-bottom: 2px solid gray;
                border-left: 2px solid gray;
            `
        } else {
            friendsRequests.style.display = 'block'
            friendsData.style.display = 'none'

            friendsListBtn.style.cssText = `
                border-bottom: 2px solid gray;
                border-right: 2px solid gray;
            `
        }

        target.classList.add('active')
    }

    choiceLink.forEach(item => item.addEventListener('click', e => getFriendsBtnsActive(e)))
})