// Selecting all of the major working parts of the game.
const form = document.querySelector('#guessForm');
const input = document.querySelector('input');
const scoreSection = document.querySelector('#score');
const timeSection = document.querySelector('#time');
const button = document.querySelector('button');
const burgerMenu = document.querySelector('#open');
const slideBar = document.querySelector('.slidebar');
const closeSidebar = document.querySelector('#close');
const container = document.querySelector('.container');

let score = 0;
let time = 60;
let gamesPlayed = 0;
let alreadyUsed = new Set()

// Used to get form data and send a request
// to validate the word passed into the form.
const getFormData = async function(evt) {
    evt.preventDefault();
    if (!input.value.length) return;
    
    let {resp, data} = await axios.get('/temp', 
    {params: {word: input.value}});
    if (!alreadyUsed.has(input.value)) {
        displayMessage(data);
        score += increaseScore(data, input.value);
        alreadyUsed.add(input.value);
    }
    scoreSection.innerText = score;
    input.value = ''
}

// Displays the status message in the proper place.
const displayMessage = (msg) => {
    const displaySection = document.querySelector('#msg');
    displaySection.innerText = msg + '!';
}

// Increases the score to be displayed on the front-end.
const increaseScore = (message, word) => {
    if (message === 'ok') return word.length;
    return 0;
}

// Used to start the timer, count it down, and eventually clear it.
// Sends a POST request to the server at the end of the game to let
// it know to add another game played to the session.
const timer = setInterval(async function() {
    timeSection.innerText = `:${time}`;
    time--
    if (time === -1) {
        timeSection.innerText = 'Game Over!';
        button.disabled = true;
        gamesPlayed++;
        await axios.post('/games', {games: gamesPlayed})
        clearInterval(timer);
    }
},1000);

// handles what happens if the sliding sidebar was opened but not closed
// and the screen was enlarged.
setInterval(() => {
    if (window.innerWidth <= 1000) {
        burgerMenu.classList.remove('hide')
        burgerMenu.classList.add('show')
    } else {
        burgerMenu.classList.remove('show')
        burgerMenu.classList.add('hide')
        slideBar.style.display = 'none';
        closeSidebar.style.display = 'none';
        container.style.display = 'grid';
    }
},200);

// handles the opening and display of the sliding sidebar.
burgerMenu.addEventListener('click', (e) => {
    setTimeout(() => {
        slideBar.style.width = '1000px';
    },10)
    slideBar.style.display = 'flex';
    closeSidebar.style.display = 'block';
    burgerMenu.classList.add('hide');
    burgerMenu.classList.remove('show');
    container.style.display = 'none';
});

// handles the closing of the sidebar and display of the main game screen.
closeSidebar.addEventListener('click', (e) => {
    setTimeout(() => {
        slideBar.style.width = '0px';
    },10)
    slideBar.style.display = 'none';
    closeSidebar.style.display = 'none';
    burgerMenu.classList.add('show');
    burgerMenu.classList.remove('hide');
    container.style.display = 'grid';
});

// handles submission of the guess form.
form.addEventListener('submit', getFormData);

