//reconcile.html functions
function selectValues(querySelector) {
    // use to set startValue (starting balance) and endValue (ending balance)
    const returnArray = document.querySelectorAll(querySelector);
    
    returnArray.forEach(function (element) {
        let returnBal = currency(element.getAttribute('value'));
        returnValue = returnBal.value;
    });
    return returnValue;
}

function compareBalance(startBal, reconciledChange) {
    // computes change between starting balance and computed ending balance as transactions are clicked on
    let compEndBal = startBal + reconciledChange;
    $('#reconciledChanges').text(currency(reconciledChange));
    $('#difference').text(currency(compEndBal));
    return compEndBal;
}

function discrepancyWork(compEndBal, UEndBal) {
    // computes change between computed ending balance and user-entered ending balance as transactions are clicked on
    //if discrepancy = 0 this function will also show finish button
    let discrepancy = currency(UEndBal).subtract(compEndBal);
    if (discrepancy.value === 0.00) {
        $('.finished').show();
    }
    $('#discrepancy').text(discrepancy);
    return discrepancy;
}

function stateOnLoad() {
    //can it tell me which boxes are checked
    //get idArray
    //get amountArray
    idArray = [];
    amountArray = [];
    let totalBoxes = document.querySelectorAll('.cbox');
    
    $.each(totalBoxes, function (key, value) {
        const amount = currency(value.value);
        const id = parseInt(value.name);
        if (value.checked === true) {
            idArray.push(id);
            amountArray.push(amount);
        } else {
            console.log();
        }
        
    }
    
    );
    return [idArray, amountArray, totalBoxes];
}

function stateOnChange(startValue, endValue) {
    //really just a wrapper for stateOnLoad functions
    const threeArrays = stateOnLoad();

    const idArrayOnload = threeArrays[0];
    const amountArrayOnload = threeArrays[1];
    const totalBoxesOnload = threeArrays[2];

    const reconciledChange = amountArrayOnload.reduce(reducer);

    let compEndBal = compareBalance(startValue, reconciledChange.value)
    let discrepancy = discrepancyWork(compEndBal, endValue);
    $('#discrepancy').text(discrepancy);

    return [idArrayOnload, reconciledChange.value];


}

const reducer = (acc, currentVal) => currency(acc).add(currentVal);


$(document).ready(function () {
    // window.localStorage.clear();

    $('.finished').hide();  //hides 'finished' 
    //gathers values from html; these values loaded from flask
    let startValue = selectValues('div.startbal');
    let endValue = selectValues('div.endbal');
    let recId = selectValues('div.recId');

    //just persist

    //on document.ready, this gets checkboxValues fro lS
    let checkboxValues = JSON.parse(localStorage.getItem('checkboxValues')) || {};
    //this actually populates the boxes
    $.each(checkboxValues, function (key, value) {
        $("#" + key).prop('checked', value);
    });

    const threeArrays = stateOnLoad();

    const idArrayOnload = threeArrays[0];
    const amountArrayOnload = threeArrays[1];
    const totalBoxesOnload = threeArrays[2];

    const reconciledChange = amountArrayOnload.reduce(reducer);

    let compEndBal = compareBalance(startValue, reconciledChange.value)
    let discrepancy = discrepancyWork(compEndBal, endValue);
    $('#discrepancy').text(discrepancy);


    $('.current').on('click', function () {
        if (discrepancy.value !== 0.00) {
            $('.finished').hide();
        }

        checkboxValues[this.id] = this.checked; //applies checked value to attribute id, this refers to 'clicked' .current element, this is what we are loading into localStorage
        singleValueChecked = currency(this.value);
        stateOnChange(startValue, endValue);

        localStorage.setItem("checkboxValues", JSON.stringify(checkboxValues));

    });

    $('#finished').on('click', function () {
        console.log('somthing');
        //this is the snapshot 
        twoArrays = stateOnChange(startValue, endValue);
        const idArrayFinal = twoArrays[0];
        const sumFinal = twoArrays[1];

        $.getJSON($SCRIPT_ROOT + '/_reconciled_button', {
            amount: sumFinal,
            idArray: idArrayFinal,
            recId: recId,
        });
    })




});