$cupcakeSubmit = $('#cupcake-submit');
$cupcakeForm = $('#cupcake-form');
$cupcakeList = $('.cupcake-list');

let allCupcakes;

class Cupcakes {
    constructor(cupcakes) {
        this.cupcakes = cupcakes;
        this.addCupcakesToDom();
    }

    static async getAllCupcakes(){
        let resp = await axios.get('/api/cupcakes');
        const cupcakes = resp.data.cupcakes;
        return cupcakes;
    }

    addCupcakesToDom(){
        for (let cupcake of this.cupcakes){
            Cupcakes.appendCupcake(cupcake);
        }
    }

    async createCupcake(evt){
        evt.preventDefault()
        
        let resp = await axios.post('/api/cupcakes', Cupcakes.getValues());

        if (resp.status === 201){
            let cupcake = resp.data.cupcake
            Cupcakes.appendCupcake(cupcake)
        }
    }

    static getValues(){
        let newCupcake = {}

        for (let input of $cupcakeForm.children('input:not(#cupcake-submit)')){
            newCupcake[input.id] = input.value;
            input.value='';
        }

        return newCupcake
    }

    static appendCupcake(cupcake){
        const $li = $(`<li id="cupcake-${cupcake.id}">${cupcake.flavor}, ${cupcake.size}, ${cupcake.rating}</li>`);
        const $img = $(`<img src="${cupcake.image}" alt="picture of a ${cupcake.flavor} cupcake">`);
        $li.append($img);
        $cupcakeList.append($li);
    }
}

async function start(){
    allCupcakes = await Cupcakes.getAllCupcakes();
    cupcakes = new Cupcakes(allCupcakes);
    $cupcakeSubmit.click(cupcakes.createCupcake);
}

$(start);


  