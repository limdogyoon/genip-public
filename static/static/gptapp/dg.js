function myEnterPress(event) {
  if (event.key === 'Enter') {
/*    document.getElementById("myForm").submit();
    document.getElementsByTagName("html")[0].style.cursor = "wait";*/
    FormSubmit()
  }
}

function changeRight(string) {
  document.getElementById("param_selected").innerHTML = string;
  document.getElementById("param").value = string;
}

function FormSubmit(){
    document.getElementById('popup').style.display = "block";
    document.getElementsByTagName("body")[0].style.cursor = "wait";
    document.getElementById('myForm').submit()
}

function myStop(){
    window.stop();
    document.getElementsByTagName("body")[0].style.cursor = "";
    document.getElementById('popup').style.display = "none";
}

/*
document.getElementById("question").focus();
*/

/*
function myTabPress(event) {
  if (event.key === 'Tab') {
    document.getElementById("question").focus();
  }
}*/

function myCopy(output) {
  var copyText = document.getElementById(output);
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile devices
  navigator.clipboard.writeText(copyText.value);
  toast("The text copied : \n" + copyText.value);
}


function isKeyPressed(event) {
  if (event.ctrlKey && event.key === 'Enter') {
    FormSubmit()
    /*document.getElementById("myForm").submit();
    document.getElementsByTagName("html")[0].style.cursor = "wait";*/
  } 
  if (event.key === 'Escape') {
    myReset();
  }
/*  if (event.key === 'Tab') {
    document.getElementById("answer").focus();
  }*/
}


function showSub(menu_name) {
  var x = document.getElementById(menu_name);
  if (x.style.visibility === 'hidden') {
    x.style.visibility = 'visible';
    document.getElementById('menu_sub2_2').style.visibility = 'visible';
    document.getElementById('menu_sub2_3').style.visibility = 'visible';
  } else {
    x.style.visibility = 'hidden';
    document.getElementById('menu_sub2_2').style.visibility = 'hidden';
    document.getElementById('menu_sub2_3').style.visibility = 'hidden';
  }
}

function changeColor() {
  var x = document.getElementById("menutext")
  x.fill = 'black';
}//defunct

// Make the DIV element draggable:
dragElement(document.getElementById("menu"));

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "_inside")) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id + "_inside").onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}
//draggable ends

//tab change
function openContent(evt, conName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById("answer").value = document.getElementById(conName).value;
  evt.currentTarget.className += " active";
}