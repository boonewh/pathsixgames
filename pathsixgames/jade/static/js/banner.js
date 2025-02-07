var bannerArray = [
    "jaderegentImages/aelfread.png",
    "jaderegentImages/edam.png",
    "jaderegentImages/haldir.png",
    "jaderegentImages/shura.png",
    "jaderegentImages/tim.png"
];

var headerArray = [
    "Aelfread",
    "Edam",
    "Haldir",
    "Shura", 
    "Tim"
];


var subHeaderArray = [
    "Gestalt Inquisitor-Ninja",
    "Gestalt Paladin-Rogue",
    "Gestalt Wizard-Skald",
    "Gestalt Cleric-Paladin",
    "Gestalt Fighter-Bloodrager"
]

var descriptionArray = [
    "Aelfread is a ghost of the battlefield, stalking his prey invisible and bringing the inquistion of Serenrae upon our foes.",
    "Edam is a little guy. Small of stature, huge on pain...dealing it.",
    "Haldir is a squishy mage. A squishy mage that has a whole lot of tricks up his sleeve. Don't mess with Haldir.",
    "Every party needs a healer. Every party needs a tank. Shura is our rock that heals. No really, he's a rock!",
    "Tim smashes things. That saying, \"You wouldn't like him when he's angry\" Yeah. Don't get on the wrong side of his rage."
]

var currentBanner = 0;
 
function rotate() {
    var bannerPlace = document.getElementById('rotateImages');
    var headingElement = document.getElementById('heading');
    var subheadingElement = document.getElementById('subheading');
    var descriptionElement = document.getElementById('description');

    bannerPlace.src = bannerArray[currentBanner];
    headingElement.textContent = headerArray[currentBanner];
    subheadingElement.textContent = subHeaderArray[currentBanner];
    descriptionElement.textContent = descriptionArray[currentBanner];

    currentBanner++;

    if(currentBanner === bannerArray.length) {
        currentBanner = 0;
    }

    setTimeout(rotate, 4000); 
}

rotate();