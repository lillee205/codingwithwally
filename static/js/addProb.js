
//setting up quill rich text editor
var toolBarOptions = [
    ['bold', 'italic', 'underline', 'strike'],
    ['blockquote'],
    [{ 'list': 'ordered' }, { 'list': 'bullet' }]
]
var quill = new Quill("#editor", {
    modules: {
        toolbar: toolBarOptions
    },
    theme: 'snow',
    placeholder: 'Write a description of your prompt. Be as explicit as you can! 50 characters min.'

})
quill.on('text-change', () => {
    $('#desc').val(quill.root.innerHTML)
});

$(function () {
    $('#myform').submit(function (e) {
        //set value of hidden fields for wtforms
        var testCaseInputList = []
        var testCaseOutputList = []
        $('.submittedCase').each(function (index) {
            testCaseInputList.push($(this).find('.inputText')[0].innerText.trim())
            testCaseOutputList.push($(this).find('.outputText')[0].innerText.trim())
        })

        $('#testCaseInputs').val(JSON.stringify(testCaseInputList))
        $('#testCaseOutputs').val(JSON.stringify(testCaseOutputList))
        var testInputList = []
        $('.submittedInput').each(function (index) {
            testInputList.push($(this).find('.inputText')[0].innerText.trim())
        })
        $('#testInputs').val(JSON.stringify(testInputList))

        var testOutputList = []
        $('.submittedOutput').each(function (index) {
            testOutputList.push($(this).find('.outputText')[0].innerText.trim())
        })
        $('#testOutputs').val(JSON.stringify(testOutputList))

    })
    //paginator 
    var currentPg = 1
    $('a').click(async function () {
        var goingForward = $(this).attr('class').includes('next');
        var goingBackward = $(this).attr('class').includes('previous');

        if (goingBackward || (await checkIfValid(currentPg) && goingForward)) {
            $('#step' + currentPg).hide("fast")
            //when clicking pagination arrows, update currentPg
            if (goingBackward && currentPg != 1) {
                if (currentPg == 3) {
                    $('#steps3to5').hide("fast")
                }
                currentPg--
            }
            else if (goingForward && currentPg != 7) {
                if (currentPg == 5) {
                    $('#steps3to5').hide("fast")
                }
                currentPg++
            }

            //changing size of black box depending on page number
            if (currentPg == 1) {
                $('#box').css('width', '40vw')
                $('#box').css('height', '70vh')
            }

            else if (currentPg == 2) {
                $('#box').css('height', '50vh')
                $('#box').css('width', '40vw')


            }
            else if (currentPg >= 3 && currentPg <= 5) {
                $('#box').css('width', '70vw')
                $('#box').css('height', '70vh')
            }
            else if (currentPg == 6) {
                $('#box').css('width', '50vw')
                $('#box').css('height', '70vh')
            }
            else if (currentPg == 7){
                $('#box').css('width', '24vw')
                $('#box').css('height', '28vh')
            }
            else {
                $('#box').css('width', '24vw')
                $('#box').css('height', '60vh')
            }

            //now, show appropriate div
            $('#pgnum').text(`${currentPg}/7`)
            setTimeout(function () {
                if (currentPg == 3 || currentPg == 5) {
                    $('#steps3to5').show("fast")
                }
                $('#step' + currentPg).show("fast")
            }, 300)
        }

    })

    //delete row of input/output
    $(document).on("click", ".trash", function () { //delete row
        $(this).closest('tr').remove()
    })

    //add row of input/output
    $(document).on("click", ".plusCase", function () { //once you check that input and output is valid, replace plus sign with check mark to signify that it is valid
        //check to make sure input and output are valid
        var currObj = $(this)
        var currRow = $(this).closest('tr')
        var input = currRow.children('.inputText').children()
        var output = currRow.children('.outputText').children()

        //send to python server and test
        $.getJSON('/background_process_testCode', {
            code: ace.edit("jsEditor").getValue(),
            input: JSON.stringify(input.val()),
            output: JSON.stringify(output.val()),
        }, function (data) {
            if (data.result == "WALLY RULES!") {
                currRow.addClass('submittedCase')
                $('#error').text('')
                currObj.replaceWith("<img class ='trash' style = 'height: 3em; width: 3em' src ='../static/assets/trashcan.png'>")
                var markup = `
            <tr class="tableTestCases ">
                <td class="inputText ">
                    <textarea style="margin-right: 0; resize: vertical;"></textarea>
                </td>
                <td class="outputText ">
                    <textarea style="margin-right: 0;resize: vertical;"></textarea>
                </td>
                <td class="testText ">
                    <div class= "plus plusCase" id = "plus">
                </td>
            </tr>

            `
                $("#tableTestCases").append(markup)
                input.replaceWith(input.val())
                output.replaceWith(output.val())
            }
            else {
                console.log("error")
                $('#error').text(data.result)
            }
        });

    })

    $(document).on("click", ".plusInput", function () { //once you check that input and output is valid, replace plus sign with check mark to signify that it is valid
        //check to make sure input and output are valid
        var currObj = $(this)
        var currRow = $(this).closest('tr')
        var input = currRow.children('.inputText').children()

        currRow.addClass('submittedInput')
        currObj.replaceWith("<img class ='trash' style = 'height: 3em; width: 3em' src ='../static/assets/trashcan.png'>")
        var markup = `
            <tr class="tableTestInputs ">
                <td class="inputText ">
                    <textarea style="margin-right: 0; resize: vertical;"></textarea>
                </td>
                <td class="testText ">
                    <div class= "plus plusInput" id = "plus">
                </td>
            </tr>
            `
        $("#tableTestInputs").append(markup)
        input.replaceWith(input.val())

    })

    $(document).on("click", ".plusOutput", function () { //once you check that input and output is valid, replace plus sign with check mark to signify that it is valid
        //check to make sure input and output are valid
        var currObj = $(this)
        var currRow = $(this).closest('tr')
        var output = currRow.children('.outputText').children()

        currRow.addClass('submittedOutput')
        currObj.replaceWith("<img class ='trash' style = 'height: 3em; width: 3em' src ='../static/assets/trashcan.png'>")
        var markup = `
            <tr class="tableTestOutputs ">
                <td class="outputText ">
                    <textarea style="margin-right: 0; resize: vertical;"></textarea>
                </td>
                <td class="testText ">
                    <div class= "plus plusOutput" id = "plus">
                </td>
            </tr>
            `
        $("#tableTestOutputs").append(markup)
        output.replaceWith(output.val())

    })
})


async function checkIfValid(currentPg) {
    if (currentPg == 1) {
        if (quill.getText().length < 50) {
            alert("Brevity may be the soul of wit, but in this case, more explanation may be better.")
            return false;
        }
    }
    else if (currentPg == 2) {
        if ($("input:checkbox:checked").length == 0) {
            alert("Please tag your problem appropriately!")
            return false;
        }
    }
    else if (currentPg == 3) {
        //since we need to do a server request to check database, we utilize database to get around javascript's async nature
        var nameValid = await checkName()
        if (nameValid == false) {
            alert("This function name already exists in the database. Please choose a different name.")
            return false;
        }
        if ($('.trash').length < 3) {
            alert("Please write at least three test cases.")
            return false;
        }
        jsEditor = ace.edit("jsEditor")
        jsEditor.setReadOnly(true);
        ace.edit("buggyEditor").getSession().setValue(jsEditor.getSession().getValue())

    }
    return true;
}

function checkName() {
    return new Promise(function (resolve, reject) {
        var code = ace.edit("jsEditor").getValue()
        $.getJSON('/background_process_checkFuncName', {
            func_name: code.slice(code.indexOf("def") + 4, code.indexOf("("))
        }, function (data) {
            flag = true;
            if (data.result == "invalid") {
                flag = false
            }
            resolve(flag)
        })
    })

}