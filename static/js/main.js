/**
 * """Author: Nalongsone Danddank, Final Project, begin on Feb 2 2022, end on April 27, 2022, ICS499 METRO STATE """
 */
COLOR_CLASS = {
    0: "absent",
    1: "correct",
    2: "present",
    3: "correct-base",
    4: "present-base"
};
const chooseWord = (words_, ) => {
    // choose random item from words array
    let randomItem = Math.floor(Math.random() * (words_.length - 1)) + 1;
    // solutionWord = words_[randomItem]; 
    return words_[randomItem];
};
const flipTileTelugu = (row, col, state) => {
    let tile = document.querySelector(
        '#guess' + (row + 1) + 'Tile' + (col + 1)
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
const checkTelugu = (position, n, guess_word) => {

    return COLOR_CLASS[guess_word[n]["color_arr"][position]];
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
// Update tile markup for Telugu
const updateTilesTelugu = (row, col, letter, color_idx) => {
    let currentTile = document.querySelector(
        '#guess' + (row + 1) + 'Tile' + (col + 1)
    );
    currentTile.innerText = letter;
    currentTile.classList.add(COLOR_CLASS[color_idx]);
};
// Update tile markup for Telugu for flip
const updateTilesTeluguForFlip = (row, col, letter, color_idx) => {
    let currentTile = document.querySelector(
        '#guess' + (row + 1) + 'Tile' + (col + 1)
    );
    currentTile.innerText = letter;
    currentTile.classList.add('has-letter');
};

// Backspace -- Delete last tile markup
const deleteFromTiles = (tileNumber, currentGuessCount) => {
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

function PostDataRedirect(data, dataName, location) {
    var form = document.createElement("form");

    form.method = "POST";
    form.action = location;

    if (data.constructor === Array && dataName.constructor === Array) {
        for (var i = 0; i < data.length; i++) {
            var element = document.createElement("input");
            element.type = "hidden";
            element.value = data[i];
            element.name = dataName[i];
            form.appendChild(element);
        }
    } else {
        var element1 = document.createElement("input");
        element1.type = "hidden";
        element1.value = data;
        element1.name = dataName;
        form.appendChild(element1);
    }

    document.body.appendChild(form);

    form.submit();
}

// PostDataRedirect([ un, pw ], ["un", "pw"], "login.php");