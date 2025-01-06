function tweetar(id) {
    const tweetInput = document.querySelector('.tweet-box textarea');
    const content = tweetInput.value.trim();
    fetch(`/commentary/?id=${id}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        location.reload(); 
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });
}

function redirectToComentaries(param) {
    const baseUrl = '/comments/';
    const queryParam = `?param=${param}`;
    window.location.href = baseUrl + queryParam;
}

function liked(id) {
    fetch(`/toggle-like/?id=${id}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let tweetElement = document.querySelector(`#tweet-${id}`);
            let likeIcon = tweetElement.querySelector('.like-icon');

            likeIcon.classList.add('pulsing');

            setTimeout(() => {
                likeIcon.classList.remove('pulsing');
            }, 500); 

           
            if (data.isLiked) {
                likeIcon.classList.remove('bi-suit-heart');
                likeIcon.classList.add('bi-heart-fill');
                likeIcon.classList.add('heart-liked');
                likeIcon.classList.remove('heart');
            } else {
                likeIcon.classList.remove('bi-heart-fill');
                likeIcon.classList.add('bi-suit-heart');
                likeIcon.classList.add('heart');
                likeIcon.classList.remove('heart-liked');
            }
        } else {
            console.error('Erro:', data.error);
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });
}