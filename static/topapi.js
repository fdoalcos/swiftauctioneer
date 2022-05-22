const url = "https://api.jikan.moe/v3/top/anime?page=1"


fetch("https://api.jikan.moe/v3/top/anime?page=1")
        .then(res => res.json())
        .then(updateDom)
        .catch(error =>{
            console.log("Error!")
            console.error(error)
        })

function updateDom(data){

    const searchResults = document.getElementById('search-result1')

    searchResults.innerHTML = data.top
    .map(anime=>{
        return `
        <div id="card2" class="card2">
            	<a href="${anime.url}"><img id="anime1" class="img1" src="${anime.image_url}"" alt="${anime.title}"></a>
            	<figcaption class="figcaption" id="layer1" href="${anime.url}" name="title">${anime.title}</figcaption>
        	</div>
        `
    }).join("");


}


