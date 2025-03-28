async function getCharade(id) {
    try {
        const url = `https://charader-senai.vercel.app/api/charades`;

        const response = id ? await fetch(`${url}${id}`) : await fetch(url) ;
        const data = await response.json();
        console.log(data);

        
    }
    
    catch (e) {
        console.log(e)
    }
    
    finally {
        if (data) {
            const charadeField = document.querySelector('#charadeField')
            charadeField.querySelector('#charade').value = data.charade

        }
    
    return data

    }
}