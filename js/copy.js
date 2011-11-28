jQuery.fn.selText = function() {
    var obj = this[0];
    if ($.browser.msie) {
        var range = obj.offsetParent.createTextRange();
        range.moveToElementText(obj);
        range.select();
    } else if ($.browser.mozilla || $.browser.opera) {
        var selection = obj.ownerDocument.defaultView.getSelection();
        var range = obj.ownerDocument.createRange();
        range.selectNodeContents(obj);
        selection.removeAllRanges();
        selection.addRange(range);
    } else if ($.browser.safari) {
        var selection = obj.ownerDocument.defaultView.getSelection();
        selection.setBaseAndExtent(obj, 0, obj, 1);
    }
    return this;
}

$(document).ready(function() {


  //$('.latex-defition').copypaste( 'You have just copied "%copy%" from my page at %url%' );

  //$(".latex").bind('copy', function(){});
  
  //$('.latex-definition').addClass('foobar');


  $('.latex-definition').click(function() {
    //alert("latex-definition");
    //alert($(this).text());
    //$(this).focus();
    //$(this).select();
    $(this).selText().addClass("selected");
    //$(this).html().select();
    //$(this).css("color","yellow");
  
/*
    $(this).focus(function() {
      alert("Handler for .focus() called.");
      $(this).select(function() {
        alert("Handler for .select() called.");
        });
    });
    $(this).bind('copy');
*/
    //selectAllText($(this))
  });

});
