(() => {
  'use strict';

  const root = document.querySelector('[data-motion-root]');
  if (!root) return;

  const stage = root.querySelector('[data-athlete-stage]');
  const canvas = root.querySelector('[data-trajectory-canvas]');
  const context = canvas && canvas.getContext ? canvas.getContext('2d') : null;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const compactMotion = window.matchMedia('(max-width: 700px)');
  const precisePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

  const sessionKey = 'editorialLandingIntroPlayed';
  const controller = new AbortController();
  const signal = controller.signal;
  const timeouts = [];
  let pageVisible = !document.hidden;
  let resizeTimer = 0;
  let easterEggActive = false;

  function safeSessionGet() {
    try { return sessionStorage.getItem(sessionKey); } catch (error) { return null; }
  }
  function safeSessionSet() {
    try { sessionStorage.setItem(sessionKey, '1'); } catch (error) { /* storage optional */ }
  }
  function clearTimeline() {
    while (timeouts.length) window.clearTimeout(timeouts.pop());
  }

  /* ---------------------------------------------------------------- */
  /* Intro motion: progressive reveal driven by classes on <body>      */
  /* ---------------------------------------------------------------- */
  function initIntroMotion() {
    const body = document.body;

    function addScene(n) { body.classList.add(`is-intro-scene-${n}`); }

    function settle(state) {
      clearTimeline();
      for (let i = 1; i <= 7; i += 1) addScene(i);
      body.classList.remove('is-intro-scene-loading');
      body.classList.add(`is-intro-${state}`);
      body.classList.remove('is-intro-intro');
      safeSessionSet();
      window.dispatchEvent(new CustomEvent('editorial:settled'));
    }

    function playIntro() {
      clearTimeline();
      for (let i = 1; i <= 7; i += 1) body.classList.remove(`is-intro-scene-${i}`);
      body.classList.remove('is-intro-settled', 'is-intro-skipped', 'is-intro-reduced');
      body.classList.add('is-intro-intro');

      const timing = compactMotion.matches
        ? [[1, 0], [2, 250], [3, 700], [4, 1050], [5, 1450], [6, 1850], [7, 2200]]
        : [[1, 0], [2, 450], [3, 1050], [4, 1550], [5, 2150], [6, 2750], [7, 3300]];

      timing.forEach(([scene, delay]) => {
        timeouts.push(window.setTimeout(() => addScene(scene), delay));
      });
      timeouts.push(window.setTimeout(() => settle('settled'), compactMotion.matches ? 2700 : 4000));
    }

    root.querySelector('[data-intro-skip]')?.addEventListener('click', () => settle('skipped'), { signal });

    document.addEventListener('visibilitychange', () => { pageVisible = !document.hidden; }, { signal });
    window.addEventListener('pageshow', (event) => {
      pageVisible = !document.hidden;
      if (event.persisted) {
        settle('settled');
        root.querySelectorAll('.figure-ghost').forEach((ghost) => ghost.remove());
        window.dispatchEvent(new CustomEvent('editorial:canvasReady'));
      }
    }, { signal });

    if (reduceMotion.matches) {
      body.classList.add('is-intro-reduced');
    } else if (safeSessionGet()) {
      settle('settled');
    } else {
      playIntro();
    }
  }

  /* ---------------------------------------------------------------- */
  /* Athlete auto-rotation: 이전 동작이 잔상처럼 흐려지며 사라진다         */
  /* ---------------------------------------------------------------- */
  function initAthleteSwitcher() {
    if (!stage) return;
    const images = Array.from(stage.querySelectorAll('[data-athlete-image]'));
    if (images.length < 2) return;
    const wrap = stage.querySelector('.athlete-figure-wrap');

    let index = Math.max(0, images.findIndex((img) => img.classList.contains('is-active')));
    let swimmingLayerTimer = 0;

    function spawnGhost(sourceImage) {
      if (!wrap) return;
      const ghost = sourceImage.cloneNode(true);
      ghost.removeAttribute('data-athlete-image');
      ghost.className = 'figure-ghost';
      ghost.style.objectPosition = window.getComputedStyle(sourceImage).objectPosition;
      ghost.setAttribute('aria-hidden', 'true');
      wrap.appendChild(ghost);
      // 클래스를 바로 붙이면 브라우저가 시작 상태를 못 보고 전환을 건너뛸 수 있어
      // 한 프레임 쉬었다가 붙인다.
      requestAnimationFrame(() => {
        requestAnimationFrame(() => ghost.classList.add('is-fading'));
      });
      timeouts.push(window.setTimeout(() => ghost.remove(), 800));
    }

    function activate(nextIndex) {
      if (easterEggActive) return;
      const targetImage = images[nextIndex];
      if (!targetImage) return;
      index = nextIndex;

      const current = images.find((img) => img.classList.contains('is-active'));
      window.clearTimeout(swimmingLayerTimer);
      if (wrap && targetImage.dataset.athleteImage === 'swimming') {
        wrap.classList.add('is-swimming-front');
      } else if (wrap && current?.dataset.athleteImage === 'swimming') {
        swimmingLayerTimer = window.setTimeout(() => {
          wrap.classList.remove('is-swimming-front');
        }, 800);
        timeouts.push(swimmingLayerTimer);
      } else if (wrap) {
        wrap.classList.remove('is-swimming-front');
      }
      if (current && current !== targetImage && !reduceMotion.matches) {
        spawnGhost(current);
      }
      images.forEach((img) => img.classList.toggle('is-active', img === targetImage));
    }

    if (reduceMotion.matches) return;

    const cycleMs = 4500;
    const autoTimer = window.setInterval(() => {
      if (!pageVisible) return;
      activate((index + 1) % images.length);
    }, cycleMs);

    signal.addEventListener('abort', () => {
      window.clearInterval(autoTimer);
      window.clearTimeout(swimmingLayerTimer);
    }, { once: true });
  }

  /* ---------------------------------------------------------------- */
  /* Hidden card sequence easter egg                                  */
  /* ---------------------------------------------------------------- */
  function initEasterEgg() {
    if (!stage) return;

    const sequence = (stage.dataset.easterSequence || '')
      .split(',')
      .map((value) => Number.parseInt(value.trim(), 10))
      .filter((value) => Number.isInteger(value));
    const cards = Array.from(stage.querySelectorAll('[data-easter-key]'));
    const resetBadge = stage.querySelector('[data-stage-badge]');
    const backgroundUrl = stage.dataset.easterBackgroundUrl;
    const characterUrl = stage.dataset.easterImageUrl;
    const symbolUrl = stage.dataset.easterSymbolUrl;
    const auraUrl = stage.dataset.easterAuraUrl;
    const audioUrl = stage.dataset.easterAudioUrl;
    const voiceUrl = stage.dataset.easterVoiceUrl;

    if (!sequence.length || !cards.length || !backgroundUrl || !characterUrl || !symbolUrl || !auraUrl || !audioUrl || !voiceUrl) return;

    let inputIndex = 0;
    const hiddenAudio = new Audio(audioUrl);
    const voiceAudio = new Audio(voiceUrl);
    const easterTimers = [];

    hiddenAudio.preload = 'auto';
    hiddenAudio.volume = 1;
    hiddenAudio.load();
    voiceAudio.preload = 'auto';
    voiceAudio.volume = 0;
    voiceAudio.loop = true;
    voiceAudio.load();

    voiceAudio.addEventListener('ended', () => {
      hiddenAudio.volume = 1;
    }, { signal });

    function makeElement(tagName, className) {
      const element = document.createElement(tagName);
      element.className = className;
      return element;
    }

    function buildCrumbleCanvas() {
      const crumbleCanvas = makeElement('canvas', 'easter-collapse-canvas');
      crumbleCanvas.setAttribute('aria-hidden', 'true');
      return crumbleCanvas;
    }

    function startCrumbleAnimation(crumbleCanvas) {
      if (!crumbleCanvas) return;
      if (reduceMotion.matches) {
        crumbleCanvas.remove();
        return;
      }

      const Matter = window.Matter;
      const PIXI = window.PIXI;
      if (!Matter || !PIXI) {
        console.warn('Easter egg physics libraries could not be loaded.');
        crumbleCanvas.remove();
        return;
      }

      const width = window.innerWidth;
      const height = window.innerHeight;
      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      const impact = { x: width * .5, y: height * .72 };
      const backgroundColor = getComputedStyle(document.documentElement)
        .getPropertyValue('--editorial-bg').trim() || '#f2efe7';
      const backgroundNumber = Number.parseInt(backgroundColor.replace('#', ''), 16) || 0xf2efe7;
      const engine = Matter.Engine.create();
      const app = new PIXI.Application({
        view: crumbleCanvas,
        width,
        height,
        resolution: dpr,
        autoDensity: true,
        antialias: true,
        backgroundAlpha: 0,
      });
      const shards = [];
      const dustParticles = [];
      const physicsLayer = new PIXI.Container();
      const dustLayer = new PIXI.Container();
      const solidCover = new PIXI.Graphics();

      app.stage.sortableChildren = true;
      solidCover.beginFill(backgroundNumber).drawRect(0, 0, width, height).endFill();
      solidCover.zIndex = 0;
      physicsLayer.zIndex = 1;
      dustLayer.zIndex = 2;
      app.stage.addChild(solidCover, physicsLayer, dustLayer);

      engine.gravity.x = 0;
      engine.gravity.y = 1.18;
      engine.gravity.scale = .001;

      function randomBetween(min, max) {
        return min + Math.random() * (max - min);
      }

      function clipPolygon(polygon, a, b, c) {
        const clipped = [];
        for (let index = 0; index < polygon.length; index += 1) {
          const current = polygon[index];
          const previous = polygon[(index + polygon.length - 1) % polygon.length];
          const currentValue = a * current.x + b * current.y - c;
          const previousValue = a * previous.x + b * previous.y - c;
          const currentInside = currentValue <= .01;
          const previousInside = previousValue <= .01;

          if (currentInside !== previousInside) {
            const ratio = previousValue / (previousValue - currentValue);
            clipped.push({
              x: previous.x + (current.x - previous.x) * ratio,
              y: previous.y + (current.y - previous.y) * ratio,
            });
          }
          if (currentInside) clipped.push(current);
        }
        return clipped;
      }

      function createWallCells() {
        const columns = compactMotion.matches ? 5 : 8;
        const rows = compactMotion.matches ? 6 : 7;
        const seeds = [];

        for (let row = 0; row < rows; row += 1) {
          for (let column = 0; column < columns; column += 1) {
            seeds.push({
              x: (column + .5 + randomBetween(-.28, .28)) * width / columns,
              y: (row + .5 + randomBetween(-.3, .3)) * height / rows,
            });
          }
        }

        return seeds.map((seed) => {
          let polygon = [
            { x: -2, y: -2 },
            { x: width + 2, y: -2 },
            { x: width + 2, y: height + 2 },
            { x: -2, y: height + 2 },
          ];

          seeds.forEach((other) => {
            if (other === seed || polygon.length < 3) return;
            const a = 2 * (other.x - seed.x);
            const b = 2 * (other.y - seed.y);
            const c = other.x * other.x + other.y * other.y - seed.x * seed.x - seed.y * seed.y;
            polygon = clipPolygon(polygon, a, b, c);
          });
          return polygon;
        }).filter((polygon) => polygon.length >= 3);
      }

      function createShard(vertices) {
        const centerX = vertices.reduce((sum, point) => sum + point.x, 0) / vertices.length;
        const centerY = vertices.reduce((sum, point) => sum + point.y, 0) / vertices.length;
        const body = Matter.Bodies.fromVertices(centerX, centerY, [vertices], {
          friction: .78,
          frictionAir: .008,
          restitution: .035,
          density: .0024,
          chamfer: { radius: 1.5 },
        }, true);
        if (!body) return;

        Matter.Body.setStatic(body, true);
        Matter.World.add(engine.world, body);

        const localPoints = [];
        body.vertices.forEach((point) => {
          localPoints.push(point.x - body.position.x, point.y - body.position.y);
        });

        const container = new PIXI.Container();
        const brokenEdge = new PIXI.Graphics();
        const face = new PIXI.Graphics();
        const crack = new PIXI.Graphics();

        brokenEdge.beginFill(0x514b43, .98).drawPolygon(localPoints).endFill();
        brokenEdge.position.set(4, 7);
        brokenEdge.alpha = 0;
        face.beginFill(backgroundNumber).drawPolygon(localPoints).endFill();
        crack.lineStyle(1.35, 0x302d29, .92).drawPolygon(localPoints);
        crack.alpha = 0;
        container.addChild(brokenEdge, face, crack);
        container.position.set(body.position.x, body.position.y);
        physicsLayer.addChild(container);

        const horizontalDistance = Math.abs(centerX - impact.x) / width;
        const releaseAt = 500
          + (1 - centerY / height) * 620
          + horizontalDistance * 150
          + randomBetween(-70, 85);
        shards.push({ body, container, brokenEdge, crack, released: false, releaseAt });
      }

      createWallCells().forEach(createShard);

      const dustSource = new PIXI.Graphics();
      dustSource.beginFill(0xd7d0c3).drawCircle(12, 12, 12).endFill();
      const dustTexture = app.renderer.generateTexture(dustSource);
      dustSource.destroy();

      const particleCount = compactMotion.matches ? 52 : 105;
      for (let index = 0; index < particleCount; index += 1) {
        const sprite = new PIXI.Sprite(dustTexture);
        const scale = randomBetween(.18, .78);
        sprite.anchor.set(.5);
        sprite.scale.set(scale);
        sprite.alpha = 0;
        dustLayer.addChild(sprite);
        dustParticles.push({
          sprite,
          x: randomBetween(width * .08, width * .92),
          y: randomBetween(height * .72, height * .99),
          velocityX: randomBetween(-95, 95),
          velocityY: randomBetween(-150, -28),
          start: randomBetween(650, 1450),
          life: randomBetween(1050, 1900),
          growth: randomBetween(.75, 1.8),
          baseScale: scale,
        });
      }

      let frameId = 0;
      let startedAt = 0;
      let previousTime = 0;
      let destroyed = false;

      function destroyPhysicsScene() {
        if (destroyed) return;
        destroyed = true;
        window.cancelAnimationFrame(frameId);
        Matter.World.clear(engine.world, false);
        Matter.Engine.clear(engine);
        app.destroy(false, { children: true, texture: true, baseTexture: true });
        crumbleCanvas.remove();
      }

      function updateDust(elapsed, deltaSeconds) {
        dustParticles.forEach((particle) => {
          const age = elapsed - particle.start;
          if (age < 0 || age > particle.life) {
            particle.sprite.alpha = 0;
            return;
          }
          const progress = age / particle.life;
          particle.velocityY += 45 * deltaSeconds;
          particle.x += particle.velocityX * deltaSeconds;
          particle.y += particle.velocityY * deltaSeconds;
          particle.sprite.position.set(particle.x, particle.y);
          particle.sprite.scale.set(particle.baseScale * (1 + progress * particle.growth));
          particle.sprite.alpha = Math.sin(progress * Math.PI) * .42;
        });
      }

      function animate(now) {
        if (!startedAt) {
          startedAt = now;
          previousTime = now;
        }
        const elapsed = now - startedAt;
        const deltaMilliseconds = Math.min(now - previousTime, 33.34);
        const deltaSeconds = deltaMilliseconds / 1000;
        previousTime = now;

        solidCover.alpha = Math.max(0, Math.min(1, 1 - (elapsed - 420) / 330));

        shards.forEach((shard) => {
          const crackStart = Math.max(80, shard.releaseAt - 410);
          shard.crack.alpha = Math.max(0, Math.min(.95, (elapsed - crackStart) / 260));

          if (!shard.released && elapsed >= shard.releaseAt) {
            shard.released = true;
            shard.brokenEdge.alpha = 1;
            Matter.Body.setStatic(shard.body, false);
            Matter.Body.setVelocity(shard.body, {
              x: (shard.body.position.x - impact.x) / width * randomBetween(1.1, 2.8),
              y: randomBetween(-1.7, -.25),
            });
            Matter.Body.setAngularVelocity(shard.body, randomBetween(-.035, .035));
          }

          shard.container.position.set(shard.body.position.x, shard.body.position.y);
          shard.container.rotation = shard.body.angle;
        });

        Matter.Engine.update(engine, deltaMilliseconds);
        updateDust(elapsed, deltaSeconds);

        if (elapsed > 520 && elapsed < 1550) {
          const strength = (1 - (elapsed - 520) / 1030) * (compactMotion.matches ? 2.5 : 4.5);
          app.stage.position.set(randomBetween(-strength, strength), randomBetween(-strength * .55, strength * .55));
        } else {
          app.stage.position.set(0, 0);
        }

        const allShardsBelowViewport = shards.every((shard) => (
          shard.released && shard.body.bounds.min.y > height + 40
        ));
        const collapseFinished = elapsed > 3000 && allShardsBelowViewport;

        if (!collapseFinished && elapsed < 6500) {
          frameId = window.requestAnimationFrame(animate);
        } else {
          destroyPhysicsScene();
        }
      }

      frameId = window.requestAnimationFrame(animate);
      signal.addEventListener('abort', () => {
        destroyPhysicsScene();
      }, { once: true });
    }

    function buildEasterScene() {
      const scene = makeElement('div', 'easter-scene');
      scene.setAttribute('aria-hidden', 'true');

      const background = makeElement('div', 'easter-scene-background');
      background.style.backgroundImage = `url("${backgroundUrl}")`;

      const formation = makeElement('div', 'easter-formation');
      const symbol = makeElement('img', 'easter-compass-symbol');
      symbol.dataset.src = symbolUrl;
      symbol.alt = '';
      symbol.draggable = false;

      const auraWrap = makeElement('div', 'easter-aura-wrap');
      const aura = makeElement('img', 'easter-aura');
      aura.src = auraUrl;
      aura.alt = '';
      aura.draggable = false;
      auraWrap.appendChild(aura);

      const character = makeElement('img', 'easter-character');
      character.src = characterUrl;
      character.alt = '';
      character.draggable = false;

      const title = makeElement('div', 'easter-technique-title');
      const titlePrefix = document.createElement('span');
      const titleName = document.createElement('strong');
      titlePrefix.textContent = '파괴살';
      titleName.textContent = '「나침」';
      title.append(titlePrefix, titleName);

      formation.append(symbol, auraWrap, character, title);
      scene.append(background, formation, buildCrumbleCanvas());
      return scene;
    }

    function schedule(callback, delay) {
      easterTimers.push(window.setTimeout(callback, delay));
    }

    function activateEasterEgg() {
      if (easterEggActive) return;

      easterEggActive = true;
      inputIndex = 0;
      const scene = buildEasterScene();

      document.body.appendChild(scene);

      requestAnimationFrame(() => {
        scene.classList.add('is-crumbling');
        startCrumbleAnimation(scene.querySelector('.easter-collapse-canvas'));
        document.body.classList.add('is-easter-playing');
      });

      hiddenAudio.currentTime = 0;
      hiddenAudio.muted = false;
      hiddenAudio.play().then(() => {
        scene.classList.add('is-music-playing');
      }).catch((error) => {
        console.warn('Easter egg audio playback was blocked.', error);
      });

      // Unlock the second audio element during the original card click so
      // browsers also allow the delayed voice line to play later.
      voiceAudio.currentTime = 0;
      voiceAudio.volume = 0;
      voiceAudio.loop = true;
      voiceAudio.play().catch((error) => {
        console.warn('Easter egg voice preload was blocked.', error);
      });

      schedule(() => document.body.classList.add('is-easter-character-landed'), 2200);
      schedule(() => scene.classList.add('is-character-dropping'), 2800);
      schedule(() => {
        const symbol = scene.querySelector('.easter-compass-symbol');
        if (symbol?.dataset.src) symbol.src = symbol.dataset.src;
        scene.classList.add('is-symbol-visible');
      }, 4100);
      schedule(() => scene.classList.add('is-aura-visible'), 4550);
      schedule(() => scene.classList.add('is-title-visible'), 7800);
      schedule(() => {
        hiddenAudio.volume = .28;
        voiceAudio.loop = false;
        voiceAudio.currentTime = 0;
        voiceAudio.volume = 1;
        voiceAudio.play().catch((error) => {
          hiddenAudio.volume = 1;
          console.warn('Easter egg voice playback was blocked.', error);
        });
      }, 8500);
      schedule(() => {
        scene.classList.add('is-settled');
        document.body.classList.remove('is-easter-playing');
        document.body.classList.add('is-easter-settled');
      }, 8600);
    }

    cards.forEach((card) => {
      card.addEventListener('click', () => {
        if (easterEggActive) return;

        const key = Number.parseInt(card.dataset.easterKey, 10);
        if (key === sequence[inputIndex]) {
          inputIndex += 1;
          if (inputIndex === sequence.length) activateEasterEgg();
          return;
        }

        inputIndex = key === sequence[0] ? 1 : 0;
      }, { signal });
    });

    resetBadge?.addEventListener('click', () => {
      inputIndex = 0;
    }, { signal });

    signal.addEventListener('abort', () => {
      easterTimers.forEach((timer) => window.clearTimeout(timer));
      if (hiddenAudio) hiddenAudio.pause();
      if (voiceAudio) voiceAudio.pause();
    }, { once: true });
  }

  /* ---------------------------------------------------------------- */
  /* Canvas trajectories: hand-drawn curves connecting cards & figure  */
  /* ---------------------------------------------------------------- */
  function initCanvasTrajectories() {
    if (!context || !canvas || !stage) return;
    if (compactMotion.matches) return;

    const linkGroups = [
      ['[data-stage-card="sport"]', '[data-stage-card="region"]'],
      ['[data-stage-card="region"]', '[data-stage-card="qual"]'],
      ['[data-stage-card="qual"]', '[data-stage-card="org"]'],
      ['[data-stage-badge]', '[data-stage-card="org"]'],
    ];

    let curves = [];
    let progress = 0;
    let frameId = 0;
    let drawn = false;

    function anchor(selector) {
      const el = stage.querySelector(selector);
      if (!el) return null;
      const stageBox = stage.getBoundingClientRect();
      const box = el.getBoundingClientRect();
      return {
        x: box.left - stageBox.left + box.width / 2,
        y: box.top - stageBox.top + box.height / 2,
      };
    }

    function buildCurves() {
      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      const box = stage.getBoundingClientRect();
      canvas.width = Math.round(box.width * dpr);
      canvas.height = Math.round(box.height * dpr);
      canvas.style.width = `${box.width}px`;
      canvas.style.height = `${box.height}px`;
      context.setTransform(dpr, 0, 0, dpr, 0, 0);

      curves = linkGroups.map(([fromSel, toSel]) => {
        const from = anchor(fromSel);
        const to = anchor(toSel);
        if (!from || !to) return null;
        const mx = (from.x + to.x) / 2 + (to.y - from.y) * .18;
        const my = (from.y + to.y) / 2 - (to.x - from.x) * .18;
        const points = [];
        const steps = 28;
        for (let i = 0; i <= steps; i += 1) {
          const t = i / steps;
          const x = (1 - t) ** 2 * from.x + 2 * (1 - t) * t * mx + t ** 2 * to.x;
          const y = (1 - t) ** 2 * from.y + 2 * (1 - t) * t * my + t ** 2 * to.y;
          points.push({ x, y });
        }
        return points;
      }).filter(Boolean);
    }

    function draw() {
      const box = stage.getBoundingClientRect();
      context.clearRect(0, 0, box.width, box.height);
      context.strokeStyle = 'rgba(17,17,17,.5)';
      context.lineWidth = 1.3;
      context.lineCap = 'round';

      curves.forEach((points) => {
        const count = Math.max(2, Math.round(points.length * progress));
        context.beginPath();
        points.slice(0, count).forEach((point, index) => {
          if (index === 0) context.moveTo(point.x, point.y);
          else context.lineTo(point.x, point.y);
        });
        context.stroke();

        if (progress >= 1) {
          const dot = points[points.length - 1];
          context.beginPath();
          context.fillStyle = '#2457f5';
          context.arc(dot.x, dot.y, 3, 0, Math.PI * 2);
          context.fill();
        }
      });
    }

    function animateIn() {
      if (drawn) return;
      drawn = true;
      const start = performance.now();
      const duration = reduceMotion.matches ? 1 : 900;

      function step(now) {
        progress = Math.min(1, (now - start) / duration);
        draw();
        if (progress < 1 && pageVisible) frameId = window.requestAnimationFrame(step);
      }
      frameId = window.requestAnimationFrame(step);
    }

    buildCurves();
    if (reduceMotion.matches) {
      progress = 1;
      draw();
    } else {
      window.addEventListener('editorial:canvasReady', animateIn, { signal, once: true });
    }

    window.addEventListener('resize', () => {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(() => { buildCurves(); draw(); }, 150);
    }, { passive: true, signal });

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) window.cancelAnimationFrame(frameId);
    }, { signal });

    signal.addEventListener('abort', () => window.cancelAnimationFrame(frameId), { once: true });

    // Fallback: if intro settles without ever dispatching canvasReady (e.g. repeat visit), draw immediately.
    if (safeSessionGet() || reduceMotion.matches) {
      progress = 1;
      draw();
    } else {
      timeouts.push(window.setTimeout(() => window.dispatchEvent(new CustomEvent('editorial:canvasReady')), compactMotion.matches ? 1850 : 2750));
    }
  }

  /* ---------------------------------------------------------------- */
  /* Pointer parallax (desktop only, subtle)                           */
  /* ---------------------------------------------------------------- */
  function initPointerParallax() {
    if (!stage || !precisePointer.matches || reduceMotion.matches) return;
    const layers = [
      stage.querySelector('.athlete-figure-wrap'),
      ...stage.querySelectorAll('.stage-card'),
      stage.querySelector('.stage-badge'),
    ].filter(Boolean);
    if (!layers.length) return;

    const pointer = { x: 0, y: 0, targetX: 0, targetY: 0 };
    let frameId = 0;

    function onMove(event) {
      const box = stage.getBoundingClientRect();
      pointer.targetX = ((event.clientX - box.left) / box.width - .5) * 16;
      pointer.targetY = ((event.clientY - box.top) / box.height - .5) * 12;
    }

    function render() {
      pointer.x += (pointer.targetX - pointer.x) * .08;
      pointer.y += (pointer.targetY - pointer.y) * .08;
      layers.forEach((layer, index) => {
        const depth = index === 0 ? .3 : .6 + index * .08;
        layer.style.translate = `${(pointer.x * depth).toFixed(2)}px ${(pointer.y * depth).toFixed(2)}px`;
      });
      frameId = window.requestAnimationFrame(render);
    }

    stage.addEventListener('pointermove', onMove, { passive: true, signal });
    stage.addEventListener('pointerleave', () => { pointer.targetX = 0; pointer.targetY = 0; }, { signal });
    frameId = window.requestAnimationFrame(render);
    signal.addEventListener('abort', () => window.cancelAnimationFrame(frameId), { once: true });
  }

  /* ---------------------------------------------------------------- */
  /* Reduced motion + page-leave transition                            */
  /* ---------------------------------------------------------------- */
  function initReducedMotion() {
    if (reduceMotion.matches) document.body.classList.add('is-intro-reduced');
  }

  try {
    initReducedMotion();
    initIntroMotion();
    initAthleteSwitcher();
    initEasterEgg();
    initCanvasTrajectories();
    initPointerParallax();

    window.addEventListener('pagehide', (event) => {
      clearTimeline();
      window.clearTimeout(resizeTimer);
      // 뒤로가기 캐시에 저장되는 페이지는 같은 JS 인스턴스가 그대로
      // 복원된다. 이때 이벤트까지 abort하면 자동 모션이
      // 영구적으로 사라지므로 실제 폐기되는 경우에만 정리한다.
      if (!event.persisted) controller.abort();
    });
  } catch (error) {
    clearTimeline();
    for (let i = 1; i <= 7; i += 1) document.body.classList.add(`is-intro-scene-${i}`);
    document.body.classList.add('is-intro-settled');
  }
})();

/* ---------------------------------------------------------------- */
/* Iris clip-path preview / page transition (recommend panels)       */
/* ---------------------------------------------------------------- */
(() => {
  'use strict';

  const panels = document.querySelectorAll('.recommend-panel[data-iris-target]');
  if (!panels.length) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const PEEK_RADIUS = 250;

  panels.forEach((panel) => {
    const layer = document.querySelector(`.iris-layer[data-iris-layer="${panel.dataset.irisTarget}"]`);
    const preview = panel.querySelector('[data-panel-preview]');
    const frame = preview ? preview.querySelector('[data-iris-frame]') : null;
    const coverFrame = layer ? layer.querySelector('[data-iris-cover-frame]') : null;
    const brand = layer ? layer.querySelector('.iris-layer-brand') : null;
    if (!layer) return;

    let navigating = false;

    function loadFrame(el) {
      if (!el || el.dataset.loaded) return;
      el.dataset.loaded = '1';
      el.src = el.dataset.src;
    }

    // The peek circle is positioned with percentages ("at 50% 50%") relative
    // to the button's own box, which .recommend-panel's overflow: hidden also
    // clips — so it can never bleed past the button edge, and it stays put
    // on scroll without any JS position tracking.
    function setPeek(active) {
      if (!preview || reduceMotion.matches || navigating) return;
      if (active) { loadFrame(frame); loadFrame(coverFrame); }
      preview.classList.add('is-active');
      preview.style.clipPath = `circle(${active ? PEEK_RADIUS : 0}px at 50% 50%)`;
    }

    panel.addEventListener('mouseenter', () => setPeek(true));
    panel.addEventListener('mouseleave', () => setPeek(false));
    panel.addEventListener('focus', () => setPeek(true));
    panel.addEventListener('blur', () => setPeek(false));

    panel.addEventListener('click', (event) => {
      if (reduceMotion.matches || navigating) return;
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
      const href = panel.getAttribute('href');
      if (!href) return;

      event.preventDefault();
      navigating = true;
      if (preview) {
        preview.style.transition = 'none';
        preview.style.clipPath = 'circle(0px at 50% 50%)';
        void preview.offsetWidth;
        preview.style.transition = '';
      }
      loadFrame(coverFrame);

      // Anchor at the same point the hover-peek circle used (the button's own
      // center — that's what "at 50% 50%" resolves to on .panel-preview), not
      // the raw click position, so the click-expand continues from exactly
      // where the peek circle already was instead of jumping to the cursor.
      const rect = panel.getBoundingClientRect();
      const x = rect.left + rect.width / 2;
      const y = rect.top + rect.height / 2;
      const fullRadius = Math.hypot(window.innerWidth, window.innerHeight);

      // Snap the full-screen layer to the exact same size/position the peek
      // circle was already at, with no transition — otherwise this element
      // (starting from the class's default circle(0px)) would itself animate
      // 0 → PEEK_RADIUS under the .85s transition below, growing "from
      // nothing" at the same time the peek circle collapses. That double
      // motion at the same spot is what reads as a stutter/cut. Only after
      // this instant handoff do we turn the transition on for the real
      // PEEK_RADIUS → fullRadius expansion.
      layer.style.transition = 'none';
      layer.style.clipPath = `circle(${PEEK_RADIUS}px at ${x}px ${y}px)`;
      void layer.offsetWidth;
      layer.style.transition = '';
      layer.classList.add('is-transitioning-cover');
      if (brand) brand.classList.add('is-loading');

      const goToTarget = () => { window.location.href = href; };
      let settled = false;
      function onTransitionEnd(transitionEvent) {
        if (transitionEvent.propertyName !== 'clip-path' || settled) return;
        settled = true;
        layer.removeEventListener('transitionend', onTransitionEnd);
        goToTarget();
      }
      layer.addEventListener('transitionend', onTransitionEnd);
      // Fallback in case transitionend never fires (e.g. layout thrash mid-transition).
      window.setTimeout(() => { if (!settled) { settled = true; goToTarget(); } }, 1000);

      requestAnimationFrame(() => {
        requestAnimationFrame(() => { layer.style.clipPath = `circle(${fullRadius}px at ${x}px ${y}px)`; });
      });
    });

    // A page a user reaches via Back/Forward after we navigated away mid-transition
    // may be served from bfcache with the circle still frozen mid-expansion — reset it.
    window.addEventListener('pageshow', (event) => {
      if (!event.persisted) return;
      navigating = false;
      if (preview) { preview.classList.remove('is-active'); preview.style.removeProperty('clip-path'); }
      if (brand) brand.classList.remove('is-loading');
      layer.classList.remove('is-transitioning-cover');
      layer.style.transition = 'none';
      layer.style.removeProperty('clip-path');
      void layer.offsetWidth;
      layer.style.transition = '';
      [frame, coverFrame].forEach((el) => {
        if (!el) return;
        el.removeAttribute('src');
        el.src = 'about:blank';
        delete el.dataset.loaded;
      });
    });
  });
})();
