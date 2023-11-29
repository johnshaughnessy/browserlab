// Wait for dom to load, if it hasn't already

const promptInput = document.getElementById("prompt-input");
const drawingCanvas = document.getElementById("drawing-canvas");
const displayCanvas = document.getElementById("display-canvas");
const ctxDraw = drawingCanvas.getContext("2d");
const ctxDisplay = displayCanvas.getContext("2d");

let isDrawing = false;
let cursorSize = 10;
let cursorX = 0;
let cursorY = 0;

let prevCursorX = 0;
let prevCursorY = 0;

function startDrawing(e) {
  // Get cursor position relative canvas coordinates
  cursorX = e.clientX - drawingCanvas.offsetLeft;
  cursorY = e.clientY - drawingCanvas.offsetTop;

  prevCursorX = cursorX;
  prevCursorY = cursorY;

  // Draw a circle at the cursor position
  ctxDraw.beginPath();
  ctxDraw.arc(cursorX, cursorY, cursorSize / 2, 0, 2 * Math.PI);
  ctxDraw.fill();

  isDrawing = true;
}

function stopDrawing(e) {
  isDrawing = false;
}

function onMouseMove(e) {
  if (isDrawing) {
    // Get cursor position relative canvas coordinates
    cursorX = e.clientX - drawingCanvas.offsetLeft;
    cursorY = e.clientY - drawingCanvas.offsetTop;

    ctxDraw.beginPath();
    ctxDraw.lineWidth = cursorSize;
    ctxDraw.moveTo(prevCursorX, prevCursorY);
    ctxDraw.lineTo(cursorX, cursorY);
    ctxDraw.stroke();

    prevCursorX = cursorX;
    prevCursorY = cursorY;
  }
}

function changeCursorSize(e) {
  cursorSize = Math.max(1, Math.min(100, cursorSize - e.deltaY / 100));
  console.log(cursorSize);
}

drawingCanvas.addEventListener("mousedown", startDrawing);
drawingCanvas.addEventListener("mousemove", onMouseMove);
drawingCanvas.addEventListener("wheel", changeCursorSize);
drawingCanvas.addEventListener("mouseup", stopDrawing);
drawingCanvas.addEventListener("mouseleave", stopDrawing);

// Give the canvas a border
drawingCanvas.style.border = "1px solid black";
displayCanvas.style.border = "1px solid black";

document.addEventListener("blur", stopDrawing);

let syncTimeout = null;
async function sync() {
  const img = new Image();
  img.src = drawingCanvas.toDataURL();

  await fetch("/doodle/prompt", {
    method: "POST",
    body: promptInput.value,
  })
    .then((res) => res.json())
    .then((data) => {
      //ctxDisplay.clearRect(0, 0, displayCanvas.width, displayCanvas.height);
      // Display the prompt on the display canvas
      ctxDisplay.font = "20px sans-serif";
      ctxDisplay.fillText(data.prompt, 10, 20);
    });

  // POST to /doodle/image
  // The API will return an image for us to display
  // on the display canvas
  const response = await fetch("/doodle/image", {
    method: "POST",
    body: img.src,
  });

  // Get the image data from the response
  await response.blob().then((blob) => {
    const img = new Image();
    img.onload = () => {
      ctxDisplay.drawImage(img, 0, 0);
    };
    img.src = URL.createObjectURL(blob);
    // Add the image to the page so that it loads
    // and we can draw it to the canvas
    //document.body.appendChild(img);
  });

  syncTimeout = setTimeout(sync, 1);
}

document.getElementById("enable-sync-button").addEventListener("click", () => {
  clearTimeout(syncTimeout);
  sync();
});

document.getElementById("disable-sync-button").addEventListener("click", () => {
  clearTimeout(syncTimeout);
});
