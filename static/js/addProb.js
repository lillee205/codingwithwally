
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
    $('#code').val(quill.root.innerHTML)
});

$(function () {

    //paginator 
    var currentPg = 1
    $('a').click(function () {
        $('#step' + currentPg).hide("fast")
        //when clicking pagination arrows, update currentPg
        if ($(this).attr('class').includes('previous') && currentPg != 1) {
            if (currentPg == 3){
                $('#steps3to5').hide("fast")
            }
            currentPg--
        }
        else if ($(this).attr('class').includes('next') && currentPg != 6) {
            if (currentPg == 5){
                $('#steps3to5').hide("fast")
            }
            currentPg++
        }
        if (currentPg == 1) {
            $('#box').css('width', '40vw')
            $('#box').css('height', '70vh')
        }
        else if (currentPg >= 3 && currentPg <= 5) {
            $('#box').css('width', '70vw')
            $('#box').css('height', '70vh')
        }
        else {
            $('#box').css('width', '24vw')
            $('#box').css('height', '60vh')
        }
        //now, show appropriate div
        $('#pgnum').text(`${currentPg}/9`)
        setTimeout(function () {
            if (currentPg == 3 || currentPg == 5){
                $('#steps3to5').show("fast")
            }
            $('#step' + currentPg).show("fast")
        }, 300)


    })

    //input output 


    $(document).on("click", ".trash", function () { //delete row
        $(this).closest('tr').remove()
    })

    $(document).on("click", ".plus", function () { //once you check that input and output is valid, replace plus sign with check mark to signify that it is valid
        //check to make sure input and output are valid
        var currObj = $(this)
        var currRow = $(this).closest('tr')
        var input = currRow.children('.inputText').children()
        var output = currRow.children('.outputText').children()

        //send to python server and test
        $.getJSON('/background_process_testCode', {
            code: ace.edit("jsEditor").getValue(),
            input: JSON.stringify(eval(input.val())),
            output: JSON.stringify(eval(output.val())),
        }, function (data) {
            if (data.result == "WALLY RULES!") {

                $('#error').text('')
                currObj.replaceWith("<img class ='trash' style = 'height: 3em; width: 3em' src ='../static/assets/trashcan.png'>")
                var markup = `
            <tr>
                <td class="inputText tableTestCases">
                    <textarea style="margin-right: 0; resize: vertical;"></textarea>
                </td>
                <td class="outputText tableTestCases">
                    <textarea style="margin-right: 0;resize: vertical;"></textarea>
                </td>
                <td class="testText tableTestCases">
                    <div class= "plus" id = "plus">
                </td>
            </tr>
            {{form.testInputs}}
            {{form.testOutputs}}
            `
                input.replaceWith(input.val())
                output.replaceWith(output.val())
                $("table tbody").append(markup)
            }
            else {
                console.log("error")
                $('#error').text(data.result)
            }
        });

    })
})