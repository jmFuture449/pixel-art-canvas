(() => {
  const size = 32;
  const canvas = document.getElementById('pixel-grid');
  const ctx = canvas.getContext('2d');
  const grid = Array.from({ length: size }, () => Array(size).fill('#ffffff'));
  const status = document.getElementById('status');
  let color = '#000000';
  let drawing = false;

  function render() {
    const cell = canvas.width / size;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let y = 0; y < size; y += 1) {
      for (let x = 0; x < size; x += 1) {
        ctx.fillStyle = grid[y][x];
        ctx.fillRect(x * cell, y * cell, cell, cell);
        ctx.strokeStyle = '#e3e5e9';
        ctx.lineWidth = 0.5;
        ctx.strokeRect(x * cell, y * cell, cell, cell);
      }
    }
  }

  function paint(event) {
    const bounds = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - bounds.left) / bounds.width * size);
    const y = Math.floor((event.clientY - bounds.top) / bounds.height * size);
    if (x >= 0 && x < size && y >= 0 && y < size) {
      grid[y][x] = color;
      render();
    }
  }

  document.querySelectorAll('.swatch').forEach((button) => {
    button.addEventListener('click', () => {
      color = button.dataset.color;
      document.querySelectorAll('.swatch').forEach((swatch) => {
        swatch.setAttribute('aria-pressed', String(swatch === button));
      });
    });
  });

  canvas.addEventListener('pointerdown', (event) => {
    drawing = true;
    canvas.setPointerCapture(event.pointerId);
    paint(event);
  });
  canvas.addEventListener('pointermove', (event) => { if (drawing) paint(event); });
  canvas.addEventListener('pointerup', () => { drawing = false; });
  canvas.addEventListener('pointercancel', () => { drawing = false; });

  document.getElementById('save-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = event.currentTarget.querySelector('button[type="submit"]');
    button.disabled = true;
    status.textContent = 'Saving…';
    status.dataset.state = '';
    try {
      const response = await fetch('/canvases', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: document.getElementById('canvas-name').value, pixel_data: grid }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Unable to save canvas.');
      status.textContent = result.message;
      status.dataset.state = 'success';
    } catch (error) {
      status.textContent = error.message || 'Unable to save canvas. Please try again.';
      status.dataset.state = 'error';
    } finally {
      button.disabled = false;
    }
  });

  render();
})();
