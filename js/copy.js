$(document).ready(function() {
  //$(".latex").bind('copy', function(){});
  
  $(".latex",this).click(function() {
    //$(this).css("color","red");
    $(this).focus(function() {
      //alert("Handler for .focus() called.");
      $(this).select(function() {
        alert("Handler for .select() called.");
        });
    });
    $(this).bind('copy');
    //selectAllText($(this))      
  });
}); 
