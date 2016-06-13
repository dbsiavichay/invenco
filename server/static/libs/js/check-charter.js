var checkCharter = function (charter) {
  if (!charter) return false;
  if (charter.length != 10) return false;

  array = charter.split('');
  num = array.length;

  total = 0;
  digito = (array[9]*1);

  for( i=0; i < (num-1); i++ ) {
    mult = 0;
    if ( ( i%2 ) != 0 ) {
      total = total + ( array[i] * 1 );
    } else {
      mult = array[i] * 2;
      if ( mult > 9 ) total = total + ( mult - 9 );
      else total = total + mult;
    }
  }

  decena = total / 10;
  decena = Math.floor( decena );
  decena = ( decena + 1 ) * 10;
  final = ( decena - total );

  if (( final == 10 && digito == 0 ) || ( final == digito ))
    return true;
  else
    return false;
}
