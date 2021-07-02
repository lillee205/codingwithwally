$(function() {
    $("#rand").bind("click", function() {
        $('input#hiddenSelect').val("rand");
        $("#selectForm").submit()
    })
    $(".select-items div").bind('click', function() {
        $('input#hiddenSelect').val($(this)[0].innerHTML);
        console.log($('input#hiddenSelect').val())
        $("#selectForm").submit()
    });
});

var mini = true;
function toggleSidebar() {
    if (mini) {
        document.getElementById("sidebar").style.width = "260px";
        this.mini = false;
    } else {
        document.getElementById("sidebar").style.width = "48px";
        this.mini = true;
    }
}