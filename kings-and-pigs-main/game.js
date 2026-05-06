const canvas = document.getElementById('gameCanvas');
canvas.width = 1500;
canvas.height = 500;
const ctx = canvas.getContext('2d');

// Game state
const gameState = {
  unlockedActions: new Set(),
  currentChallenge: 0,
  challenges: [
    {
      title: "Print Challenge",
      description: "Type the C code to print 'Hello World'",
      solution: "printf(\"Hello World\");",
      actionId: "action1"
    },
    {
      title: "Variable Challenge",
      description: "Type the C code to declare an integer variable named 'x'",
      solution: "int x;",
      actionId: "action2"
    },
    {
      title: "Loop Challenge",
      description: "Type the C code for a for loop that counts from 1 to 5",
      solution: "for(int i=1; i<=5; i++)",
      actionId: "action3"
    },
    {
      title: "If Challenge",
      description: "Type the C code for an if statement checking if x is greater than 10",
      solution: "if(x > 10)",
      actionId: "action4"
    },
    {
      title: "Function Challenge",
      description: "Type the C code to declare a function named 'add' that takes two integers",
      solution: "int add(int a, int b)",
      actionId: "action5"
    },
    {
      title: "Array Challenge",
      description: "Type the C code to declare an array of 5 integers",
      solution: "int arr[5];",
      actionId: "action6"
    },
    {
      title: "Pointer Challenge",
      description: "Type the C code to declare a pointer to an integer",
      solution: "int *ptr;",
      actionId: "action7"
    },
    {
      title: "Struct Challenge",
      description: "Type the C code to declare a struct named 'Point' with x and y coordinates",
      solution: "struct Point { int x; int y; };",
      actionId: "action8"
    }
  ]
};

// Load all character images
const playerImage = new Image();
playerImage.src = './img/Character_1.png';

// Load frame 1 images (5 images)
const frame1Images = [];
for(let i = 1; i <= 5; i++) {
  const img = new Image();
  img.src = `./img/frame_1_${i}.png`;
  frame1Images.push(img);
}

// Load frame 2 images (5 images)
const frame2Images = [];
for(let i = 1; i <= 5; i++) {
  const img = new Image();
  img.src = `./img/frame_2_${i}.png`;
  frame2Images.push(img);
}

const computerImage = new Image();
computerImage.src = './img/Character_2.png';

// Create iframe for 3D background
const iframe = document.createElement('iframe');
iframe.src = 'https://www.3dviewer.net/embed.html?model=https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/DamagedHelmet/glTF/DamagedHelmet.gltf';
iframe.style.position = 'absolute';
iframe.style.top = '0';
iframe.style.left = '0';
iframe.style.width = '100%';
iframe.style.height = '100%';
iframe.style.zIndex = '-1';
iframe.style.border = 'none';
document.querySelector('.game-container').prepend(iframe);

const player = {
  x: 50,
  y: canvas.height - 167,
  width: 56,
  height: 71,
  health: 100,
  isAnimating: false,
  currentFrame: 0,
  currentSequence: 0,
  animationFrames: [frame1Images, frame2Images],
  lastFrameTime: 0,
  velocityY: 0,
  isJumping: false,
  isShielding: false,
  shieldDuration: 0
};

const computer = {
  x: canvas.width - 167,
  y: canvas.height - 175,
  width: 70,
  height: 85,
  health: 100,
  isAnimating: false,
  currentFrame: 0,
  currentSequence: 0,
  animationFrames: 0,
  lastFrameTime: 0
};

const bullets = [];
const computerBullets = [];
let hitEffects = [];

// Initialize the game
function initGame() {
  console.log('Initializing game...');
  updateTaskDescription();
  setupActionBoxes();
  console.log('Game initialized');
}

// Update task description
function updateTaskDescription() {
  const taskDescription = document.getElementById('taskDescription');
  if (gameState.currentChallenge < gameState.challenges.length) {
    const challenge = gameState.challenges[gameState.currentChallenge];
    taskDescription.textContent = `${challenge.title}\n\n${challenge.description}`;
  } else {
    taskDescription.textContent = "All challenges completed!";
  }
}

// Setup action boxes
function setupActionBoxes() {
  console.log('Setting up action boxes...');
  console.log('Current challenges:', gameState.challenges);
  
  gameState.challenges.forEach((challenge, index) => {
    console.log(`Setting up challenge ${index}:`, challenge);
    const actionBox = document.getElementById(challenge.actionId);
    console.log('Action box found:', actionBox);
    
    if (!actionBox) {
      console.error(`Action box with id ${challenge.actionId} not found!`);
      return;
    }
    
    const input = actionBox.querySelector('.code-input');
    const submitButton = actionBox.querySelector('.submit-button');
    const status = actionBox.querySelector('.action-status');
    
    console.log('Input element:', input);
    console.log('Submit button:', submitButton);
    
    // Enable input and button when it's the current challenge
    if (index === gameState.currentChallenge) {
      console.log(`Enabling challenge ${index} (${challenge.actionId})`);
      input.disabled = false;
      input.placeholder = `Type '${challenge.solution}' to unlock`;
      submitButton.disabled = false;
    }
    
    submitButton.addEventListener('click', () => {
      console.log('Submit button clicked!');
      const code = input.value.trim().toLowerCase();
      console.log('Submitted code:', code);
      console.log('Expected solution:', challenge.solution.toLowerCase());
      
      if (code === challenge.solution.toLowerCase()) {
        console.log('Correct code entered! Unlocking action...');
        unlockAction(challenge.actionId);
        gameState.unlockedActions.add(challenge.actionId);
        gameState.currentChallenge++;
        updateTaskDescription();
        
        // Enable the next challenge
        if (gameState.currentChallenge < gameState.challenges.length) {
          const nextActionBox = document.getElementById(gameState.challenges[gameState.currentChallenge].actionId);
          const nextInput = nextActionBox.querySelector('.code-input');
          const nextSubmitButton = nextActionBox.querySelector('.submit-button');
          nextInput.disabled = false;
          nextInput.placeholder = `Type '${gameState.challenges[gameState.currentChallenge].solution}' to unlock`;
          nextSubmitButton.disabled = false;
        }
      } else {
        console.log('Incorrect code entered. Try again.');
      }
    });
  });
}

// Unlock an action
function unlockAction(actionId) {
  console.log(`Unlocking action: ${actionId}`);
  const actionBox = document.getElementById(actionId);
  if (!actionBox) {
    console.error(`Action box with id ${actionId} not found!`);
    return;
  }
  
  actionBox.classList.remove('locked');
  actionBox.classList.add('unlocked');
  const status = actionBox.querySelector('.action-status');
  status.textContent = 'Unlocked';
  status.classList.remove('locked-status');
  status.classList.add('unlocked-status');
  const input = actionBox.querySelector('.code-input');
  const submitButton = actionBox.querySelector('.submit-button');
  input.disabled = true;
  submitButton.disabled = true;
  input.value = '';
  console.log(`Action ${actionId} unlocked successfully`);
}

// Handle player actions
function handlePlayerAction(actionId) {
  if (!gameState.unlockedActions.has(actionId)) return;

  switch(actionId) {
    case 'action1':
      shootBullet();
      break;
    case 'action2':
      moveLeft();
      break;
    case 'action3':
      moveRight();
      break;
    case 'action4':
      jump();
      break;
    case 'action5':
      activateShield();
      break;
    case 'action6':
      specialAttack();
      break;
    case 'action7':
      heal();
      break;
    case 'action8':
      ultimate();
      break;
  }
}

// Bullet creation and drawing
function shootBullet() {
  console.log('Shooting bullet...');
  bullets.push({
    x: player.x + player.width,
    y: player.y + player.height / 2,
    width: 10,
    height: 5,
    speed: 10
  });
}

// Update bullets
function updateBullets() {
  for (let i = bullets.length - 1; i >= 0; i--) {
    bullets[i].x += bullets[i].speed;
    
    // Remove bullets that go off screen
    if (bullets[i].x > canvas.width) {
      bullets.splice(i, 1);
    }
    
    // Check collision with computer
    if (checkCollision(bullets[i], computer)) {
      computer.health -= 10;
      updateHealthBars();
      bullets.splice(i, 1);
      createHitEffect(bullets[i].x, bullets[i].y);
    }
  }
}

// Draw bullets
function drawBullets() {
  ctx.fillStyle = 'yellow';
  bullets.forEach(bullet => {
    ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
  });
}

// Action implementations
function moveLeft() {
  if (player.x > 0) {
    player.x -= 10;
  }
}

function moveRight() {
  if (player.x < canvas.width - player.width) {
    player.x += 10;
  }
}

function jump() {
  if (!player.isJumping) {
    player.isJumping = true;
    player.velocityY = -15;
  }
}

function activateShield() {
  if (!player.isShielding) {
    player.isShielding = true;
    player.shieldDuration = 3000; // 3 seconds
  }
}

function specialAttack() {
  // Create multiple bullets in a spread pattern
  for (let i = -2; i <= 2; i++) {
    bullets.push({
      x: player.x + player.width,
      y: player.y + player.height/2 + (i * 10),
      vx: 15
    });
  }
}

function heal() {
  player.health = Math.min(100, player.health + 20);
  updateHealthBars();
}

function ultimate() {
  // Create a powerful attack that damages the enemy significantly
  computer.health = Math.max(0, computer.health - 50);
  updateHealthBars();
}

// Update health bars
function updateHealthBars() {
  gsap.to('#playerHealth', {
    width: player.health + '%'
  });
  gsap.to('#enemyHealth', {
    width: computer.health + '%'
  });
}

// Bullet drawing and effects
function drawBullet(bullet) {
  ctx.save();
  
  // Bullet trail
  const trailLength = 5;
  for(let i = 0; i < trailLength; i++) {
    const trailPos = {
      x: bullet.x - (bullet.vx * i * 2),
      y: bullet.y
    };
    
    ctx.beginPath();
    ctx.fillStyle = `rgba(100, 100, 100, ${(trailLength - i) / trailLength * 0.3})`;
    ctx.arc(trailPos.x, trailPos.y, 2, 0, Math.PI * 2);
    ctx.fill();
  }

  // Main bullet
  ctx.beginPath();
  ctx.fillStyle = '#FFD700';
  const bulletLength = 12;
  const bulletWidth = 3;
  const angle = bullet.vx > 0 ? 0 : Math.PI;

  ctx.translate(bullet.x, bullet.y);
  ctx.rotate(angle);
  
  ctx.beginPath();
  ctx.moveTo(-bulletLength/2, 0);
  ctx.lineTo(bulletLength/2, 0);
  ctx.lineTo(bulletLength/2 - 2, -bulletWidth);
  ctx.lineTo(-bulletLength/2, -bulletWidth);
  ctx.lineTo(-bulletLength/2, 0);
  ctx.fill();

  // Muzzle flash
  if (bullet.vx > 0 && bullet.x < player.x + player.width + 50 ||
      bullet.vx < 0 && bullet.x > computer.x - 50) {
    ctx.beginPath();
    const flashSize = Math.random() * 5 + 10;
    ctx.fillStyle = 'rgba(255, 200, 0, 0.6)';
    ctx.arc(bullet.vx > 0 ? -bulletLength : bulletLength, 0, flashSize, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();
}

// Hit effects
function createHitEffect(x, y) {
  const particles = [];
  for(let i = 0; i < 8; i++) {
    const angle = (Math.PI * 2 / 8) * i;
    particles.push({
      x: x,
      y: y,
      vx: Math.cos(angle) * 2,
      vy: Math.sin(angle) * 2,
      life: 1
    });
  }
  return particles;
}

// Collision detection
function checkCollision(bullet, target) {
  return bullet.x >= target.x && 
         bullet.x <= target.x + target.width &&
         bullet.y >= target.y && 
         bullet.y <= target.y + target.height;
}

// Enemy shooting
function enemyShoot() {
  computer.isAnimating = true;
  computerBullets.push({
    x: computer.x,
    y: computer.y + computer.height/2,
    vx: -15
  });
  
  canvas.style.transform = 'translateX(-2px)';
  setTimeout(() => {
    canvas.style.transform = 'none';
  }, 50);

  setTimeout(() => {
    computer.isAnimating = false;
  }, 200);
}

function drawBlock(block) {
  const currentTime = Date.now();
  
  if (block.isAnimating && block.animationFrames) {  // Check if animation frames exist
    // Calculate which image to show based on time
    if (currentTime - block.lastFrameTime > 333) { // 333ms for 3 FPS
      block.currentFrame = (block.currentFrame + 1) % 5;
      block.lastFrameTime = currentTime;
    }
    
    // Draw current animation frame if available, otherwise fall back to default image
    try {
      const frameImage = block.animationFrames[block.currentSequence][block.currentFrame];
      if (frameImage && frameImage.complete) {
        ctx.drawImage(frameImage, block.x, block.y, block.width, block.height);
      } else {
        const image = block === player ? playerImage : computerImage;
        ctx.drawImage(image, block.x, block.y, block.width, block.height);
      }
    } catch (error) {
      // Fallback to default image if there's any error
      const image = block === player ? playerImage : computerImage;
      ctx.drawImage(image, block.x, block.y, block.width, block.height);
    }
  } else {
    // Draw default standing image
    const image = block === player ? playerImage : computerImage;
    ctx.drawImage(image, block.x, block.y, block.width, block.height);
  }

  // Draw health bar
  const healthPercent = block.health / 100;
  const healthBarWidth = block.width;
  const healthBarHeight = 10;
  const healthBarY = block.y - 20;
  
  // Background of health bar (empty part)
  ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';
  ctx.fillRect(block.x, healthBarY, healthBarWidth, healthBarHeight);
  
  // Filled part of health bar
  ctx.fillStyle = `rgb(${255 * (1 - healthPercent)}, ${255 * healthPercent}, 0)`;
  ctx.fillRect(block.x, healthBarY, healthBarWidth * healthPercent, healthBarHeight);
  
  // Border of health bar
  ctx.strokeStyle = '#fff';
  ctx.strokeRect(block.x, healthBarY, healthBarWidth, healthBarHeight);
}

// Game loop
function gameLoop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Draw characters
  drawBlock(player);
  drawBlock(computer);
  
  // Update and draw bullets
  updateBullets();
  drawBullets();
  
  // Update hit effects
  updateHitEffects();
  
  // Check game over
  if (player.health <= 0 || computer.health <= 0) {
    gameOver();
  }

  requestAnimationFrame(gameLoop);
}

// Handle keyboard events
document.addEventListener('keydown', (event) => {
  if (!gameState.unlockedActions.has('action1')) return; // Only handle if shoot is unlocked
  
  switch(event.key) {
    case ' ': // Space bar
      if (gameState.unlockedActions.has('action1')) {
        console.log('Space pressed, shooting...');
        shootBullet();
      }
      break;
    case 'ArrowLeft':
      if (gameState.unlockedActions.has('action2')) {
        moveLeft();
      }
      break;
    case 'ArrowRight':
      if (gameState.unlockedActions.has('action3')) {
        moveRight();
      }
      break;
    case 'ArrowUp':
      if (gameState.unlockedActions.has('action4')) {
        jump();
      }
      break;
    case 's':
      if (gameState.unlockedActions.has('action5')) {
        activateShield();
      }
      break;
    case 'a':
      if (gameState.unlockedActions.has('action6')) {
        specialAttack();
      }
      break;
    case 'h':
      if (gameState.unlockedActions.has('action7')) {
        heal();
      }
      break;
    case 'u':
      if (gameState.unlockedActions.has('action8')) {
        ultimate();
      }
      break;
  }
});

// Start the game
initGame();
gameLoop(); 