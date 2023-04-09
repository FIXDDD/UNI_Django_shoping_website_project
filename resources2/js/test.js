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






