const canvas = document.getElementById("canvas");
const topdiv = document.getElementById("topdiv");
const context = canvas.getContext("2d");
var width_org = topdiv.offsetWidth;
var height_org = topdiv.offsetHeight;
canvas.width = width_org;
canvas.height = height_org;

var particleArray = [];
class Particle {
	constructor(x = 0, y = 0) {
		this.connections = [];
		this.speed = 0.2;
		this.radius = 10;
		this.x = Math.min(Math.max(this.radius, x), width_org - this.radius);
		this.y = Math.min(Math.max(this.radius, y), height_org - this.radius);
		this.dx = (Math.random() - 0.5) * this.speed;
		this.dy = (Math.random() - 0.5) * this.speed;
	}

	// Draw circle
	draw() {
		context.beginPath();
		context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
		const gradient = context.createRadialGradient(
			this.x,
			this.y,
			1,
			this.x + 0.5,
			this.y + 0.5,
			this.radius
		);
		gradient.addColorStop(0.0, "rgba(0, 153, 0, 1.0)");
		gradient.addColorStop(1.0, "rgba(204, 255, 204, 1.0)");
		context.fillStyle = gradient;
		context.fill();
	}

	// Draw line
	connect() {
		context.beginPath();
		context.strokeStyle = "rgba(204, 255, 204, 1.0)";
		context.lineWidth = 2;

		const number_of_connections = 2;
		
		this.connections = [];
		for (let i = 0; i < particleArray.length; i++) {
			var p = particleArray[i];
			if (p != this) {
				const distance = euclidian(this, p);
				if (this.connections.length < number_of_connections) {
					this.connections.push([distance, p]);
					this.connections.sort(compareDistances);
				} else {
					if (distance < this.connections[this.connections.length-1][0]) {
						this.connections[this.connections.length-1] = [distance, p];
						this.connections.sort(compareDistances);
					}
				}
			}
		}

		// Draw
		for (let i = 0; i < this.connections.length; i++) {
			var s = this.connections[i];

			// Draw line from the edge of the circle
			const dx = this.x - s[1].x;
			const dy = this.y - s[1].y;
			const length = Math.sqrt(dx**2 + dy**2);
			const factor = this.radius / length;
			var x2 = s[1].x + factor*dx;
			var y2 = s[1].y + factor*dy;

			// Line
			context.moveTo(this.x, this.y);
			context.lineTo(x2, y2);
			context.stroke();
		}

	}

	// Move circle
	move() {
		if (topdiv.offsetWidth != width_org || topdiv.offsetHeight != height_org) {
			console.log(width_org, topdiv.offsetWidth);
			console.log(height_org, topdiv.offsetHeight);
			width_org = topdiv.offsetWidth;
			height_org = topdiv.offsetHeight;
			createParticles();
		}
		if (this.x + this.dx < this.radius || this.x + this.dx > width_org - this.radius) {
			this.dx *= -1;
		}
		if (this.y + this.dy < this.radius || this.y + this.dy > height_org - this.radius) {
			this.dy *= -1;
		}
		this.y += this.dy;
		this.x += this.dx;
	}
}

function compareDistances(a, b) {
	return a[0] > b[0];
}

const euclidian = (a, b) => {
	return (a.x - b.x) ** 2 + (a.y - b.y) ** 2;
}

const createParticles = () => {
	// Initialize the random generator with a seed
	function createRandomGenerator(seed) {
		let state = seed;
		
		return function() {
			state = (state * 9301 + 49297) % 233280;
			return state / 233280;
		};
	}	
	const seed = 12345;
	const getRandom = createRandomGenerator(seed);

	particleArray = [];
	const number_of_particles = Math.floor(0.0002 * width_org * height_org);
	for (let i = 0; i < number_of_particles; i++) {
		x = Math.floor(getRandom() * width_org)
		y = Math.floor(getRandom() * height_org)
		const particle = new Particle(x, y);
		particleArray.push(particle);
	}
}

const animate = () => {
	context.clearRect(0, 0, width_org, height_org);
	particleArray.forEach((particle) => {
		particle.move();
		particle.connect();
		particle.draw();
	});
	requestAnimationFrame(animate);
};

createParticles();
animate();
