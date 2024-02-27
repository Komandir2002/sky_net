let rating = 0;

function getCookie(name) {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            ratedScore = cookie.substring(name.length + 1);
            const textElement = document.querySelector('.text');
            if (textElement) {
                textElement.innerHTML = `<p>Ваша оценка ${ratedScore}/5👍</p>`;
                for (let i = 0; i <= ratedScore; i++) {
                    stars[i].className = 'star-selected';
                }
            }
            rating = cookie.substring(name.length + 1);
            console.log(cookie.substring(name.length + 1));
            return cookie.substring(name.length + 1);
        }
    }
    console.log(0);
    return 0;
}

if (getCookie() === 0) {
    document.querySelectorAll('.star').forEach(item => {
        item.addEventListener('click', function () {
            const score = this.getAttribute('data-value');
            const applicationId = this.parentNode.getAttribute('data-application-id');
            fetch(`/rate-application/${applicationId}/`, {
                method: 'POST',
                body: JSON.stringify({'score': score}),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    document.cookie = `rating=${score};`;
                    ratedScore = Number(score);
                    updateRating(ratedScore);
                })
                .catch(error => console.error('Error:', error));
        }, {once: true});
    });
}