import React, { useEffect, useRef, useState } from 'react';
import { Character, Bullet, Position, Explosion } from './types';

const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 400;
const PLAYER_SIZE = 30;
const ENEMY_SIZE = 30;
const PLAYER_MAX_HEALTH = 20;
const ENEMY_MAX_HEALTH = 5;
const BULLET_SIZE = 5;
const BULLET_SPEED = 7;
const ENEMY_SHOOT_INTERVAL = 10000; // Changed to 10 seconds
const EXPLOSION_DURATION = 300;
const EXPLOSION_SIZE = 20;

const drawBattlefieldBackground = (ctx: CanvasRenderingContext2D) => {
  const skyGradient = ctx.createLinearGradient(0, 0, 0, CANVAS_HEIGHT);
  skyGradient.addColorStop(0, '#0f172a');
  skyGradient.addColorStop(0.55, '#1e293b');
  skyGradient.addColorStop(1, '#3f2f1d');
  ctx.fillStyle = skyGradient;
  ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
  for (let index = 0; index < 18; index += 1) {
    const x = 40 + index * 42;
    const y = 45 + (index % 4) * 14;
    ctx.beginPath();
    ctx.arc(x, y, index % 3 === 0 ? 2.5 : 1.5, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.fillStyle = 'rgba(15, 23, 42, 0.65)';
  ctx.beginPath();
  ctx.moveTo(0, 230);
  ctx.lineTo(110, 150);
  ctx.lineTo(230, 235);
  ctx.lineTo(350, 140);
  ctx.lineTo(500, 240);
  ctx.lineTo(670, 155);
  ctx.lineTo(800, 230);
  ctx.lineTo(800, CANVAS_HEIGHT);
  ctx.lineTo(0, CANVAS_HEIGHT);
  ctx.closePath();
  ctx.fill();

  const groundGradient = ctx.createLinearGradient(0, 250, 0, CANVAS_HEIGHT);
  groundGradient.addColorStop(0, '#3f6212');
  groundGradient.addColorStop(1, '#1a2e05');
  ctx.fillStyle = groundGradient;
  ctx.fillRect(0, 250, CANVAS_WIDTH, CANVAS_HEIGHT - 250);

  ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
  for (let x = 0; x <= CANVAS_WIDTH; x += 40) {
    ctx.fillRect(x, 250, 1, CANVAS_HEIGHT - 250);
  }
  for (let y = 250; y <= CANVAS_HEIGHT; y += 30) {
    ctx.fillRect(0, y, CANVAS_WIDTH, 1);
  }

  ctx.fillStyle = 'rgba(18, 18, 18, 0.4)';
  ctx.fillRect(75, 205, 40, 45);
  ctx.fillRect(690, 195, 40, 55);
  ctx.fillRect(88, 185, 14, 20);
  ctx.fillRect(703, 170, 14, 25);

  ctx.fillStyle = 'rgba(245, 158, 11, 0.18)';
  ctx.beginPath();
  ctx.arc(115, 80, 60, 0, Math.PI * 2);
  ctx.fill();
};

const Game: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [gameOver, setGameOver] = useState<string | null>(null);
  const [explosions, setExplosions] = useState<Explosion[]>([]);
  
  const [player, setPlayer] = useState<Character>({
    x: 50, // Fixed position
    y: CANVAS_HEIGHT / 2,
    width: PLAYER_SIZE,
    height: PLAYER_SIZE,
    color: '#4CAF50',
    health: PLAYER_MAX_HEALTH // Increased to 20
  });

  const [enemy, setEnemy] = useState<Character>({
    x: CANVAS_WIDTH - 80, // Fixed position
    y: CANVAS_HEIGHT / 2,
    width: ENEMY_SIZE,
    height: ENEMY_SIZE,
    color: '#F44336',
    health: ENEMY_MAX_HEALTH // Changed to 5
  });

  const [playerBullets, setPlayerBullets] = useState<Bullet[]>([]);
  const [enemyBullets, setEnemyBullets] = useState<Bullet[]>([]);

  const createExplosion = (x: number, y: number) => {
    const explosion: Explosion = {
      x: x - EXPLOSION_SIZE / 2,
      y: y - EXPLOSION_SIZE / 2,
      width: EXPLOSION_SIZE,
      height: EXPLOSION_SIZE,
      color: '#FFA500',
      duration: EXPLOSION_DURATION,
      timestamp: Date.now()
    };
    setExplosions(prev => [...prev, explosion]);
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'x' && !gameOver) {
      setPlayerBullets(prev => [...prev, {
        x: player.x + player.width,
        y: player.y + (player.height / 2) - (BULLET_SIZE / 2),
        width: BULLET_SIZE,
        height: BULLET_SIZE,
        color: '#FFD700',
        direction: 'right'
      }]);
    }
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [gameOver, player.x, player.y]);

  useEffect(() => {
    if (gameOver) return;

    const enemyShootInterval = setInterval(() => {
      setEnemyBullets(prev => [...prev, {
        x: enemy.x,
        y: enemy.y + (enemy.height / 2) - (BULLET_SIZE / 2),
        width: BULLET_SIZE,
        height: BULLET_SIZE,
        color: '#FF5722',
        direction: 'left'
      }]);
    }, ENEMY_SHOOT_INTERVAL);

    return () => clearInterval(enemyShootInterval);
  }, [enemy.x, enemy.y, gameOver]);

  useEffect(() => {
    if (!canvasRef.current || gameOver) return;

    let animationFrameId: number;

    const gameLoop = () => {
      if (gameOver) return;

      // Clean up expired explosions
      setExplosions(prev => 
        prev.filter(explosion => 
          Date.now() - explosion.timestamp < explosion.duration
        )
      );

      // Check bullet collisions with each other
      let bulletsToRemove = new Set<Bullet>();
      
      playerBullets.forEach(playerBullet => {
        enemyBullets.forEach(enemyBullet => {
          if (
            playerBullet.x < enemyBullet.x + enemyBullet.width &&
            playerBullet.x + playerBullet.width > enemyBullet.x &&
            playerBullet.y < enemyBullet.y + enemyBullet.height &&
            playerBullet.y + playerBullet.height > enemyBullet.y
          ) {
            bulletsToRemove.add(playerBullet);
            bulletsToRemove.add(enemyBullet);
            createExplosion(
              (playerBullet.x + enemyBullet.x) / 2,
              (playerBullet.y + enemyBullet.y) / 2
            );
          }
        });
      });

      // Remove collided bullets
      setPlayerBullets(prev => 
        prev
          .filter(bullet => !bulletsToRemove.has(bullet))
          .map(bullet => ({ ...bullet, x: bullet.x + BULLET_SPEED }))
          .filter(bullet => bullet.x < CANVAS_WIDTH)
      );

      setEnemyBullets(prev =>
        prev
          .filter(bullet => !bulletsToRemove.has(bullet))
          .map(bullet => ({ ...bullet, x: bullet.x - BULLET_SPEED }))
          .filter(bullet => bullet.x > 0)
      );

      // Check collisions with enemy
      setPlayerBullets(prev => {
        const remainingBullets = prev.filter(bullet => {
          const collision = 
            bullet.x < enemy.x + enemy.width &&
            bullet.x + bullet.width > enemy.x &&
            bullet.y < enemy.y + enemy.height &&
            bullet.y + bullet.height > enemy.y;
          
          if (collision) {
            setEnemy(prevEnemy => ({
              ...prevEnemy,
              health: prevEnemy.health - 1
            }));
            createExplosion(bullet.x, bullet.y);
            return false;
          }
          return true;
        });
        return remainingBullets;
      });

      // Check collisions with player
      setEnemyBullets(prev => {
        const remainingBullets = prev.filter(bullet => {
          const collision = 
            bullet.x < player.x + player.width &&
            bullet.x + bullet.width > player.x &&
            bullet.y < player.y + player.height &&
            bullet.y + bullet.height > player.y;
          
          if (collision) {
            setPlayer(prevPlayer => ({
              ...prevPlayer,
              health: prevPlayer.health - 1
            }));
            createExplosion(bullet.x, bullet.y);
            return false;
          }
          return true;
        });
        return remainingBullets;
      });

      // Check game over conditions
      if (player.health <= 0) setGameOver('Game Over');
      if (enemy.health <= 0) setGameOver('You Win!');

      animationFrameId = requestAnimationFrame(gameLoop);
    };

    animationFrameId = requestAnimationFrame(gameLoop);
    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [gameOver, player.x, player.y, player.width, player.height, enemy.x, enemy.y, enemy.width, enemy.height]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Paint the arena before drawing characters and effects.
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    drawBattlefieldBackground(ctx);

    // Draw player
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);

    // Draw enemy
    ctx.fillStyle = enemy.color;
    ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);

    // Draw player bullets
    playerBullets.forEach(bullet => {
      ctx.fillStyle = bullet.color;
      ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });

    // Draw enemy bullets
    enemyBullets.forEach(bullet => {
      ctx.fillStyle = bullet.color;
      ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });

    // Draw explosions
    explosions.forEach(explosion => {
      const progress = 1 - (Date.now() - explosion.timestamp) / explosion.duration;
      ctx.fillStyle = explosion.color;
      ctx.globalAlpha = progress;
      ctx.beginPath();
      ctx.arc(
        explosion.x + explosion.width / 2,
        explosion.y + explosion.height / 2,
        explosion.width / 2,
        0,
        Math.PI * 2
      );
      ctx.fill();
      ctx.globalAlpha = 1;
    });

  }, [player, enemy, playerBullets, enemyBullets, explosions]);

  const playerHealthPercent = Math.max(0, (player.health / PLAYER_MAX_HEALTH) * 100);
  const enemyHealthPercent = Math.max(0, (enemy.health / ENEMY_MAX_HEALTH) * 100);

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-8 text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,_rgba(34,197,94,0.14),_transparent_28%),radial-gradient(circle_at_80%_10%,_rgba(249,115,22,0.12),_transparent_24%)]" />

      <div className="relative w-full max-w-5xl rounded-[28px] border border-white/10 bg-slate-950/65 p-5 shadow-[0_30px_80px_rgba(0,0,0,0.45)] backdrop-blur-sm sm:p-6">
        <div className="mb-5 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-amber-300/80">Battle Arena</p>
            <h1 className="mt-2 text-3xl font-black text-white sm:text-4xl">Kings vs Pigs</h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-300">
              A darker battlefield backdrop gives this shooter a stronger arcade look while keeping the action easy to see.
            </p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
            <p className="font-semibold text-white">Controls</p>
            <p className="mt-1">Press <span className="rounded-md bg-white/10 px-2 py-1 font-bold text-amber-300">X</span> to shoot</p>
          </div>
        </div>

        <div className="mb-4 grid gap-3 md:grid-cols-2">
          <div className="rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-4">
            <div className="mb-2 flex items-center justify-between text-sm">
              <span className="font-semibold text-emerald-200">Player Health</span>
              <span className="font-bold text-white">{player.health}/{PLAYER_MAX_HEALTH}</span>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-white/10">
              <div
                className="h-full rounded-full bg-gradient-to-r from-emerald-300 via-emerald-400 to-lime-400 transition-all duration-300"
                style={{ width: `${playerHealthPercent}%` }}
              />
            </div>
          </div>

          <div className="rounded-2xl border border-rose-400/20 bg-rose-500/10 p-4">
            <div className="mb-2 flex items-center justify-between text-sm">
              <span className="font-semibold text-rose-200">Enemy Health</span>
              <span className="font-bold text-white">{enemy.health}/{ENEMY_MAX_HEALTH}</span>
            </div>
            <div className="h-3 overflow-hidden rounded-full bg-white/10">
              <div
                className="h-full rounded-full bg-gradient-to-r from-orange-300 via-rose-400 to-red-500 transition-all duration-300"
                style={{ width: `${enemyHealthPercent}%` }}
              />
            </div>
          </div>
        </div>

        <div className="relative overflow-hidden rounded-[24px] border border-white/10 bg-black/20 p-3 shadow-inner shadow-black/40">
          <canvas
            ref={canvasRef}
            width={CANVAS_WIDTH}
            height={CANVAS_HEIGHT}
            className="w-full rounded-[18px] border border-white/10 bg-slate-900"
          />
          {gameOver && (
            <div className="absolute inset-3 flex items-center justify-center rounded-[18px] bg-slate-950/70 backdrop-blur-sm">
              <div className="rounded-2xl border border-white/10 bg-black/30 px-8 py-6 text-center">
                <p className="text-sm uppercase tracking-[0.35em] text-amber-300/80">Match Result</p>
                <div className="mt-3 text-4xl font-black text-white">{gameOver}</div>
              </div>
            </div>
          )}
        </div>

        <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-sm text-slate-300">
          <p>The new background uses a dusk battlefield theme so the green player, red enemy, and bullets stay highly visible.</p>
          <p className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-slate-200">Arcade HUD interface applied</p>
        </div>
      </div>
    </div>
  );
};

export default Game;