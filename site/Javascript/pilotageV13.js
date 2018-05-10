// version sans la gestion de la tete verticalement par la souris

var socket = new WebSocket('ws://' + adr + ':8080');
var dply = 1;
var dplx = 1;
var pos = 1;
var action =1;
var headX = 1;
console.log(adr);
var message = "";
var numero = "";

socket.onopen = function()
{
	var handshake =
	"GET / HTTP/1.1\n" +
	"Host: " + adr + " \n" +
	"Upgrade: websocket\n" +
	"Connection: Upgrade\n" +
	"Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\n" +
	"Sec-WebSocket-Protocol: quote\n" +
	"Sec-WebSocket-Version: 13\n" +
	"Origin: http://127.0.0.1\n";

		socket.send(handshake);
};

var x,y, xlast, ylast = 0;
var x = 0;
var y = 0;
var theta=0;
var tete=0;

var state = false;
var cursorX;
var cursorY;

var x,y, xlast, ylast = 0;
var x = 0;
var y = 0;
var theta = 0;
var tete = 0;
var command = "";

document.onmousemove = function(e)
{
	cursorX = e.pageX;
	cursorY = e.pageY;
}

function tts()
{
    var msg = document.getElementById("tts").value;
    socket.send('8' + msg);
}

function behavior(name)
{
    console.log(name);
    socket.send('7' + name);
}

function maintenancebehavior(name)
{
    console.log(name);
    socket.send('7' + name);
}


var cursorX;
var cursorY;

document.onmousemove = function(e)
{
	cursorX = e.pageX;
	cursorY = e.pageY;
}

var x,y, xlast, ylast = 0;
var x = 0;
var y = 0;
var theta=0;
var tete=0;

var x,y, xlast, ylast = 0;
var x = 0;
var y = 0;
var theta=0;
var tete=0;
var command="";

function calc()
{
	xlast = cursorX -x;
	ylast = cursorY -y;
	command=""
	console.log(ylast + " Différence" + xlast)
	//console.log(cursorY + " Actuel" + cursorX)
	x = cursorX;
	y = cursorY;

	if(theta == 1)
	{
		command= "121"
		theta = 0
	}
	else
	{
		if(xlast < -30)
		{
			command = "120"
			theta = 1
		}
		if(xlast > 30)
		{
			command = "122"
			theta = 1
		}
	}
	
/*	if(ylast < -30)
	{
		command = command + "90"
	}
	if(ylast > 30)
	{
		command = command + "91"
	}
	
*/
	if(command != "")
	{
		socket.send(command)
	}

}
window.setInterval("calc()", 500);


document.onkeyup = keyup;
		
function keyup(e)
{
	e = e || window.event;
	
	if(action == 0)
	{
		if (e.keyCode == '27')
		{
			//Echap
			action = 1;
			socket.send("stop");
		}
	}
	
	if(headX == 0)
	{
		if (e.keyCode == '65')
		{
			socket.send("61");
			headX = 1;
		}
		if (e.keyCode == '69') 
		{
			socket.send("61");
			headX = 1;
		}
	}

	
	if(dply == 0)
	{
	
		if (e.keyCode == '90')
		{
			//Z
			socket.send("111");
			dply = 1;
		}
		if (e.keyCode == '83') 
		{
			//S
			socket.send("111");
			dply = 1;
		}
	}
	if(dplx == 0)
	{
		
		if (e.keyCode == '81') 
		{
			//Q
		   socket.send("101");
		   dplx = 1;
		}
		if (e.keyCode == '68') 
		{
			//D
		   socket.send("101");
		   dplx = 1;
		}
	}
	
	if(pos == 0)
	{
		if (e.keyCode == '67') 
		{
		   pos = 1;
		}
		
		if (e.keyCode == '16') 
		{
		   pos = 1;
		}
		
		if (e.keyCode == '17') 
		{
		   pos = 1;
		}
	}
};
	
document.onkeydown = keydown;

function keydown(a)
{

		a = a || window.event;
			
		if(action == 1)
		{
			if (a.keyCode == '27')
			{
				//Echap
				action = 0;
				socket.send("0");
			}
		}
		
		if(dply == 1)
		{
		
			if (a.keyCode == '90')
			{
				socket.send("112");
				dply = 0;
			}
			if (a.keyCode == '83') 
			{
				socket.send("110");
				dply = 0;
			}
		}
		
		if(headX == 1)
		{
		
			if (a.keyCode == '69')
			{
				socket.send("60");
				headX = 0;
			}
			if (a.keyCode == '65') 
			{
				socket.send("62");
				headX = 0;
			}
		}
		
		if(dplx == 1)
		{
			if (a.keyCode == '81') 
			{
			   socket.send("102");
			   dplx = 0;
			}
			if (a.keyCode == '68') 
			{
			   socket.send("100");
			   dplx = 0;
			}
		}
		if(pos == 1)
		{
			if (a.keyCode == '67') 
			{
			   socket.send("40");
			   pos = 0;
			}
			
			if (a.keyCode == '17') 
			{
			   socket.send("41");
			   pos = 0;
			}
			
			if (a.keyCode == '16') 
			{
			   socket.send("42");
			   pos = 0;
			}
		}
}
		
	  /*  var canvas = document.getElementById("canvas");
		canvas.addEventListener("mousemove", function(e) {
				console.log(e.pageX, e.pageY); 
				}
				);*/
				
		   /*     function mouse_position()
{
var r = window.event;

var posX = r.clientX;
var posY = r.clientY;

document.Form1.posx.value = posX;
document.Form1.posy.value = posY;

var t = setTimeout("mouse_position()",100);

}*/


/*
var img="NAO"; // ici nom de l'image a recharger
var src="image0.png"
var mon_image = new Image();
var canvas = document.getElementById('imageNAO');
var context = canvas.getContext('2d');
var titi = true;

var canvas = document.getElementById('imageNAO');
if(!canvas)
{
	alert("Impossible de récupérer le canvas");
}

var context = canvas.getContext('2d');
if(!context)
{
	alert("Impossible de récupérer le context du canvas");
}

socket.onmessage = function(msg)
{
	console.log(msg.data);
	numero = msg.data.split("-")[1];
	message = msg.data.split("-")[0];
	
	if(message == "sys")
	{
		refreshImage(numero);
		titi = false;
		console.log("Rafrachi l'image");
	}
	else
	{
		var img = context.createImageData(320, 240);
		refreshImage(msg.data, img);
	}
}

function refreshImage(array, img) 
{
	
	var arrayBuf = array;
	var tpx = 320 * 240;
	var uint8array = new Uint8Array(arrayBuf);
	for (var j = 0; j < tpx; j++) 
	{
		img.data[j * 4] = uint8array[j * 3];
		img.data[j * 4 + 1] = uint8array[j * 3 + 1];
		img.data[j * 4 + 2] = uint8array[j * 3 + 2];
		img.data[j * 4 + 3] = 200;
	}
	context.putImageData(img, 0, 0);
}*/

