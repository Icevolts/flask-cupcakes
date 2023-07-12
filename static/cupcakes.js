const baseURL = 'http://127.0.0.1:5000/api';

function generateCupcakeHTML(cupcake){
    return `<div data-cupcake-id=${cupcake.id}>
    <li> ${cupcake.flavor}/ ${cupcake.size}/ ${cupcake.rating}
    <button class='deleteBtn'>Delete</button></li>
    <img src='${cupcake.image}'> </div>`
}

async function showCupcakeList(){
    const res = await axios.get(`${baseURL}/cupcakes`);
    for(let cupcakeData of res.data.cupcakes){
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $('#cupcakesList').append(newCupcake);
    }
}

$('#addCupcakeForm').on('submit',async function(evt){
    evt.preventDefault();
    let flavor = $('#formFlavor').val();
    let size = $('#formSize').val();
    let rating = $('#formRating').val();
    let image = $('#formImage').val();

    const cupcakeRes = await axios.post(`${baseURL}/cupcakes`,{flavor,size,rating,image});
    let newCupcake = $(generateCupcakeHTML(cupcakeRes.data.cupcake));
    $('#cupcakesList').append(newCupcake);
    $('#addCupcakeForm').trigger('reset');
});

$('#cupcakesList').on('click','.deleteBtn',async function(evt){
    evt.preventDefault();
    let $cupcake = $(evt.target).closest('div');
    let cupcakeId = $cupcake.attr('data-cupcake-id');
    await axios.delete(`${baseURL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(showCupcakeList);