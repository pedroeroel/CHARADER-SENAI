async function getCharade(id) {
    try {
        const url = `charader-senai-git-main-roels-projects-4fd57707.vercel.app/charades`;

        const response = (id) ? await fetch((url+id)) : await fetch(url) ;
        const data = await response.json();
        console.log(data);
    }

    catch (e) {
        console.log(e)
    }

    return ''
}