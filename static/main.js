const base_url = "https://api.jikan.moe/v3";



function searchAnime(event){

	event.preventDefault();

	const form = new FormData(this);
	const query = form.get("search");

	console.log(query);

    fetch(`${base_url}/search/anime?q=${query}&page=1`)
	.then(res=>res.json())
	.then(updateDom)
	.catch(err=>console.warn(err.message));

}


function updateDom(data){


	const searchResult = document.getElementById('search-result');

	const animeByCategories = data.results
        .reduce((acc, anime)=>{

            const {type} = anime;
            if(acc[type] === undefined) acc[type] = [];
            acc[type].push(anime);
            return acc;


		}, {});

			searchResult.innerHTML = Object.keys(animeByCategories).map(key=>{

            const animesHTML = animeByCategories[key]
            .sort((a,b)=>a.episodes-b.episodes)
            .map(anime=>{
                return  `
		    		<div id="card1" class="card1">
            			<a href="${anime.url}"><img id="anime" class="img" src="${anime.image_url}"" alt="${anime.title}"></a>
            			<figcaption id="layer" href="${anime.url}" name="title">${anime.title}</figcaption>
        			</div>`

			}).join("");

				return `
				<section>
					<h3 class="type" >${key.toUpperCase()}<h3>
					<div class="rowcss" >${animesHTML}</div>
				</section`
			}).join("");

}


function pageLoaded(){
	const form = document.getElementById("search_form");
	form.addEventListener("submit", searchAnime);


}

window.addEventListener("load", pageLoaded);