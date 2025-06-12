function getAsciiCodes() {
    const spaces = Array.from({ length: 10 }, () => 32);
    const alpha = Array.from({ length: 26 }, (_, i) => 65 + i);
    const numbers = Array.from({ length: 10 }, (_, i) => 48 + i);
    return spaces.concat(alpha).concat(numbers);
}
function generateId(matrixColumnId: string, rowId: string): string {
    return `${matrixColumnId}-${rowId}`;
}
function makeRandomLetter(): string {
    const asciiPrintable = window.asciiCodes;
    const index = Math.floor(Math.random() * asciiPrintable.length);
    return String.fromCharCode(asciiPrintable[index]);
}
function changeLetter(elementLetter: HTMLElement) {
    if (elementLetter.parentNode === null) {
        // were removed from DOM
        return;
    }
    const runAfter = Math.floor(Math.random() * 10000);
    setTimeout(() => {
        elementLetter.dispatchEvent(new Event("changeLetter"));
        changeLetter(elementLetter);
    }, runAfter);
}
function makeElementLetter(matrixColumnId: string, letter: string, currentCount: number): HTMLElement {
    const span = document.createElement("span");
    const asciiPrintable = window.asciiCodes;
    span.id = generateId(matrixColumnId, `row-${currentCount + 1}`);
    span.textContent = letter;
    span.addEventListener("changeLetter", (event) => {
        event.currentTarget.textContent = makeRandomLetter(asciiPrintable);
    });
    span.addEventListener("changeLook", (event) => {
        event.currentTarget.style.color = event.detail.color;
        event.currentTarget.style.filter = `blur(${event.detail.blur})`;
    });
    return span;
}
function buildLetters(em: HTMLElement, countLetters: number) {
    // asure children are empty for a matrix column
    em.innerHTML = "";
    let currentCount = 0;
    while (currentCount < countLetters) {
        const letter = makeRandomLetter();
        const lineBreaker = document.createElement("br");
        const elementLetter = makeElementLetter(em.id, letter, currentCount);
        em.appendChild(elementLetter);
        em.appendChild(lineBreaker);
        changeLetter(elementLetter);
        currentCount += 1;
    }
}
function changeLookColumnLetters(em: HTMLElement, firstPoint: Array, secondPoint: Array) {
    let [row, greenPercents, blurValue]: [number, number, number] = firstPoint;
    let [secRow, secGreenPercents, secBlurValue]: [number, number, number] = secondPoint;
    const secIdx = secRow === null ? null : secRow * 2 - 2;
    for (let idx = row * 2 - 2 ; idx >= 0; idx -= 2) {
        if (idx === secIdx) {
            // switch to second
            greenPercents = secGreenPercents;
            blurValue = secBlurValue;
        }
        const cell = em.children[idx];
        const color = `rgb(0% ${greenPercents}% 0%)`;
        const blur = `${blurValue}px`;
        const event = new CustomEvent("changeLook", {detail: {color: color, blur: blur}});
        cell.dispatchEvent(event);
        if (greenPercents > 0) {
            greenPercents -= 5;
        }
        if (blurValue < 10) {
            blurValue += 0.25;
        }
    }
}
function runMatrixColumn(em: HTMLElement, reset: boolean = true) {
    if (reset === true) {
        buildLetters(em, 10);
    }
    let willBreak = false;
    let step: number = 1;
    let secStep: number = null;
    let secCounter: number = 0;
    let firstGreenPcts: number = 100;
    let firstBlurValue: number = 0;
    while (true) {
        const first = step > 10 ? 10 : step;
        const firstGrPcts = firstGreenPcts;
        const firstBlVal = firstBlurValue;
        const second = secStep;
        const currentStep = step;
        const wereBreak = willBreak;
        setTimeout(
            () => changeLookColumnLetters(
                em,
                [first, firstGrPcts, firstBlVal],
                [second, 100, 0]
            ),
            100 * currentStep
        );
        if (currentStep > 10) {
            /***
             For the first lightning run we are nearly after the first end,
             we are going to lower green percentages and blur.
             */
            if (firstGreenPcts >= 80) {
                // the first part of lowering the green (slower)
                firstGreenPcts -= 2;
            } else if (firstGreenPcts >= 0 && firstGreenPcts < 80) {
                // the second part of lowering the green (faster)
                if (firstGreenPcts > 0 && firstGreenPcts < 20) {
                    // just to be sure that we are not lower than the bottom
                    firstGreenPcts = 0;
                } else if (firstGreenPcts === 0) {
                    // it is needed to decide what to do next
                    if (second === null) {
                        // there is a clean situation - only one lightning run has ended
                        const nextRun = 100 * (currentStep + 1);
                        const delay = Math.floor(Math.random() * 10000);
                        // if willBreak is true, we want to have a random rest(delay)
                        const runAfter = wereBreak ? nextRun + delay : nextRun;
                        setTimeout(
                            () => runMatrixColumn(em, wereBreak),
                            runAfter
                        );
                        // !!! END OF MATRIX COLUMN RUN !!!
                        break;
                    } else {
                        /***
                         First run has ended, second is still running, but we mark it
                         as the process will break later with letters reset.
                         */
                        willBreak = true;
                    }
                } else {
                    // huge step down when we are not too deep
                    firstGreenPcts -= 20;
                }
            }
            if (firstBlurValue < 10) {
                firstBlurValue += 0.5;
            }
        }
        if (second === null) {
            // we don't have second lightening run, maybe we want another?
            if (secCounter < 3 && willBreak === false) {
                // we don't want to end process, so we'll see ...
                const probability = Math.random();
                if (probability > 0.75) {
                    // probability - has said yes, we want to have a second lightning run
                    secCounter++;
                    secStep = Math.floor(Math.random() * first)
                    if (secStep === 0) {
                        secStep = 1;
                    }
                }
            }
        } else if (second === 9) {
            // We are at the end of second lightening run, so we can switch it to first ...
            secStep = null;
            firstGreenPcts = 100;
            firstBlurValue = 0;
        } else {
            secStep++;
        }
        step++;
    }
}
function matrix(elementToShow: HTMLElement) {
    window.asciiCodes = getAsciiCodes();
    const matrixColumnIds = Array.from({ length: 10 }, (_, i) => 1 + i);
    htmlElementsMatrix(matrixColumnIds, elementToShow);
    for (const matrixColumnId of matrixColumnIds) {
        const matrixColumn = window.document.getElementById(`col-${matrixColumnId}`);
        setTimeout(
            () => runMatrixColumn(matrixColumn),
            Math.random() * 1000
        );
    }
}
function htmlElementsMatrix(matrixColumnIds: Array[Number], elementToShow: HTMLElement) {
    const bearer = window.document.createElement("div");
    bearer.id = "bearer";
    bearer.onclick = (event: Event) => {event.currentTarget.remove(); window.document.body.appendChild(elementToShow);};
    for (const matrixColumnId of matrixColumnIds) {
        const divId = `col-${matrixColumnId}`;
        const div = window.document.createElement("div");
        div.id = divId;
        div.className = "matrix-column";
        bearer.appendChild(div);
    }
    window.document.body.appendChild(bearer);
}
function startMatrix() {
    if (getCookie("matrixed") === undefined) {
        setCookie("matrixed", true, 30 * 24 * 60 * 60);
        const mainDiv = window.document.getElementById("main");
        window.document.body.removeChild(mainDiv);
        matrix(mainDiv);
    }
}
function getCookie(name: string) {
    const matches = document.cookie.match(
        new RegExp(
            "(?:^|; )" + name.replace(/([$?*|{}\[\]\\\/+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}
function setCookie(name: string, value: any, maxAge: number) {
    options = {
        path: '/',
        maxAge: maxAge
    };
    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
    for (let [key, val] of Object.entries(options)) {
        if (key === "maxAge") {
            if (val === undefined) {
                continue;
            }
            key = "max-age";
        }
        updatedCookie += "; " + key;
        if (val !== true) {
            updatedCookie += "=" + val;
        }
    }
    document.cookie = updatedCookie;
}
setTimeout(
    () => startMatrix(),
    5000
);
