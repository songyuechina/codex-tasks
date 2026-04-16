
function msgon( msgtype ) {
  if( msgtype == 1 ) { msg1.innerText = "Can be contained in "+oname+" ..."; }
  if( msgtype == 2 ) { msg1.innerText = oname+ " can contain ..."; }
  if( msgtype == 3 ) { msg1.innerText = "Automation interfaces supported by "+oname+" ..."; }
}

function msgoff(  ) {
  msg1.innerText = "";
}
function showprop( url ) {
w1 = open(url,"prop","toolbar=no,location=no,directories=no,status=yes,menubar=no,scrollbars=yes,resizable=yes,width=600,height=400");
w1.focus();
}

