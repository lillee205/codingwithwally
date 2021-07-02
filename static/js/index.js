var activeTags = []
$(function () {
    //redirect to right problem pg
    $('.flexchild').click(function (e) {
        e.preventDefault()
        window.location.href = "/prob/" + $(this).children('h4').text()
    })
    //admin delete
    var currFunc = ""
    $('.x').click(function (e) {
        currFunc = $(this).parent().children('h4').text()
        $('#delPopup').fadeIn("fast")
        e.stopPropagation();
    })
    $(".delBtn").click(function () {
        if ($(this)[0].innerText == "yes") {
            window.location.href = "/";
            $.getJSON('/background_process_delete', {
                func_name: currFunc,
            }, function (data) {
                currFunc = ""
            })
        }
        else {
            currFunc = ""
            $('#delPopup').fadeOut("fast")
        }
    })
    //admin add
    $("#plus").click(function () {
        console.log("h")
        $('#addPopup').fadeIn("fast")
    })
    $(".addBtn").click(function () {
        if ($(this)[0].innerText == "yes") {
            window.location.href = "/addProb";
        }
        else {
            $('#addPopup').fadeOut("fast")
        }
    })
    var yellow = "rgb(255, 181, 49)"
    var pink = "rgb(220, 37, 106)"
    $(".tag").click(function () { // filtering system
        
        var currentColor = $(this).css("background-color")
        var newColor = ""
        var currTag = $(this)[0].innerText
        console.log("currTag is " + currTag)
        if (currentColor == pink) {
            newColor = yellow
            activeTags.push(currTag)
        }
        else {
            newColor = pink
            activeTags.splice(activeTags.indexOf(currTag), 1)
        }

        $(this).css('background-color', newColor);

        if ($(".tag[style='background-color: rgb(255, 181, 49);']").length == 0) { //if no tags are selected, show all
            $('.flexchild').show()
        }
        else {
            $('.flexchild').hide()
            $(".flexchild").each(function () {
                tagBox = $(this).find(".tagsSmallFlex")
                tags = []
                $(tagBox).children().each(function () {
                    tags.push($(this)[0].innerText)
                })

                let checker = (arr, target) => target.every(v => arr.includes(v)); //checks to see if all the tags in activetags are in the current problem tags
                if (checker(tags, activeTags)) {
                    $(this).show()
                }
            })
        }
        if ($(".flexchild:visible").length == 0) { //if no tag results match, then show this message that nothing matches
            $('#nothing').show()
        }
        else {
            $('#nothing').hide()
        }

    })

})