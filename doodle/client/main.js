// Wait for dom to load, if it hasn't already

const promptInput = document.getElementById("prompt-input");
const drawingCanvas = document.getElementById("drawing-canvas");
const displayCanvas = document.getElementById("display-canvas");
const ctxDraw = drawingCanvas.getContext("2d");
const ctxDisplay = displayCanvas.getContext("2d");

let isDrawing = false;
let cursorSize = 5;
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

  ctxDraw.endPath();
}

function onMouseMove(e) {
  if (isDrawing) {
    // Get cursor position relative canvas coordinates
    cursorX = e.clientX - drawingCanvas.offsetLeft;
    cursorY = e.clientY - drawingCanvas.offsetTop;

    // Draw a line from the previous cursor position to the current one
    // Set the line width to the cursor size
    ctxDraw.lineWidth = cursorSize;
    ctxDraw.moveTo(prevCursorX, prevCursorY);
    ctxDraw.lineTo(cursorX, cursorY);
    ctxDraw.stroke();

    prevCursorX = cursorX;
    prevCursorY = cursorY;
  }
}

function changeCursorSize(e) {
  cursorSize = Math.max(1, Math.min(100, cursorSize - e.deltaY));
}

drawingCanvas.addEventListener("mousedown", startDrawing);
drawingCanvas.addEventListener("mousemove", onMouseMove);
drawingCanvas.addEventListener("scroll", changeCursorSize);
drawingCanvas.addEventListener("mouseup", stopDrawing);
drawingCanvas.addEventListener("mouseleave", stopDrawing);

// Give the canvas a border
drawingCanvas.style.border = "1px solid black";
displayCanvas.style.border = "1px solid black";

document.addEventListener("blur", stopDrawing);
