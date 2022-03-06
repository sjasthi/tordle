const chooseWord = (words_, ) => {
    // choose random item from words array
    let randomItem = Math.floor(Math.random() * (words_.length - 1)) + 1;
    // solutionWord = words_[randomItem]; 
    return words_[randomItem];
};
const flipTile = (tileNum, state) => {
    let tile = document.querySelector(
        '#guess' + currentGuessCount + 'Tile' + tileNum
    );
    tile.classList.add('flip-in');
    setTimeout(() => {
        tile.classList.add(state);
    }, 250);
    setTimeout(() => {
        tile.classList.remove('flip-in');
        tile.classList.add('flip-out');
    }, 250);
    setTimeout(() => {
        tile.classList.remove('flip-out');
    }, 1500);
};
const checkTelugu = (position, guess_word) => {
    result = {
        0: "absent",
        1: "correct",
        2: "present",
        3: "correct-base",
        4: "present-base"
    };
    return result[guess_word[0]["color_arr"][position]];
};
const checkLetter = (position, currentGuess, solutionWord) => {
    //console.log('checkLetter');
    let guessedLetter = currentGuess.dataset.letters.charAt(position);
    let solutionLetter = solutionWord.charAt(position);
    //console.log(guessedLetter, solutionLetter);

    // If letters match, return "correct"
    if (guessedLetter == solutionLetter) {
        return 'correct';
    }
    // If not a match, if letter exists in solution word, return "present"
    else {
        return solutionWord.includes(guessedLetter) ? 'present' : 'absent';
    }

};


const showSolution = (solutionWord) => {
    alert('Better luck next time. The solution was: ' + solutionWord);
};

// Update tile markup
const updateTiles = (tileNumber, letter) => {
    //console.log('updateTiles(' + tileNumber, letter + ')');
    let currentTile = document.querySelector(
        '#guess' + currentGuessCount + 'Tile' + tileNumber
    );
    currentTile.innerText = letter;

    currentTile.classList.add('has-letter');
};

// Backspace -- Delete last tile markup
const deleteFromTiles = (tileNumber, currentGuessCount) => {
    // remove markup from last tile
    //console.log('deleteFromTiles = ' + tileNumber);
    let currentTile = document.querySelector(
        '#guess' + currentGuessCount + 'Tile' + tileNumber
    );
    currentTile.innerText = '';
    currentTile.classList.remove('has-letter');
};


// Backspace -- Delete last letter
const deleteFromLetters = (currentGuess, currentGuessCount) => {
    // remove last letter from data-letters
    let oldLetters = currentGuess.dataset.letters;
    //console.log('oldLetters = ' + oldLetters);
    let newLetters = oldLetters.slice(0, -1);
    //console.log('newLetters = ' + newLetters);
    currentGuess.dataset.letters = newLetters;
    deleteFromTiles(oldLetters.length, currentGuessCount);
};

// Update "letters"
const updateLetters = (letter, currentGuess) => {
    let oldLetters = currentGuess.dataset.letters;
    let newLetters = oldLetters + letter;
    let currentTile = newLetters.length;
    currentGuess.dataset.letters = newLetters;
    // console.log('currentTile = ' + currentTile);
    updateTiles(currentTile, letter);
};

const jumpTiles = (size, currentGuessCount) => {
    for (let i = 0; i < size; i++) {
        setTimeout(() => {
            let currentTile = document.querySelector(
                '#guess' + currentGuessCount + 'Tile' + (i + 1)
            );
            currentTile.classList.add('jump');
        }, i * 200);
    }
};