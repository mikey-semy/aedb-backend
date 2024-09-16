document.querySelector('.menu-icon').addEventListener('click', function() {
    document.querySelector('.nav-menu').classList.toggle('active');
});

document.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.getElementById('back-to-top');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    backToTopButton.addEventListener('click', function() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });
});

function getManuals() {
    let response = {
        run: function (url_) {
            let headers = {
                'accept': 'application/json',
            };

            fetch(url_, {
                'method': 'GET',
                'mode': 'cors',
                'credentials': 'include',
                'cache': 'no-cache',
                'headers': headers
            })
            .then(response => this.check(response))
            .then(data => this.success(data))
            .catch(error => this.error(error));
        },

        check: function (response) {
            if (response.status !== 200) {
                console.log('Похоже, возникла проблема. Код состояния: ' + response.status);
                return;
            }
            return response.json();
        },

        success: function (data) {
            console.log('Данные получены!');
            let html = `
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Download</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            data.forEach((manual) => {
                html += `
                        <tr>
                            <td>${manual.title}</td>
                            <td><a href="${manual.file_url}" target="_blank">Download</a></td>
                        </tr>
                `;
            });
            html += `
                    </tbody>
                </table>
            `;
            const container = document.getElementById('manuals-container');
            container.innerHTML = html;
            console.log(data);
        },

        error: function (error) {
            console.log('Ошибка: ', error);
        }
    };

    const url_ = 'https://aedb.ru/manuals';
    console.log(url_);
    response.run(url_);
};