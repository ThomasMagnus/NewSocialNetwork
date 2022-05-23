const formData = JSON.stringify({id: 363493})

const headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 YaBrowser/22.3.0.2434 Yowser/2.5 Safari/537.36',
    'X-CSRFToken': 'wU4xpmSTjGAPALU3HGIyVpZkWFrDvtwKGCMdzi2976wx9egdF2GvSRG5LhnV768f',
}

fetch("http://localhost:8000/friendPage/friend/search/", {
    method: 'POST',
    body: formData,
    headers: headers,
    credentials: 'include',
})
    .then(response => console.log(response))