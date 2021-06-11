const $kids = $('#holder').children();

$kids.on('click', event => {
  $(event.currentTarget).css('border', '1px solid black);

});
