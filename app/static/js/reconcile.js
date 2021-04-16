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
    let compEndBal = startBal + reconciledChange
    $('#difference').text(currency(compEndBal));
    return compEndBal;
}
function discrepancyWork(compEndBal, UEndBal) {
    // computes change between computed ending balance and user-entered ending balance as transactions are clicked on
    //if discrepancy = 0 this function will also show finish button
    let discrepancy = currency(UEndBal).subtract(compEndBal)
    if (discrepancy.value === 0.00) {
        $('.finished').show();
    }
    $('#discrepancy').text(discrepancy);
    return discrepancy;
}
function changeHelper(sumChange, startValue, endValue, idArray, recId) {

    if (sumChange !== 0) {
        console.log("sumChange (branch 1):", sumChange);
        let compEndBal = compareBalance(startValue, sumChange);
        let discrepancy = discrepancyWork(compEndBal, endValue);
        $("#reconciledChanges").text(sumChange);
        $.getJSON($SCRIPT_ROOT + '/_reconciled', {
            amount: sumChange,
            idArray: idArray,
            recId: recId,
        }, function (data) {
            // $("#reconciledChanges").text(data.result);
            $('.finished').on('click', function () {
                $.getJSON($SCRIPT_ROOT + '/_reconciled_button', {
                    amount: sumChange,
                    idArray: idArray,
                    recId: recId,
                })
            })
        })
    } else {   
        console.log("sumChange (branch zero):", sumChange);
        let compEndBal = compareBalance(startValue, sumChange);
        let discrepancy = discrepancyWork(compEndBal, endValue);
        $.getJSON($SCRIPT_ROOT + '/_reconciled', {
            amount: sumChange,
            idArray: idArray
        }, function (data) {
            $("#reconciledChanges").text(data.result);
        })
    } }
function compareLength(checkboxValues, totalBoxes) {
    let checkedCount = 0;

    for (const [key, value] of Object.entries(checkboxValues)) {
        if (value === true) {
            checkedCount += 1;
        }
    }

    if (checkedCount > 0) {
        return true

    } else {
        return false
    }
}
//select_all/none functions
function handleButtonClick(checkedCount) {
    if (checkedCount === false) {
        $button.text('check all');
        $(".all_or_none").on("click", function () {
            console.log('we are here');
            checkAll(totalBoxes);
        });
    }
    else {
        $button.text('uncheck all');
        $(".all_or_none").on("click", function () {
            console.log('we are here2');
            uncheckAll(totalBoxes);
        })
    }
}
function checkAll(totalBoxes) {
    for (const [key, value] of Object.entries(totalBoxes)) {
        value['checked'] = true;
        console.log(value['checked']);
    }
}
function uncheckAll(totalBoxes) {
    for (const [key, value] of Object.entries(totalBoxes)) {
        value['checked'] = false;
        console.log(value['checked']);
    }

}

$(document).ready(function () {
    // window.localStorage.clear();

    //set initial state

    $('.finished').hide();  //hides 'finished' button until discrepancy = 0 
    let $button = $("#all_or_none"); //checkall/none button 
    //gathers values from html
    let startValue = selectValues('div.startbal');
    let endValue = selectValues('div.endbal');
    let recId = selectValues('div.recId');
    //set starting values for user-readable boxes
    //loads contents of localStorage into checkboxValues; persistence comes from here
    let checkboxValues = JSON.parse(localStorage.getItem('checkboxValues')) || {};  
    console.log(checkboxValues['buttonText']);
    $button.text(checkboxValues['buttonText']);

    console.log('initial state', checkboxValues);  
    let $checkboxes = $("#checkbox-container :checkbox");
        //checks actual boxes after loading from localStorage
    $.each(checkboxValues, function (key, value) {
            $("#" + key).prop('checked', value);
        });       
        //sets initial state of checkall/none button
    let totalBoxes = document.querySelectorAll('.cbox');
        //get clicked changes from checkboxValues and load them in lower box
    checkedCount = compareLength(checkboxValues, totalBoxes)
        //this should persist checks to box 4 panel box
    universalClick(totalBoxes, checkedCount);
        
    let compEndBal = compareBalance(startValue, 0)
    let discrepancy = discrepancyWork(compEndBal, endValue);
    $('#discrepancy').text(discrepancy);        
   
    //if checkedCount equals 0 > check_all else otherwise show deselect all
    //this should be run at every check click & should update localStorage as well
    function compareLength(checkboxValues, totalBoxes) {
        let checkedCount = 0;
     
        for (const [key, value] of Object.entries(checkboxValues)) {
            if (value === true) {
                console.log(key, value);
                checkedCount += 1;
            }
        }

        if (checkedCount > 0) {
            //true = some boxes checked
            return true

        } else {
            return false
        }
    }
    //select_all/none functions
    function universalClick(totalBoxes, checkedBool) {
        let keyArray = [];
        let idArray = [];
    

        if (checkedBool === false) {
            sumChange = 0
            changeHelper(sumChange, startValue, endValue, [], recId);
  
            
        } 
        else {
            
        console.log('getting checked true')
        checkedBool === true;

        Object.entries(totalBoxes).forEach(([key, value]) => {
            const reducer = (acc, currentVal) => currency(acc).add(currentVal);
            // console.log(key, value.value);

            if (value.checked === true) {
                // console.log(key, value.value);
                keyArray.push(currency(value.value));
                let idElement = value.name
                idArray.push(parseInt(idElement))

                let sumChange = keyArray.reduce(reducer);
                changeHelper(sumChange.value, startValue, endValue, idArray, recId);
            } 
        
          });
        }
    }

    $(".all_or_none").on("click", function () {
        if ($button.text() === 'check all') {
            console.log('check all');
            function checkAll(totalBoxes) {
                keyArray = [];
                valueArray = [];
                for (const [key, value] of Object.entries(totalBoxes)) {
              
                    value['checked'] = true;
                    keyArray.push('option'+ key);
                    valueArray.push(value['checked']);
                    console.log('option'+ key, value['checked']);
                }
                return [totalBoxes, keyArray, valueArray];
            }
            returnValues = checkAll(totalBoxes);
            keyArray = returnValues[1];
            valueArray = returnValues[2];
            checkboxValues = {};
            for (var i = 0; i < keyArray.length; i++)
                checkboxValues[keyArray[i]] = valueArray[i];
            console.log('hash', checkboxValues);
            $button.text('uncheck all');
            checkboxValues["buttonText"] = 'uncheck all';
            console.log(checkboxValues);
            localStorage.setItem("checkboxValues", JSON.stringify(checkboxValues));
            universalClick(returnValues[0], true)
         }
        else {
            console.log('uncheck_all');
            function uncheckAll(totalBoxes) {
                keyArray = [];
                valueArray = [];
                for (const [key, value] of Object.entries(totalBoxes)) {
                    value['checked'] = false;
                    keyArray.push('option' + key);
                    valueArray.push(value['checked']);
                    console.log(value['checked']);
                } return [totalBoxes, keyArray, valueArray];
            }
            returnValues = uncheckAll(totalBoxes);
            keyArray = returnValues[1];
            valueArray = returnValues[2];
            checkboxValues = {};
            for (var i = 0; i < keyArray.length; i++)
                checkboxValues[keyArray[i]] = valueArray[i];
            console.log('hash', checkboxValues);
            $button.text('check all');
            checkboxValues["buttonText"] = 'check all';
            localStorage.setItem("checkboxValues", JSON.stringify(checkboxValues));
            universalClick(returnValues[0], false)

         }
    });
    
     //following handles events from checkboxes, this starts the events
    $('.current').change(function () {
        console.log("The checkbox with the ID " + this.id + " changed " + this.checked);
        checkboxValues[this.id] = this.checked;
   
        localStorage.setItem("checkboxValues", JSON.stringify(checkboxValues));
        checkboxValues = JSON.parse(localStorage.getItem('checkboxValues')) || {};
        checkedBool = compareLength(checkboxValues, totalBoxes); 
        universalClick(totalBoxes, checkedBool);    
        
        
        }
        
        );
    });

