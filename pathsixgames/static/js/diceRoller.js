"use strict";

const rollButtons = document.querySelectorAll(".roll-button");
rollButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
        const clickedButton = event.target;
        const type = clickedButton.getAttribute("data-type");
        const numDice = parseInt(document.getElementById(`${type}Num`).value);
        if (type === "percentile") {
            rollPercentile(numDice);
        } else {
            rollDice(type, numDice);
        }
    });
});

const clearResultsButton = document.getElementById("clearResults");
clearResultsButton.addEventListener("click", clearResults);

function rollDice(type, numDice) {
    let results = [];
    let sum = 0;
    let i = 0;

    let diceMax = parseInt(type.slice(1));

    function rollSingleDie() {
        const roll = Math.floor(Math.random() * diceMax + 1);
        results.push(roll);
        sum += roll;
    }

    function rollNext() {
        if (i < numDice) {
            rollSingleDie();
            i++;
            document.getElementById(`${type}Results`).innerHTML = "Results: " + results.join(", ");
            document.getElementById(`${type}Total`).innerHTML = "Total: " + sum;

            setTimeout(rollNext, 250); // Quarter-second delay
        } else {
            updateTotal();
        }
    }

    rollNext();
}

function rollPercentile(numDice) {
    let results = [];
    let sum = 0;
    let i = 0;

    function roll() {
        const tens = Math.floor(Math.random() * 10);
        const ones = Math.floor(Math.random() * 10);
        const result = (tens * 10) + ones;
        results.push(result);
        sum += result;
    }

    function rollNext() {
        if (i < numDice) {
            roll();

            i++;
            document.getElementById("percentileResults").innerHTML = "Results: " + results.join(", ");
            document.getElementById("percentileTotal").innerHTML = "Total: " + sum;

            setTimeout(rollNext, 250); // Quarter-second delay
        } else {
            updateTotal();
        }
    }

    rollNext();
}

function updateTotal() {
    const diceTypes = ["d4", "d6", "d8", "d10", "d12", "d20", "percentile"];
    let total = 0;
    let hasValidRolls = false; // Flag to check if there are valid roll results

    for (const type of diceTypes) {
        const totalStr = document.getElementById(`${type}Total`).innerHTML;
        if (totalStr !== "") {
            const rollValue = parseInt(totalStr.split(": ")[1]);
            if (!isNaN(rollValue)) {
                total += rollValue;
                hasValidRolls = true;
            }
        }
    }

    if (hasValidRolls) {
        document.getElementById("total").innerHTML = "Total of All Rolls: " + total;
    } else {
        document.getElementById("total").innerHTML = "Total of All Rolls: 0";
    }
}

function clearResults() {
    const diceTypes = ["d4", "d6", "d8", "d10", "d12", "d20", "percentile"];
    
    for (const type of diceTypes) {
        document.getElementById(`${type}Results`).innerHTML = "Results:";
        document.getElementById(`${type}Total`).innerHTML = "Total:";
    }

    document.getElementById("total").innerHTML = "Total of All Rolls: 0";
    updateTotal();
}