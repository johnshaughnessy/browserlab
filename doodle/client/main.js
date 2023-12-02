// Wait for dom to load, if it hasn't already

const promptInput = document.getElementById("prompt-input");
const strengthInput = document.getElementById("strength-input");
const guidanceScaleInput = document.getElementById("guidance-scale-input");
const drawingCanvas = document.getElementById("drawing-canvas");
const displayCanvas = document.getElementById("display-canvas");
const ctxDraw = drawingCanvas.getContext("2d");
const ctxDisplay = displayCanvas.getContext("2d");

let isDrawing = false;
let cursorSize = 30;
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
  ctxDraw.fillStyle = penColor;
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

    // Use the pen color and cursor size to draw a line
    ctxDraw.strokeStyle = penColor;
    ctxDraw.lineWidth = cursorSize;
    ctxDraw.beginPath();
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

// This is a chechbox, so in the HTML it looks like this:
// <input type="checkbox" id="use-pixelart-input" />
const usePixelartInput = document.getElementById("use-pixelart-input");

function updateDoodleSettings() {
  const doodleSettings = {
    prompt: promptInput.value,
    strength: parseFloat(strengthInput.value),
    guidance_scale: parseFloat(guidanceScaleInput.value),
    use_pixelart: usePixelartInput.checked,
  };

  return fetch("/doodle/settings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(doodleSettings),
  });
}

let syncTimeout = null;
async function sync() {
  const img = new Image();
  img.src = drawingCanvas.toDataURL();

  await updateDoodleSettings()
    .then((res) => res.json())
    .then((data) => {
      console.log("Updated doodle settings:", data);
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

  if (isSyncEnabled) {
    syncTimeout = setTimeout(sync, 1);
  }
}

document.getElementById("enable-sync-button").addEventListener("click", () => {
  clearTimeout(syncTimeout);
  isSyncEnabled = true;
  sync();
});

document.getElementById("disable-sync-button").addEventListener("click", () => {
  clearTimeout(syncTimeout);
  isSyncEnabled = false;
});

document
  .getElementById("clear-drawing-button")
  .addEventListener("click", () => {
    ctxDraw.clearRect(0, 0, drawingCanvas.width, drawingCanvas.height);
  });

const colors = [
  "#ff0000", //(Red)
  "#ff2900",
  "#ff5300",
  "#ff7c00",
  "#ffa600",

  "#ffa600", //(Orange)
  "#ffbc00",
  "#ffd200",
  "#ffe900",
  "#ffff00",

  "#ffff00", //(Yellow)
  "#bfdf00",
  "#80bf00",
  "#409f00",
  "#008000",

  "#008000", //(Green)
  "#006040",
  "#004080",
  "#0020bf",
  "#0000ff",

  "#0000ff", //(Blue)
  "#2000df",
  "#4000bf",
  "#60009f",
  "#800080",

  "#800080", //(Violet)
  "#9f409f",
  "#bf80bf",
  "#dfbfdf",
  "#ffffff", //(White/Gray/Black)

  "#000000", // (Black)
  "#400000", // (Dark Red)
  "#800000", // (Medium Red)
  "#bf0000", // (Bright Red)
  "#ff0000", // (Vibrant Red)

  "#000000", // (Black)
  "#402900", // (Dark Orange)
  "#805300", // (Medium Orange)
  "#bf7c00", // (Bright Orange)
  "#ffa600", // (Vibrant Orange)

  "#000000", // (Black)
  "#404000", // (Dark Yellow)
  "#808000", // (Medium Yellow)
  "#bfbf00", // (Bright Yellow)
  "#ffff00", // (Vibrant Yellow)

  "#000000", // (Black)
  "#004000", // (Dark Green)
  "#008000", // (Medium Green)
  "#00bf00", // (Bright Green)
  "#00ff00", // (Vibrant Green)

  "#000000", // (Black)
  "#000040", // (Dark Blue)
  "#000080", // (Medium Blue)
  "#0000bf", // (Bright Blue)
  "#0000ff", // (Vibrant Blue)

  "#000000", // (Black)
  "#200020", // (Dark Violet)
  "#400040", // (Medium Violet)
  "#600060", // (Bright Violet)
  "#800080", // (Vibrant Violet)

  "#000000", // (Black)
  "#404040", // (Dark Gray)
  "#808080", // (Medium Gray)
  "#bfbfbf", // (Light Gray)
  "#ffffff", // (White)
];

let penColor = "#000000";
const colorSwatches = document.getElementById("color-swatches");

colors.forEach((color) => {
  // For each color, create a small swatch/button that sets the pen color
  const swatch = document.createElement("button");
  swatch.style.backgroundColor = color;
  swatch.style.width = "20px";
  swatch.style.height = "20px";
  swatch.style.border = "none";
  swatch.style.margin = "2px";
  swatch.style.padding = "0px";
  swatch.style.cursor = "pointer";
  swatch.addEventListener("click", () => {
    penColor = color;
    ctxDraw.fillStyle = penColor;
    console.log("Pen color set to " + penColor);
  });
  colorSwatches.appendChild(swatch);
});

const filePicker = document.createElement("input");
filePicker.type = "file";
filePicker.accept = "image/*";

filePicker.addEventListener("change", (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onload = (e) => {
    const img = new Image();
    img.onload = () => {
      // Fit the image to the canvas
      const scale = Math.min(
        drawingCanvas.width / img.width,
        drawingCanvas.height / img.height,
      );
      const x = drawingCanvas.width / 2 - (img.width / 2) * scale;
      const y = drawingCanvas.height / 2 - (img.height / 2) * scale;
      ctxDraw.drawImage(img, x, y, img.width * scale, img.height * scale);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
});
document.getElementById("add-bg-image-button").addEventListener("click", () => {
  filePicker.click();
});
