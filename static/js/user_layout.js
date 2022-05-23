document.addEventListener('DOMContentLoaded', () => {
    'use strict'

    const userMenuArrow = document.querySelector('.user__menu_arrow'),
        userList = document.querySelector('.user__list'),
        userArrow = document.querySelector('.user__menu_arrow i'),
        burger = document.querySelector('.burger'),
        burgerLine = document.querySelectorAll('.burger-line'),
        nav = document.querySelector('.nav'),
        searchInput = document.querySelector('.search__input'),
        searchForm = document.querySelector('.search');

    let searchfriendItem;

    const postData = async (data, url, header) => {
        return await fetch(url, {
            method: 'POST',
            body: data,
            headers: header,
            credentials: 'include',
        })
    }

    const getCookie = () => {

        const getCookieString = name => {
            let cookieValue = null

            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';')
                for (let i = 0; i <= cookies.length - 1; i++) {
                    if (cookies[i].substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookies[i].substring(name.length + 1))
                    }
                }
            }
            return cookieValue
        }

        const headers = new Headers()
        headers.append('X-CSRFToken', getCookieString('csrftoken'))
        return headers
    }

    const showUserMenu = () => {
        userList.classList.toggle('active')
        userArrow.classList.toggle('active__arrow')
    }

    const showBurger = () => {
        burgerLine.forEach(item => {
            item.classList.toggle('active-line')
        })
        nav.classList.toggle('active-menu')
        userList.classList.remove('active')
        userArrow.classList.remove('active__arrow')
    }

    const removeSearchFriendsText = e => {
        const target = e.target

        try {
            if (target.classList !== '.search__friendItem a') {
                document.querySelector('.search__friendList').remove()
            }
        } catch {
        }
    }

    const searchUsers = () => {

        class Users {
            constructor(name, id, avatar, limit = 7) {
                this.name = name;
                this.id = id;
                this.avatar = avatar;
                this.limit = limit;
            }

            createUSer(ul) {

                const createHtml = img => {
                    return (`
                            <a href=http://localhost:8000/friendPage/${this.id}/>
                                <div class="search__img">
                                    <img src="${img}" alt="friend_img">
                                </div>
                                ${this.name}
                            </a>
                        `)
                }

                const html = this.avatar ? createHtml(this.avatar) : createHtml('/static/img/user_logo.jpg');

                const li = document.createElement('li')
                li.classList.add('search__friendItem')
                li.innerHTML = html

                ul.append(li)

            }
        }

        const clearSearchPanel = () => {
            try {
                searchForm.querySelector('.search__friendList').remove()
            } catch (e) {}
        }

        if (searchInput.value.trim()) {

            let dataDict = {
                friendsSearch: searchInput.value.toLowerCase()
            }

            let data = JSON.stringify(dataDict)

            postData(data, 'http://localhost:8000/users/friends/searchFriend/', getCookie())
                .then(response => {
                    console.log(response)
                    return response.json()
                })
                .then(data => {
                    clearSearchPanel()
                    const ul = document.createElement('ul')
                    ul.classList.add('search__friendList')
                    searchForm.append(ul)

                    data.forEach(item => {
                        let users;
                        if (data.length > 7) {
                            users = new Users(item[0], item[1], item[2])
                        } else {
                            users = new Users(item[0], item[1], item[2], data.length)
                        }

                        users.createUSer(ul)
                        console.log(`User: ${item[0]}, id: ${item[1]}`)
                    })

                    searchfriendItem = document.querySelectorAll('.search__friendItem a')
                    searchfriendItem.forEach(item => item.addEventListener('click', e => getFriendPage(e)))

                })
        } else {
            clearSearchPanel()
        }
    }

    const getFriendPage = e => {
        e.preventDefault()
        const target = e.target
        const userID = target.pathname.match(/\d/g).join('')

        const data = JSON.stringify({
            'user_id': userID
        })

        postData(data, target.href, getCookie())
            .then(response => {
                document.location = response.url
            })
    }

    userMenuArrow.addEventListener('click', showUserMenu)
    burger.addEventListener('click', showBurger)
    searchInput.addEventListener('input', searchUsers)
    document.body.addEventListener('click', (e) => removeSearchFriendsText(e))
})