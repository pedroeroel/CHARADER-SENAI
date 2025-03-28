async function getCharade(id) {
    try {
        const url = `https://charader-senai.vercel.app/api/charades`;

        const response = id ? await fetch(`${url}${id}`) : await fetch(url) ;
        const data = await response.json();
        console.log(data);

        const charadeField = document.querySelector('#charadeField')

    }

    catch (e) {
        console.log(e)
    }

    finally {
        if (data) {
            
            charadeField.querySelector('#charade').value = data.charade

        }
    
    return data

    }
}