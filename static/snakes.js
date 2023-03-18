function draw_piece(ctx, v, n, c) {	
	let x = 0;
	let y = 0;
	let x_off = 0;
	let y_off = 0;
	
	v -= 1;
	if (v < 0) {
		x = 0; y = 9;
	} else {
		x = (v % 20 < 10) ? (v % 10) + 1 : 10 - (v % 10);
		y = 9 - Math.floor(v / 10);
	}
	
	n -= 1;
	x_off = n % 2;
	y_off = Math.floor(n / 2);
	
	ctx.beginPath();
	ctx.arc(10 + 60 * x + x_off * 37 + 1, 11 + 60 * y + y_off * 37 + 1, 10, 0, 2 * Math.PI);
	ctx.fillStyle = c;
	ctx.fill();
}

function show_dices() {
	const dices = ['🎲', '⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
	document.querySelectorAll(".dice").forEach(
		elem => {			
			elem.innerHTML = dices[elem.getAttribute('value')];
		}
	);
}

function produce_dices(target_name, dices) {
	let target_div = document.getElementById(target_name);
	target_div.innerHTML = '';
	dices.forEach(
		dice => {
			let elem = document.createElement('span');
			elem.className = 'dice';
			elem.setAttribute('value', dice); 			
			target_div.appendChild(elem);
		}
	)
}

function graph(d) {
	let canvas = document.getElementById("board");
	let ctx = canvas.getContext("2d");
	let img = document.getElementById("snakedraw");
	ctx.drawImage(img, 0, 0);
	draw_piece(ctx, d.pos1, 1, 'darkmagenta');
	draw_piece(ctx, d.pos2, 2, 'yellowgreen');
	draw_piece(ctx, d.posOpp1, 3, 'lightgray');
	draw_piece(ctx, d.posOpp2, 4, 'mintcream');
	produce_dices('throw', d.throwing);
	produce_dices('cached', d.cache);
	show_dices();
	document.getElementById('round').innerText = d.step;
	document.getElementById('cacheable').innerText = d.cacheable;
}

function send(opts) {
  if (opts === undefined) opts = {};
  fetch('step', {
    method: 'post',
    body: JSON.stringify(opts)
  }).then(function(response) {
    return response.json();
  }).then(function(data) {	
    graph(data);
    initialized = true;
  });
}

let initialized = false;

window.onload = function() {
	show_dices();
	let canvas = document.getElementById("board");
	let ctx = canvas.getContext("2d");
	let img = document.getElementById("snakedraw");
	ctx.drawImage(img, 0, 0);
	send();
}

window.onkeydown = function() {
	if (!initialized) return;
	
	let written = document.getElementById('send');
	let text = written.innerText;
	
	if (window.event.key === 'Delete') {
		initialized = false;
		written.innerText = '';
		let code = window.event.ctrlKey ? 'SHADOWTOUR' : 'EXTERMINATUS';
		send({'code':code});
		return;
	}
	
	if (text.length === 0) {		
		if (['1', '2', '`'].includes(window.event.key)) {
			written.innerText = window.event.key;
		}
	} else {
		initialized = false;
		written.innerText = '';
		send({'code':`${text}${window.event.key}`});
	}
}
