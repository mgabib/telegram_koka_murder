// Инициализируем Telegram Web App
Telegram.WebApp.ready();

// Выводим объект Telegram.WebApp в консоль для проверки
console.log("Telegram WebApp object:", Telegram.WebApp);

// Игровые переменные
let player = { x: 2, y: 2 };
let maniac = { x: Math.floor(Math.random() * 5), y: Math.floor(Math.random() * 5) };
let score = 0;

// Функция отрисовки игрового поля
function drawField() {
    let field = document.getElementById("game-field");
    field.innerHTML = "";

    for (let y = 0; y < 5; y++) {
        for (let x = 0; x < 5; x++) {
            let cell = document.createElement("div");
            cell.className = "cell";

            if (x === player.x && y === player.y) {
                cell.textContent = "🟢"; // Игрок
            } else if (x === maniac.x && y === maniac.y) {
                cell.textContent = "🔴"; // Маньяк
            } else {
                cell.textContent = "⬜"; // Пустая клетка
            }

            field.appendChild(cell);
        }
    }
}

// Функция для движения игрока
function move(direction) {
    if (direction === "up" && player.y > 0) player.y--;
    if (direction === "down" && player.y < 4) player.y++;
    if (direction === "left" && player.x > 0) player.x--;
    if (direction === "right" && player.x < 4) player.x++;

    score++;
    document.getElementById("score").textContent = "Очки: " + score;

    moveManiac();
    drawField();
}

// Функция движения маньяка к игроку
function moveManiac() {
    if (maniac.x < player.x) maniac.x++;
    if (maniac.x > player.x) maniac.x--;
    if (maniac.y < player.y) maniac.y++;
    if (maniac.y > player.y) maniac.y--;
}

// Обработчик кнопки магазина
document.getElementById("shop-button").addEventListener("click", () => {
    alert("Магазин в разработке!");
});

// Начальная отрисовка поля
drawField();