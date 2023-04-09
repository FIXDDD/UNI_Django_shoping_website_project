$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $(".dropdown-trigger").dropdown();
    $('.materialboxed').materialbox();
  })

//*************************************** A ****************************************

$('#sort_form_btn').click(function () {
    $("#sort_form").submit();
})

$('#Login_button').click(function () {
    console.log('submit');
    $('#login_form form').submit();
    })

$('#Register_button').click(function () {
    console.log('submit');
    $('#register_form form').submit();
    })

$('#Change_pw__button').click(function () {
    console.log('submit');
    $('#pw_form form').submit();
    })


/**UI**/
$('.ticket-text').each(function(){
	var words = $(this).text();
    var maxWords = 150;

    if(words.length > maxWords){
        html = words.slice(0,maxWords-1)+'<span class="more_text" style="display:none;"> '+words.slice(maxWords-1, words.length)+'</span>' + '<a href="#" class="read_more">...<br/>[Read More]</a>'

        $(this).html(html)

    	$(this).find('a.read_more').click(function(event){
            $(this).toggleClass("less");
            event.preventDefault();
            if($(this).hasClass("less")){
            	$(this).html("<br/>[Read Less]")
                $(this).parent().find(".more_text").show();
            }else{
            	$(this).html("...<br/>[Read More]")
                $(this).parent().find(".more_text").hide();
            }
        })

    }
})

/** read more read less**/
function AddReadMore() {
    //This limit you can set after how much characters you want to show Read More.
    var carLmt = 300;
    // Text to show when text is collapsed
    var readMoreTxt = " ... Read More";
    // Text to show when text is expanded
    var readLessTxt = " Read Less";


    //Traverse all selectors with this class and manupulate HTML part to show Read More
    $(".addReadMore").each(function() {
        if ($(this).find(".firstSec").length)
            return;

        var allstr = $(this).text();
        if (allstr.length > carLmt) {
            var firstSet = allstr.substring(0, carLmt);
            var secdHalf = allstr.substring(carLmt, allstr.length);
            var strtoadd = firstSet + "<span class='SecSec'>" + secdHalf + "</span><span class='readMore'  title='Click to Show More'>" + readMoreTxt + "</span><span class='readLess' title='Click to Show Less'>" + readLessTxt + "</span>";
            $(this).html(strtoadd);
        }

    });
    //Read More and Read Less Click Event binding
    $(document).on("click", ".readMore,.readLess", function() {
        $(this).closest(".addReadMore").toggleClass("showlesscontent showmorecontent");
    });
}
$(function() {
    //Calling function after Page Load
    AddReadMore();
});
/**read more read less**/









